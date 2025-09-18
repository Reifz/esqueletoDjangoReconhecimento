from django.contrib import admin
from .models import Usuario, LogAcesso 

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "nivel_acesso")
    search_fields = ("name", "email")
    list_filter = ("nivel_acesso",)

@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "result", "date_time")
    list_filter = ("result", "date_time")
    search_fields = ("usuario_name", "usuario_email")