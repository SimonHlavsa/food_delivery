from django.urls import path
from .views import home, restaurants, restaurant_menu, all_orders

urlpatterns = [
    path("", home, name="home"),
    path("restaurants/", restaurants, name="restaurants"),
    path("restaurant/<int:pk>", restaurant_menu, name="restaurant_menu"),
    path("orders/", all_orders, name="all_orders"),
]