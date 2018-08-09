from django.db import models

from experiment.models import Item


class Thinking(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.TextField()
    picture = models.ImageField(blank=True, upload_to='thinking')
