
from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    # Customer pages
    path("menu/", views.menu_page, name="menu"),

    # Customer API
    path("api/menu/", views.menu_api, name="menu_api"),
    path("api/customers/", views.create_customer_api, name="create_customer_api"),
    path("api/checkout/", views.checkout_api, name="checkout_api"),
    path(
        "api/orders/<int:order_id>/status/",
        views.order_status_api,
        name="order_status_api",
    ),
path("favorites/", views.favorites_page, name="favorites"),
path("cart/", views.cart_page, name="cart"),
path("profile/", views.profile_page, name="profile"),
path("", views.home_page, name="home"),
]


