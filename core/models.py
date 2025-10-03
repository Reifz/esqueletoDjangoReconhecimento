from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')
        
        return self.create_user(email, name, password, **extra_fields)
class Usuario(AbstractUser):
    ACCESS_LEVEL_1 = '1'
    ACCESS_LEVEL_2 = '2'
    ACCESS_LEVEL_3 = '3'

    ACCESS_LEVEL_OPTIONS = [
        (ACCESS_LEVEL_1, 'Usuário'),
        (ACCESS_LEVEL_2, 'Diretor'),
        (ACCESS_LEVEL_3, 'Ministro')
    ]

    #campos do abstract user que não serão usados
    username = None
    first_name = None
    last_name = None

    #campos adicionais 
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photo')
    nivel_acesso = models.CharField(max_length=1, choices=ACCESS_LEVEL_OPTIONS, default=ACCESS_LEVEL_1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UsuarioManager()

    def __str__(self):
        return self.email


class LogAcesso(models.Model):
    RESULT_APPROVED = 'A'
    RESULT_DENIED = 'N'

    RESULT_OPTIONS = [
        (RESULT_APPROVED, 'Aprovado'),
        (RESULT_DENIED, 'Negado')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    result = models.CharField(max_length=1, choices=RESULT_OPTIONS, default=RESULT_DENIED)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.get_result_display()} - {self.date_time}"
