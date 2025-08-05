from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
    path('<slug:category_slug>/', views.recommendations, name='recommendations_by_category'),
]
