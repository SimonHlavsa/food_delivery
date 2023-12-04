from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Food

# Register your models here.

class FoodInline(admin.StackedInline):
    model = Food
    extra = 0

class CusetomUserAdmin(UserAdmin):
    fieldsets = (
        
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "User Fields",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "user_type",
                ),
            },
        ),
    
        (
            "Permissions", 
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            }
        ),
        (
            "Important dates", 
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            }
        ),
    )
    inlines = [FoodInline]  


admin.site.register(UserProfile, CusetomUserAdmin)
admin.site.register(Food)
