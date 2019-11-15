from django.urls import path
from . import views
from .views import UserRegister, UserLogin, HomePage

app_name = 'appEball'
    path('', HomePage.as_view(), name='home_page'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('teams_list/', views.teams_list, name='teams_list'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
