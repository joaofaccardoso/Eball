from django.urls import path
from . import views
from .views import UserRegister, UserLogin, HomePage,edit_user_profile

app_name = 'appEball'

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('profile/<str:username>', views.user_profile, name='userProfile'),
    path('editprofile/<str:username>', edit_user_profile.as_view(), name='editUserProfile'),
    path('help/', views.help, name='help'),
    path('users/', views.users, name='users'),
    path('accept_user/<str:username>', views.accept_user, name='accept_user'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),
    path('is_tournament_manager/<str:username>', views.is_tournament_manager, name='is_tournament_manager'),
]
