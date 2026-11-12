
import json
from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, FoodItem, FoodOrder, OrderItem


# CUSTOMER HTML PAGE

@require_GET
def menu_page(request):
    items = FoodItem.objects.filter(is_available=True)
    return render(request, "customer/menu.html", {
        "items": items,
        "menu_items": items,
    })


# CUSTOMER API

@require_GET
def menu_api(request):
    items = FoodItem.objects.filter(is_available=True)

    data = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": str(item.price),
            "is_available": item.is_available,
        }
        for item in items
    ]

    return JsonResponse({"menu": data})


@csrf_exempt
@require_POST
def create_customer_api(request):
    try:
        body = json.loads(request.body)

        customer = Customer.objects.create(
            name=body["name"],
            email=body["email"],
            phone=body["phone"],
            address=body["address"],
        )

        return JsonResponse({
            "message": "Customer created successfully",
            "customer_id": customer.id,
        }, status=201)

    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid customer data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
def checkout_api(request):
    try:
        body = json.loads(request.body)
        customer = get_object_or_404(Customer, id=body["customer_id"])
        items = body["items"]

        if not items:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        with transaction.atomic():
            order = FoodOrder.objects.create(customer=customer)
            total = Decimal("0.00")

            for entry in items:
                food = get_object_or_404(
                    FoodItem,
                    id=entry["food_item_id"],
                    is_available=True,
                )
                quantity = int(entry["quantity"])

                if quantity <= 0:
                    raise ValueError("Quantity must be positive")

                total += food.price * quantity

                OrderItem.objects.create(
                    order=order,
                    food_item=food,
                    quantity=quantity,
                    unit_price=food.price,
                )

            order.total = total
            order.save(update_fields=["total"])

        return JsonResponse({
            "message": "Order created successfully",
            "order_id": order.id,
            "total": str(order.total),
            "status": order.status,
        }, status=201)

    except (KeyError, ValueError, json.JSONDecodeError) as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_GET
def order_status_api(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id)

    return JsonResponse({
        "order_id": order.id,
        "status": order.status,
        "total": str(order.total),
        "created_at": order.created_at.isoformat(),
    })

def favorites_page(request):
    return render(request, "customer/favorites.html")


def cart_page(request):
    return render(request, "customer/cart.html")


def profile_page(request):
    return render(request, "customer/profile.html")

def home_page(request):
    return render(request, "customer/home.html")
