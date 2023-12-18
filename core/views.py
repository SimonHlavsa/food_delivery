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
        order_id_cancel = response.POST.get("cancel_order")
        order_id_complete = response.POST.get("complete_order")

        if order_id_cancel:
            order = Order.objects.get(id = order_id_cancel)
            if order.status != "completed":
                order.status = "canceled"
                order.save()
            
        elif order_id_complete:
            order = Order.objects.get(id = order_id_complete)
            if order.status != "canceled":
                order.status = "completed"
                order.save()

    user = UserProfile.objects.get(id = response.user.id)
    if user.user_type == "customer":    
        all_orders = Order.objects.filter(customer = user).order_by("-created_at")
    elif user.user_type == "restaurant":
        all_orders = Order.objects.filter(restaurant = user).order_by("-created_at")
    return render(response, "core/all_orders.html", {"all_orders": all_orders})