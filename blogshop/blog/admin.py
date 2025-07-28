from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'category', 'price', 'quantity', 'avaible', 'created', 'updated']
    list_filter = ['avaible', 'created', 'updated']