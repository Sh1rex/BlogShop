from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, ConfigPostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import Profile
from django.utils.text import slugify
from users.views import check_is_subscribed

@login_required
def postsconfig(request):
    posts = Post.objects.filter(seller=request.user)
    forms = [ConfigPostForm(instance=post) for post in posts]
    return render(request,'blog/postsconfig.html', {
        'forms': forms,
    })

@login_required
def createpost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.seller = request.user
            post.save()
            return redirect('blog:postsconfig')
    form = CreatePostForm()
    return render(request, 'blog/createpost.html',{
        'form': form,
    })
    
@login_required
@require_POST
def editpost(requset, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = ConfigPostForm(requset.POST, requset.FILES, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.slug = slugify(post.product)
        post.save()
    return redirect('blog:postsconfig')

def postdetail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    profile = get_object_or_404(Profile, user=post.seller)
    is_subscribed = check_is_subscribed(request.user, profile.user)
    return render(request, 'blog/postdetail.html', {
        'post': post,
        'profile': profile,
        'is_subscribed': is_subscribed,
    })

@login_required
@require_POST
def postdelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog:postsconfig')

