from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','seller','product', 'category', 'price', 'quantity', 'avaible', 'created', 'updated']
    list_filter = ['avaible', 'created', 'updated']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'receiver', 'category', 'stars']