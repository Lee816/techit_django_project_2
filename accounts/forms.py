import unicodedata
from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm
from django.contrib.auth import get_user_model

# 회원가입 폼
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone','username','email','password']
        widgets = {
        'email': forms.EmailInput(attrs={
            'class' : 'inputform',
            }),
        'password': forms.PasswordInput(attrs={
            'class' : 'inputform',
            }),
        'username': forms.TextInput(attrs={
            'class' : 'inputform',
            }),
        'phone': forms.TextInput(attrs={
            'class' : 'inputform',
            }),
    }

# 유저정보 변경 폼
class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['email', 'username','phone']
        widgets = {
        'email': forms.EmailInput(attrs={
            'class' : 'inputform',
            }),
        'username': forms.TextInput(attrs={
            'class' : 'inputform',
            }),
        'phone': forms.TextInput(attrs={
            'class' : 'inputform',
            }),
        }

# 로그인 폼
class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )