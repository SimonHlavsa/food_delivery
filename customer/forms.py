from django import forms
from .models import Food, Order
from django.forms import ValidationError


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'restaurant', 'food', 'is_done', 'is_canceled']

    def clean(self):
        all_food = self.cleaned_data.get('food')
        restaurant = self.cleaned_data.get('restaurant')
        if all_food:
            # only check the words if the language is valid
            for food in all_food:
                if food.restaurant != restaurant:
                    raise ValidationError("All foods in the order must belong to the same restaurant.")
        return self.cleaned_data