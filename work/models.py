from django.db import models
from datetime import *


class Tag(models.Model):
    name = models.CharField(max_length=25, primary_key=True)


class Work(models.Model):
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    image = models.ImageField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)  # added only on creation
    updated = models.DateTimeField(auto_now=True)  # updates each time the object is saved
    tags = models.ManyToManyField(Tag)

