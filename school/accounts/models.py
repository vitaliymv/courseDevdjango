from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username