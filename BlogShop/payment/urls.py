from django.urls import path
from . import views
from . import webhooks

app_name = 'payment'

urlpatterns = [
    path('topupbalance/', views.topupbalanceview, name='topupbalance'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]