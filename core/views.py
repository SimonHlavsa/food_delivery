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
        selected_food = response.POST.get("selected_food")

        order = Order.objects.create(customer = customer, restaurant = restaurant)
        order.save()
        
        for food_id in selected_food:
            food = Food.objects.get(id=food_id)
            order.food.add(food)

        return redirect("/")

    else:
        restaurant = UserProfile.objects.get(id = pk)
        customer = UserProfile.objects.get(id = response.user.id)    
        print(customer)
        all_food = Food.objects.filter(restaurant = restaurant)
    return render(response, "core/restaurant_menu.html", {"restaurant": restaurant, "all_food": all_food, "customer":customer})