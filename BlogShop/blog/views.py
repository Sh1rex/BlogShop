from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, ConfigPostForm
from .models import Post, SelectedPosts, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import Profile
from django.utils.text import slugify
from users.views import check_is_subscribed
from django.urls import reverse
from django.db.models import Avg

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
def editpost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = ConfigPostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.slug = slugify(post.product)
        post.save()
    return redirect('blog:postsconfig')

def postdetail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    profile = get_object_or_404(Profile, user=post.seller)
    is_subscribed = check_is_subscribed(request.user, profile.user)
    comments = Comment.objects.filter(receiver=profile.user)
    avg = comments.aggregate(avg=Avg('stars'))['avg']
    if SelectedPosts.objects.filter(user=request.user, post=post):
        if_selected = False
    else:
        if_selected = True
    return render(request, 'blog/postdetail.html', {
        'post': post,
        'profile': profile,
        'is_subscribed': is_subscribed,
        'avg': avg,
        'if_selected': if_selected,
    })

@login_required
@require_POST
def postdelete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog:postsconfig')

@login_required
def postselect(request, id):
    post = get_object_or_404(Post, id=id)
    SelectedPosts.objects.create(post=post, user=request.user)
    return redirect(reverse('blog:postdetail', args=[post.id, post.slug]))

@require_POST
@login_required
def postunselect(request, id):
    post = get_object_or_404(Post, id=id)
    selectedpost = get_object_or_404(SelectedPosts, post=post, user=request.user)
    selectedpost.delete()
    return redirect('blog:postsselected')

@login_required
def postsselected(request):
    posts = SelectedPosts.objects.filter(user=request.user)
    return render(request, 'blog/postsselected.html', {
        'posts': posts,
    })
