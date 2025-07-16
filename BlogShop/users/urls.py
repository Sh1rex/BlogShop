from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('register', views.register, name='register'),
    path('profile/', include([
        path('', views.own_profile, name='own_profile'),
        path('<slug:slug>/', include([
            path('', views.profile, name='profile'),
            path('subscribers/', views.subscribers, name='subscribers'),
            path('subscribed/', views.subscribed, name='subscribed'),
        ])),
    ]))
]
