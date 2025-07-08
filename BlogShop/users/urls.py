from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.own_profile, name='own_profile'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings')
]
