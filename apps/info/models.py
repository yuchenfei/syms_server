from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Classes(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    term = models.CharField(max_length=50)
    status = models.BooleanField(default=False)


class Student(models.Model):
    xh = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=5)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
