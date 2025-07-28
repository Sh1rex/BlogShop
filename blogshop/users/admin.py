from django.contrib import admin
from .models import Profile, Subscription

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    llist_display = ['user', 'profileimg', 'slug']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'subscribed_to']