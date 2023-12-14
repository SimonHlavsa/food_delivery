from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.forms import ValidationError


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="customer")

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="restaurant")

class UserProfile(AbstractUser):

    USER_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_CHOICES)

    objects = UserManager()
    customer = CustomerManager()
    restaurant = RestaurantManager()

    def __str__(self):
        return self.username


    # def create_order(self, customer, restaurant, food_items):
    #     self.validate_customer_restaurant_types(customer, restaurant)

    #     order = self.active.create(customer=customer, restaurant=restaurant)
    #     order.food.add(*food_items)
    #     return order
    

# customer_user_profile = UserProfile.objects.get(pk=1)  # Získání instance uživatelského profilu typu 'customer'
# restaurant_user_profile = UserProfile.objects.get(pk=2)  # Získání instance uživatelského profilu typu 'restaurant'
# selected_food_items = Food.objects.filter(restaurant=restaurant_user_profile)[:3]  # Vybrání jídel od daného restauračního profilu

# try:
#     new_order = Order().create_order(customer_user_profile, restaurant_user_profile, selected_food_items)
#     print("Objednávka byla úspěšně vytvořena!")
# except ValidationError as e:
#     print(f"Chyba při vytváření objednávky: {e}")
