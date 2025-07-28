from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreatePostForm, ConfigPostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
        form = CreatePostForm(request.POST)
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
    form = ConfigPostForm(requset.POST, instance=post)
    if form.is_valid():
        form.save()
    return redirect('blog:postsconfig')