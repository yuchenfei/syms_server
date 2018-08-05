from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Classes(models.Model):
    name = models.CharField(max_length=30)
