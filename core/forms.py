from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 8 caracteres'}),
        min_length=8,
        error_messages={
            "min_length": "A senha deve ter pelo menos 8 caracteres.",
            "required": "A senha é obrigatória."
        }
    )

    class Meta:
        model = Usuario
        fields = ['name', 'email', 'password', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
            'name': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise ValidationError("A foto é obrigatória.")
        return photo

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Deixe em branco para manter a senha atual'}),
        required=False,
        min_length=8,
        error_messages={"min_length": "A senha deve ter pelo menos 8 caracteres."}
    )

    class Meta:
        model = Usuario
        fields = ['name', 'email', 'password', 'photo']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se outro usuário já usa este email (excluindo o usuário atual)
        if Usuario.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("Este email já está em uso por outro usuário.")
        return email

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo and not self.instance.photo:
            raise ValidationError("A foto é obrigatória.")
        return photo

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user