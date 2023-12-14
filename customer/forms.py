from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_CHOICES)
    password1 = forms.PasswordInput()
    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'user_type')

        
class UserProfileForm(UserCreationForm):

    USER_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    user_type = forms.ChoiceField(choices=[USER_CHOICES], required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'user_type')