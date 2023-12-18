from django.contrib import admin
from .models import UserProfile
from order.models import Food

class FoodInline(admin.StackedInline):
    model = Food
    extra = 0

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_filter = ['user_type', 'is_active', 'is_superuser', 'is_staff']  

    fieldsets = (
        (None, {'fields': ('user_type', 'email', 'password')}),
        ('Personal info', {'fields': ('restaurant_name', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type'),
        }),
    )

    inlines = [FoodInline]  


    
admin.site.register(UserProfile, UserProfileAdmin)
