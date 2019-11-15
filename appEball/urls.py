from django.urls import path
from . import views

app_name = 'appEball'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('navbar/', views.navbar, name='navbar'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
