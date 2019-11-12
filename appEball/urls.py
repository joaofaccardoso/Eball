from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('navbar/', views.navbar, name='navbar'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('teams_list/', views.teams_list, name='teams_list'),
]