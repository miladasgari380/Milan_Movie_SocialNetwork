from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Guest
        fields = ['username', 'password', 'first_name', 'last_name', 'birthday', 'email', 'gender']