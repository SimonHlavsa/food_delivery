from django.db import models
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.db.models.query import QuerySet
from django.forms import ValidationError


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="customer")

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="restaurant")

class UserProfile(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_CHOICES)

    objects = UserManager()
    customer = CustomerManager()
    restaurant = RestaurantManager()

    # def __str__(self):
    #     return self.username


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
        return super().get_queryset().filter(is_done=False, is_cnceled=False)

    
class Order(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_orders')
    restaurant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_orders')
    food = models.ManyToManyField(Food)
    is_done = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = OrderManager()

    def __str__(self):
        return f"Order ID: {self.id}"
    
   


    def validate_customer_restaurant_types(self):
        if self.customer.user_type != 'customer':
            raise ValidationError("The customer must be of user type 'customer'.")

        if self.restaurant.user_type != 'restaurant':
            raise ValidationError("The restaurant must be of user type 'restaurant'.")
    
    def validate_food(self):
        foods_from_same_restaurant_ids = self.food.filter(restaurant_id=self.restaurant_id).values_list('id', flat=True)
        if set(foods_from_same_restaurant_ids) != set(self.food.values_list('id', flat=True)):
            raise ValidationError("All foods in the order must belong to the same restaurant.")
         
        
    def clean(self):
        self.validate_customer_restaurant_types()
        # self.validate_food()
        return super().clean()
    



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
