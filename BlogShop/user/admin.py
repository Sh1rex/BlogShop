from django.contrib import admin
from .models import Reg

@admin.register(Reg)
class RegAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'first_name', 'second_name', 'email']
