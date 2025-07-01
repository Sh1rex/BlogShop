from django.shortcuts import render, redirect
from .forms import UserCreationForm

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
        return render(request, 'users/profile.html')
    return redirect('login')