
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from customer.core.models import FoodOrder, OrderItem


@require_GET
def orders_api(request):
    orders = FoodOrder.objects.all()

    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "customer": order.customer.name,
            "status": order.status,
            "total": str(order.total),
            "created_at": order.created_at.isoformat(),
        })

    return JsonResponse({"orders": data})


@require_GET
def order_detail_api(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id)

    items = [
        {
            "food_item": item.food_item.name,
            "quantity": item.quantity,
            "unit_price": str(item.unit_price),
        }
        for item in order.items.all()
    ]

    return JsonResponse({
        "id": order.id,
        "customer": order.customer.name,
        "status": order.status,
        "total": str(order.total),
        "items": items,
    })


@csrf_exempt
@require_POST
def change_order_status_api(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id)

    try:
        body = json.loads(request.body)
        new_status = body["status"]

        allowed = [
            "Placed",
            "Preparing",
            "Delivered",
            "Cancelled",
        ]

        transitions = {
            "Placed": ["Preparing", "Cancelled"],
            "Preparing": ["Delivered", "Cancelled"],
            "Delivered": [],
            "Cancelled": [],
        }

        if new_status not in allowed:
            return JsonResponse({"error": "Invalid status"}, status=400)

        if new_status not in transitions[order.status]:
            return JsonResponse(
                {"error": "Status change not allowed"},
                status=400,
            )

        order.status = new_status
        order.save(update_fields=["status"])

        return JsonResponse({
            "message": "Status updated successfully",
            "order_id": order.id,
            "status": order.status,
        })

    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid request body"}, status=400)
