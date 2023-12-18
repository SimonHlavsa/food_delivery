from django import forms
from .models import UserProfile
        
class CustomerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or  not password2 or password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter matching passwords.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            password = self.cleaned_data.get('password1')
            user.set_password(password) 
            user.save()
        return user


class RestaurantCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'restaurant_name')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter matching passwords.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            password = self.cleaned_data.get('password1')
            user.set_password(password)  
            user.save()
        return user
        

