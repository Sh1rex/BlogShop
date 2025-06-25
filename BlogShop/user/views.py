from django.shortcuts import render
from .forms import RegCreateForm

def registration(request):
    form = RegCreateForm()
    return render(request, 'user/authentication/registration.html', {
        'form': form,
    })

def login(request):
    return render(request, 'user/authentication/login.html', {})