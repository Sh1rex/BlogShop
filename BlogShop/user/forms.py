from django import forms
from .models import Reg

class RegCreateForm(forms.ModelForm):
    class Meta:
        model = Reg
        fields = ['nickname', 'first_name', 'second_name', 'email', 'password',]
        widgets = {
            'password': forms.PasswordInput(),
        }
    password_confirm = forms.CharField(widget=forms.PasswordInput())