from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from link_shortener.settings import MAX_CODE_LENGTH


# Create your models here.
class ShortenedLink(models.Model):
    full_url = models.CharField(max_length=150, blank=False, null=False)
    identifier = models.CharField(
        max_length=MAX_CODE_LENGTH, blank=False, null=False, unique=True
    )
    last_use = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ShortenedLink {self.full_url} -> {self.identifier}"

    def update_last_use(self):
        self.last_use = timezone.now()
        self.save()
