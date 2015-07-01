from django import forms
from .models import *
from captcha.fields import CaptchaField
from django.forms.extras import SelectDateWidget

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    birthday = forms.DateField(widget=SelectDateWidget(years=range(2015,1900,-1)))

    class Meta:
        model = Guest
        fields = ['username', 'password', 'first_name', 'last_name', 'birthday', 'email', 'gender', 'avatar']

class ResetPass(forms.Form):
    email = forms.EmailField(max_length=100)