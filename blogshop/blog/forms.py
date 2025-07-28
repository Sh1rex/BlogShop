from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'seller', 'slug', 'avaible']

class ConfigPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'seller', 'slug']
