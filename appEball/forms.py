from django import forms
from .models import CustomUser , Tournament, Team
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
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
        )



class EditProfileForm(UserChangeForm):

    class Meta:
        model= CustomUser
        fields=( 'firstName',
            'lastName',
            'username',
            'email',
            'ccNumber',
            'phoneNumber',
            'profileImg',
            )

class TournamentCreationForm(forms.ModelForm):
    week=(('Sun','Sun'),('Mon','Mon'),('Tue','Tue'),('Wed','Wed'),('Thu','Thu'),('Fri','Fri'),('Sat','Sat'))
    class Meta:
        model = Tournament
        fields = (
            'name',
            'maxTeams',
            'beginDate',
            'endDate',
            'gameDays',
        )



class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'name',
            'tactic',
            'tournament',
        )