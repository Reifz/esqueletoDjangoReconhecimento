from django import forms
from .models import Usuario

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        min_length=8,
        error_messages={
            "min_length": "A senha deve ter pelo menos 8 caracteres."
        })

    class Meta:
        model = Usuario
        fields = ['name', 'email', 'password', 'photo']
