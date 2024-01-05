from django.urls import path
from .views import home, restaurants, restaurant_menu, all_orders, manage_food, manage_food_detail, add_food, remove_food,not_allowed

urlpatterns = [
    path("", home, name="home"),
    path("not_allowed/", not_allowed, name="not_allowed"),
    path("restaurants/", restaurants, name="restaurants"),
    path("restaurant/<int:pk>", restaurant_menu, name="restaurant_menu"),
    path("orders/", all_orders, name="all_orders"),
    path("manage_food/", manage_food, name="manage_food"),
    path("manage_food/<int:food_id>", manage_food_detail, name="manage_food_detail"),
    path("remove_food/<int:food_id>", remove_food, name="remove_food"),
    path("add_food/", add_food, name="add_food"),
]   