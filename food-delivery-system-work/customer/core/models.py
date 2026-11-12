
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "food_item"

    def __str__(self):
        return self.name


class FoodOrder(models.Model):
    class Status(models.TextChoices):
        PLACED = "Placed", "Placed"
        PREPARING = "Preparing", "Preparing"
        DELIVERED = "Delivered", "Delivered"
        CANCELLED = "Cancelled", "Cancelled"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "food_order"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        FoodOrder,
        on_delete=models.PROTECT,
        related_name="items"
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_item"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "food_item"],
                name="unique_order_food_item"
            )
        ]

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
