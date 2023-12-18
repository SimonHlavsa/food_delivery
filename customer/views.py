from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerCreationForm, RestaurantCreationForm


def register_customer(response):
    if response.method == "POST":
        form = CustomerCreationForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'customer'
            form.save()
        return redirect("/")
    else:
        form = CustomerCreationForm()

    return render(response, "customer/register.html", {"form":form})


def register_restaurant(response):
    if response.method == "POST":
        form = RestaurantCreationForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'restaurant'
            form.save()
        return redirect("/")
    else:
        form = RestaurantCreationForm()

    return render(response, "customer/register.html", {"form":form})



def logout_user(response):
    logout(response)
    return redirect("/")
