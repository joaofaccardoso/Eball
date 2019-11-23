from django.urls import path
from . import views
app_name = 'appEball'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),

    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', views.edit_user_profile.as_view(), name='editUserProfile'),
    
    path('help/', views.help, name='help'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('is_seen/<int:pk>/', views.is_seen, name='is_seen'),    
    
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),

    path('teams_list/', views.teams_list.as_view(), name='teams_list'),
    path('join_team/<int:teamId>',views.JoinTeam.as_view(), name='join_team'),
    path('delete_team/<int:pk>', views.delete_team, name='delete_team'),

    path('tournaments/', views.tournaments.as_view(), name='tournaments'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
    path('tournament_info/', views.tournament_info, name='tournament_info'),
    path('tournament_teams/', views.tournament_teams, name='tournament_teams'),
    path('delete_tournament/<int:pk>', views.delete_tournament, name='delete_tournament'),
    
    path('askSub/', views.askSub, name='askSub'),
    path('askKick/', views.askKick, name='askKick'),
]
