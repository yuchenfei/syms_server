from django.db import models

from info.models import Course, Student


class Item(models.Model):
    name = models.CharField(max_length=50)


class Experiment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    describe = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('item', 'course')


class Feedback(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    image1 = models.ImageField(blank=True, upload_to='feedback')
    image2 = models.ImageField(blank=True, upload_to='feedback')
    image3 = models.ImageField(blank=True, upload_to='feedback')
    image4 = models.ImageField(blank=True, upload_to='feedback')
    image5 = models.ImageField(blank=True, upload_to='feedback')
    thinking_id = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('experiment', 'student')


class Grade(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('experiment', 'student')
