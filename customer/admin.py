from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from order.models import Food
from .forms import UserProfileForm

# Register your models here.

class FoodInline(admin.StackedInline):
    model = Food
    extra = 0



class UserProfileAdmin(UserAdmin):
    add_form = UserProfileForm
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
    )
    inlines = [FoodInline]  

admin.site.register(UserProfile, UserProfileAdmin)

        # (
        #     "Permissions", 
        #     {
        #         "fields": (
        #             "is_active",
        #             "is_staff",
        #             "is_superuser",
        #             "groups",
        #             "user_permissions",
        #         ),
        #     }
        # ),
        # (
        #     "Important dates", 
        #     {
        #         "fields": (
        #             "last_login",
        #             "date_joined",
        #         ),
        #     }
        # ),