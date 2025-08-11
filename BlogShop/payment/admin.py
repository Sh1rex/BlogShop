from django.contrib import admin
from .models import Balance, BalanceTransiction

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

@admin.register(BalanceTransiction)
class TopUpBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'paid', 'created']
    list_filter = ['paid', 'created']
