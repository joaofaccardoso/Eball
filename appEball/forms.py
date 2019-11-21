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
        fields=( 'firstName',
            'lastName',
            'username',
            'email',
            'ccNumber',
            'phoneNumber',
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
    tacticChoice=(('4-3-3','4-3-3'),('4-4-2','4-4-2'),('4-2-3-1','4-2-3-1')) # ('4-1-2-1-2','4-1-2-1-2')
    class Meta:
        model = Team
        fields = (
            'name',
            'tactic'
        )