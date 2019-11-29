from django.urls import path
from . import views
app_name = 'appEball'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/checkRegister/', views.checkRegister, name='check_register'),

    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', views.edit_user_profile.as_view(), name='editUserProfile'),
    
    path('help/', views.help, name='help'),
    
    path('notifications/', views.notifications, name='notifications'),
    path('is_seen/<int:pk>/', views.is_seen, name='is_seen'),    
    
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),

    path('teams_list/', views.teams_list.as_view(), name='teams_list'),
    path('team_info/<int:teamId>',views.TeamInfo.as_view(), name='team_info'),
    path('delete_team/<int:pk>', views.delete_team, name='delete_team'),
    path('teams_list/checkTeamName/', views.checkTeamName, name='check_team_name'),

    path('tournaments/', views.tournaments.as_view(), name='tournaments'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
    path('tournament_info/<int:pk>/<int:gRound>', views.tournament_info, name='tournament_info'),
    path('delete_tournament/<int:pk>', views.delete_tournament, name='delete_tournament'),
    path('tournaments/checkTournamentName/', views.checkTournamentName, name='check_tournament_name'),
    path('tournaments/checkDates/', views.checkDates, name='check_dates'),
    path('change_round/<int:pk>/<int:gRound>/<str:change>', views.change_round, name='change_round'),
    
    path('generate_games/<int:pk>', views.generate_games, name='generate_games'),
    
    path('askSub/', views.askSub, name='askSub'),
    path('askKick/', views.askKick, name='askKick'),
    path('notifications/', views.notifications, name='notifications'),
    path('is_seen/<int:pk>/', views.is_seen, name='is_seen'), 
    path('presencas/<int:pk>/',views.presencas.as_view(),name='presencas'),
    path('game/<int:pk>',views.game.as_view(),name='game'),
    path('manage_team/<int:pk>',views.manage_team.as_view(),name='manage_team'),
]
