from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category

def recommendations(request, category_slug=None):
    category = None
    posts = Post.objects.filter(avaible=True).order_by('-created')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    return render(request, 'mainpage/recommendations.html', {
        'category': category,
        'posts': posts,
    })
