
from django.urls import path

from . import views, api_views

app_name = "staff"

urlpatterns = [
    # Staff HTML pages
    path("orders/", views.orders, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path(
        "orders/<int:order_id>/status/",
        views.change_status,
        name="change_status",
    ),
    path("menu/", views.menu, name="menu"),
    path(
        "menu/<int:item_id>/toggle/",
        views.toggle_availability,
        name="toggle_availability",
    ),

    # Staff API endpoints
    path("api/orders/", api_views.orders_api, name="orders_api"),
    path(
        "api/orders/<int:order_id>/",
        api_views.order_detail_api,
        name="order_detail_api",
    ),
    path(
        "api/orders/<int:order_id>/status/",
        api_views.change_order_status_api,
        name="change_order_status_api",
    ),
]
