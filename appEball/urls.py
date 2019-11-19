from django.urls import path
from . import views

app_name = 'appEball'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', views.edit_user_profile.as_view(), name='editUserProfile'),
    path('help/', views.help, name='help'),
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
    path('notifications/', views.notifications, name='notifications'),
    path('is_seen/<int:pk>/', views.is_seen, name='is_seen'),    
]
