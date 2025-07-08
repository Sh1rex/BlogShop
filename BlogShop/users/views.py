from django.shortcuts import render, redirect
from .forms import UserCreationForm, ProfileForm

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

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile = request.user.profile
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
        return render(request, 'users/profile.html')
    return redirect('login')

def settings(request):
    if request.user.is_authenticated:
        form = ProfileForm()
        return render(request, 'settings.html', {
            'form': form,
        })
    return redirect('login')
