from django.shortcuts import render, get_object_or_404, redirect
from customer.models import UserProfile
from order.models import Food, Order
from order.forms import FoodForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from customer.decorators import user_type_required

def home(response):
    if not response.user.is_authenticated:
        return render(response, "core/home.html", {})

    user = UserProfile.objects.get(id = response.user.id)
    if user.user_type == "customer":
        return redirect("restaurants")
    elif user.user_type == "restaurant":
        return render(response, "core/home.html", {})


def not_allowed(response):
    return render(response, "core/not_allowed.html")


@user_type_required("customer")
def restaurants(response):
    all_restaurants = UserProfile.objects.filter(user_type = "restaurant")
    return render(response, "core/restaurants.html", {"all_restaurants": all_restaurants})


@user_type_required("restaurant")
def manage_food(response):
    user = UserProfile.objects.get(id = response.user.id)
    all_food = Food.objects.filter(restaurant = user)
    return render(response, "core/manage_food.html", {"all_food": all_food})

@user_type_required("restaurant")
def remove_food(response, food_id):
    food = get_object_or_404(Food, id=food_id)
    food.delete()
    return redirect("manage_food")
    

@user_type_required("restaurant")
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            try:
                food = form.save(commit=False)
                food.restaurant = request.user
                food.save()
                return redirect('manage_food')
            except ValidationError as e:
                return render(request, 'core/food_form.html', {'form': form, "error":e.message})
            
    else:
        form = FoodForm()

    return render(request, 'core/food_form.html', {'form': form})

@user_type_required("restaurant")
def manage_food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)  # získání instance jídla
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)  # předání POST dat, souborů a instance
        if form.is_valid():
            form.save()  # uložení formuláře, provede aktualizaci instance Food
            return redirect('manage_food')  # přesměrování na jiný pohled po aktualizaci
    else:
        form = FoodForm(instance=food)  # inicializace formuláře s existující instancí

    return render(request, 'core/food_form.html', {'form': form})

@user_type_required("customer")
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

@login_required
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