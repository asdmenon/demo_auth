from django.db import models

# from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.


class CivilIdAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    civil_id = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.civil_id