from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, ProfileForm
from .models import Profile, Subscription
from django.urls import reverse

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
    if request.user.is_authenticated:
        if profile.user == request.user:
            if request.method == 'POST':
                if not request.POST.get('Subscribe'):
                    form = ProfileForm(request.POST, request.FILES, instance=profile)
                    if form.is_valid():
                        form.save()
        else:
            if request.method == 'POST':
                if not Subscription.objects.filter(subscriber=request.user, subscribed_to=profile.user):
                    subscription = Subscription.objects.create(subscriber=request.user, subscribed_to=profile.user)
                    subscription.save()
    subscribers = Subscription.objects.filter(subscribed_to=profile.user).count()
    subscribed = Subscription.objects.filter(subscriber=profile.user).count()
    return render(request, 'users/mainprofile.html',{
        'subscribers': subscribers,
        'profile': profile,
        'subscribed': subscribed,
    })

def settings(request):
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'settings.html', {
            'form': form,
        })
    return redirect('login')
