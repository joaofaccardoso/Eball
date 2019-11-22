from django.urls import path
from . import views
from .views import UserRegister, UserLogin, HomePage,edit_user_profile, new_tournament, new_team, teams_list,criar_player

app_name = 'appEball'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),

    path('teams_list/', teams_list.as_view(), name='teams_list'),
    path('new_team/', new_team.as_view(), name='new_team'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/new/', new_tournament.as_view(), name='new_tournament'),
    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', views.edit_user_profile.as_view(), name='editUserProfile'),
    
    path('help/', views.help, name='help'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('is_seen/<int:pk>/', views.is_seen, name='is_seen'),    
    
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),


    path('my_teams/', views.my_teams, name='my_teams'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
    path('tournament_info/', views.tournament_info, name='tournament_info'),
    path('tournament_teams/', views.tournament_teams, name='tournament_teams'),
    
    path('delete_team/<int:pk>', views.delete_team, name='delete_team'),
    
    
    path('askSub/', views.askSub, name='askSub'),
    path('askKick/', views.askKick, name='askKick'),
    path('criar_player',criar_player.as_view(),name='criar_player'),
]
