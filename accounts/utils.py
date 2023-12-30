from django.contrib.auth.models import User


def get_or_create_guest():
    """Func that return guest User intance,
    creates it if isn't present in Users db"""
    guest_user = User.objects.filter(username="guest").first()
    if guest_user is None:
        guest_user = User.objects.create(
            username="guest",
            first_name="Guesto",
            last_name="Geustov",
            is_staff=True,
        )
    return guest_user
