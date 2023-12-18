from django.db import models
from customer.models import UserProfile
from django.forms import ValidationError


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=300, blank=True)
    restaurant = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def clean(self):
    # Kontrola, zda UserProfile spojený s jídlem je typu 'restaurant'
        if self.restaurant and self.restaurant.user_type != 'restaurant':
            raise ValidationError("This UserProfile is not a restaurant and cannot be associated with food.")
        super().clean()

class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = "in_progress")

    
class Order(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_orders')
    restaurant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_orders')
    food = models.ManyToManyField(Food, blank=True)
    CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed ', 'Completed'),
        ('canceled ', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=CHOICES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = models.Manager()
    active = OrderManager()

    def __str__(self):
        return f"Order ID: {self.id}"
   
    def validate_customer_restaurant_types(self):
        if self.customer.user_type != 'customer':
            raise ValidationError("The customer must be of user type 'customer'.")

        if self.restaurant.user_type != 'restaurant':
            raise ValidationError("The restaurant must be of user type 'restaurant'.")
    
    def clean(self):
        self.validate_customer_restaurant_types()
        return super().clean()
    
    def add_food(self, selected_food):
            for food_id in selected_food:
                food = Food.objects.get(id=food_id)
                self.food.add(food)
            self.set_total_price()
 
    def set_total_price(self):
        total_price = sum(food.price for food in self.food.all())
        self.total_price = total_price
        self.save()

    