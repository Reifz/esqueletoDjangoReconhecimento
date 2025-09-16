from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
class Usuario(models.Model):
    ACCESS_LEVEL_1 = '1'
    ACCESS_LEVEL_2 = '2'
    ACCESS_LEVEL_3 = '3'

    ACCESS_LEVEL_OPTIONS = [
        (ACCESS_LEVEL_1, 'Usuário'),
        (ACCESS_LEVEL_2, 'Diretor'),
        (ACCESS_LEVEL_3, 'Ministro')
    ]

    photo  = models.ImageField(upload_to='photo')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    nivel_acesso = models.CharField(max_length=1, choices=ACCESS_LEVEL_OPTIONS, default=ACCESS_LEVEL_1)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
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