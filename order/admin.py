from django.contrib import admin
from .models import Order, Food
from .forms import OrderForm

# Register your models here.


admin.site.register(Food)

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
admin.site.register(Order, OrderAdmin)