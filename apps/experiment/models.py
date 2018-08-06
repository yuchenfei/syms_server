from django.db import models

from info.models import Course


class Experiment(models.Model):
    name = models.CharField(max_length=50)
    describe = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('name', 'course')
