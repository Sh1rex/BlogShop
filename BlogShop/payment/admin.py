from django.contrib import admin
from .models import Balance, BalanceTransaction, BuyProductTransaction

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

@admin.register(BalanceTransaction)
class TopUpBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'paid', 'created']
    list_filter = ['paid', 'created']

@admin.register(BuyProductTransaction)
class BuyProductTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

