from django.db import models

from experiment.models import Experiment, Item
from info.models import User


class ExamSetting(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()


class Question(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.TextField()
    a = models.CharField(max_length=50, blank=True)
    b = models.CharField(max_length=50, blank=True)
    c = models.CharField(max_length=50, blank=True)
    d = models.CharField(max_length=50, blank=True)
    answer = models.CharField(max_length=1)
