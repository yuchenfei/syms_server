from django.db import models

from info.models import Course


class Item(models.Model):
    name = models.CharField(max_length=50)


class Experiment(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    describe = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('item', 'course')
