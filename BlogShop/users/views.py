from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, ProfileForm
from .models import Profile
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
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
    return render(request, 'users/profile.html',{
        'profile': profile
    })

def settings(request):
    if request.user.is_authenticated:
        form = ProfileForm()
        return render(request, 'settings.html', {
            'form': form,
        })
    return redirect('login')
