from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

        
class UserProfileCreationForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type')

class UserProfileChangeForm(UserChangeForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name') # Nebo explicitně uveďte pole, která chcete změnit

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return password
        else:
            return self.initial["password"]