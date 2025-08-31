from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created', 'updated', 'seller', 'slug', 'avaible']

class ConfigPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['created', 'updated', 'seller', 'slug']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['category', 'stars', 'text']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={"cols": "30", "rows": "5"})
        }
