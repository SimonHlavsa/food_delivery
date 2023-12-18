from django.contrib import admin
from .models import Order, Food
from .forms import OrderForm

# Register your models here.


admin.site.register(Food)

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Order, OrderAdmin)