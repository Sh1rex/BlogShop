from django.urls import path
from . import views
from . import webhooks

app_name = 'payment'

urlpatterns = [
    path('topupbalance/', views.balancetransactioncheckoutsession, name='topupbalance'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path("purchaseproduct/<int:id>/", views.purchaseproduct, name="purchaseproduct"),
    path('confirmpurchase/<int:id>/', views.confirmpurchase, name='confirmpurchase'),
    path("orders/", views.orders, name="orders"),
    path("purchases/", views.purchases, name="purchases"),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
]