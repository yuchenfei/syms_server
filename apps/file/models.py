from django.db import models


class File(models.Model):
    name = models.CharField(max_length=50, unique=True)
    describe = models.CharField(max_length=255)
    file = models.FileField(upload_to='file')
