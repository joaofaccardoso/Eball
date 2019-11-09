from django.urls import path
from . import views

app_name = 'appEball'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register/', views.register, name='register'),
    path('teams_list/', views.teams_list, name='teams_list'),
]