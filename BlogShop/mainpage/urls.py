from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.main_page, name='main_page')
]
