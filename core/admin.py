from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, LogAcesso


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'name', 'photo', 'nivel_acesso')


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('email', 'name', 'photo', 'nivel_acesso', 'is_active', 'is_staff', 'is_superuser')


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ('id', 'name', 'email', 'nivel_acesso', 'is_staff', 'is_superuser')
    search_fields = ('name', 'email')
    list_filter = ('nivel_acesso', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('name', 'photo', 'nivel_acesso')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'photo', 'nivel_acesso', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'result', 'date_time')
    list_filter = ('result', 'date_time')
    search_fields = ('usuario__name', 'usuario__email')  # <-- Corrigido
