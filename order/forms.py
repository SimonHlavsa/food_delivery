from django import forms
from .models import Order
from django.forms import ValidationError


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'restaurant', 'food', 'status']

    def clean(self):
        all_food = self.cleaned_data.get('food')
        restaurant = self.cleaned_data.get('restaurant')
        if all_food:
            for food in all_food:
                if food.restaurant != restaurant:
                    raise ValidationError("All foods in the order must belong to the same restaurant.")
        return self.cleaned_data