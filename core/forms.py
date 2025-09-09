from django import forms
from .models import Usuario

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = Usuario
        fields = ['name', 'email', 'password', 'photo']
