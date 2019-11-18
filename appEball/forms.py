from django import forms
from .models import CustomUser , Tournament
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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



class EditProfileForm(UserChangeForm):

    class Meta:
        model= CustomUser
        fields=( 'username',
            'email',
            'ccNumber',
            'phoneNumber',
            )


class TournamentCreationForm(forms.ModelForm):
    
    class Meta:
        model = Tournament
        fields = (
            'name',
            'maxTeams',
            'beginDate',
            'endDate',
        )
