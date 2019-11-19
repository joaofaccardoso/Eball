from django.urls import path
from . import views
from .views import UserRegister, UserLogin, HomePage,edit_user_profile, new_tournament, new_team

app_name = 'appEball'

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('new_team/', new_team.as_view(), name='new_team'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/new/', new_tournament.as_view(), name='new_tournament'),
    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', edit_user_profile.as_view(), name='editUserProfile'),
    path('help/', views.help, name='help'),
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
]
