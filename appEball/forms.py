from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'firstName',
            'lastName',
            'username',
            'email',
            'ccNumber',
            'phoneNumber',
            'password1',
            'password2',
        )

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
        )
