from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.models.signals import post_save

        User = get_user_model()

        def promote_to_superuser(sender, instance, created, **kwargs):
            if created and instance.email == "admin@gmail.com" and instance.photo:
                instance.is_superuser = True
                instance.is_staff = True
                instance.nivel_acesso = '2'
                instance.save()
                print(f"Usuário {instance.email} promovido a superuser.")

        post_save.connect(promote_to_superuser, sender=User)
