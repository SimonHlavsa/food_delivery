from django.shortcuts import render, redirect
from customer.models import UserProfile
from order.models import Food, Order

def home(response):
    return render(response, "core/home.html", {})

def restaurants(response):
    all_restaurants = UserProfile.objects.filter(user_type = "restaurant")
    return render(response, "core/restaurants.html", {"all_restaurants": all_restaurants})

def restaurant_menu(response, pk):
    if response.method == "POST":
        restaurant = UserProfile.objects.get(id = response.POST.get("restaurant"))
        customer = UserProfile.objects.get(id = response.POST.get("customer"))    
        selected_food = response.POST.getlist("selected_food[]")

        order = Order.objects.create(customer = customer, restaurant = restaurant)
        
        order.add_food(selected_food)

        return redirect("/")

    else:
        restaurant = UserProfile.objects.get(id = pk)
        customer = UserProfile.objects.get(id = response.user.id)    
        all_food = Food.objects.filter(restaurant = restaurant)
    return render(response, "core/restaurant_menu.html", {"restaurant": restaurant, "all_food": all_food, "customer":customer})


def all_orders(response):
    if response.method == "POST":
        order_id = response.POST.get("cancel_order")
        order = Order.objects.get(id = order_id)
        order.status = "canceled"
        order.save()

    customer = UserProfile.objects.get(id = response.user.id)    
    all_orders = Order.objects.filter(customer = customer)
    return render(response, "core/all_orders.html", {"all_orders": all_orders})