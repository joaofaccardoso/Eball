from django import forms
from .models import CustomUser , Tournament, Team, TournamentDays, Reserve, Player
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

class TeamCreationForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = (
            'name',
            'tactic',
            'tournament',
        )




class TournamentDaysForm(forms.ModelForm):
    week=((0,'Sun'),(1,'Mon'),(2,'Tue'),(3,'Wed'),(4,'Thu'),(5,'Fri'),(6,'Sat'))

    class Meta:
        model = TournamentDays
        fields = (
            'name',
            'maxTeams',
            'beginDate',
        )


class ReserveForm(forms.ModelForm):

    class Meta:
        model = Reserve
        fields = (
            
        )


class SubForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = (
            'subGames',
        )