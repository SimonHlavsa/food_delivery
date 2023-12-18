from django.urls import path
from .views import home, restaurants, restaurant_menu

urlpatterns = [
    path("", home, name="home"),
    path("restaurants/", restaurants, name="restaurants"),
    path("restaurant/<int:pk>", restaurant_menu, name="restaurant_menu"),
]