from django.db import models

from experiment.models import Experiment
from info.models import User


class ExamSetting(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()
