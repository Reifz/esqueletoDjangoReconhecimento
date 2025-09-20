from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="@dmin123"
        )

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)