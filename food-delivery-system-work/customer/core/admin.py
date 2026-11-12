
from django.contrib import admin
from .models import Customer, FoodItem, FoodOrder, OrderItem

admin.site.register(Customer)
admin.site.register(FoodItem)
admin.site.register(FoodOrder)
admin.site.register(OrderItem)

