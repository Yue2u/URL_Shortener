from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shortener"

    def ready(self):
        from django.contrib.auth.models import User

        import shortener.signals

        guest_user = User.objects.filter(username="guest").first()
        if guest_user is None:
            User.objects.create(
                username="guest",
                first_name="Guesto",
                last_name="Geustov",
                is_staff=True,
            )
