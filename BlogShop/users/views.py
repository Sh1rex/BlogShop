from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ProfileForm
from .models import Profile, Subscription
from django.urls import reverse
from blog.models import Post

def check_is_subscribed(subscriber, subscribed_to):
    if Subscription.objects.filter(subscriber=subscriber, subscribed_to=subscribed_to):
        return True
    return False
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {
        'form': form,
    })

def own_profile(request):
    return redirect(reverse('users:profile', args=[request.user.profile.slug]))
             
def profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    posts = Post.objects.filter(avaible=True, seller=profile.user)
    is_subscribed = check_is_subscribed(request.user, profile.user)
    if request.user.is_authenticated:
        if profile.user == request.user:
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
    return render(request, 'users/profile/mainprofile.html', {
        'profile': profile,
        'posts': posts,
        'is_subscribed': is_subscribed,
    })

def settings(request):
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'settings.html', {
            'form': form,
        })
    return redirect('login')

def subscribers(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    is_subscribed = check_is_subscribed(request.user, profile.user)
    return render(request, 'users/profile/profilesubscribers.html', {
        'profile': profile,
        'is_subscribed': is_subscribed,
    })

def subscribed(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    is_subscribed = check_is_subscribed(request.user, profile.user)
    return render(request, 'users/profile/profilesubscribed.html', {
        'profile': profile,
        'is_subscribed': is_subscribed,
    })

@require_POST
@login_required
def subscribe(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if not Subscription.objects.filter(subscriber=request.user, subscribed_to=profile.user):
        subscription = Subscription.objects.create(subscriber=request.user, subscribed_to=profile.user)
        subscription.save()
    else:
        subscription = get_object_or_404(Subscription, subscriber=request.user, subscribed_to=profile.user)
        subscription.delete()
    return redirect(reverse('users:profile', args=[profile.slug]))