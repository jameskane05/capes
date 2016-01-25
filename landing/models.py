from django.db import models
from datetime import *
import uuid
import string
import random
from datetime import timedelta



def link_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_exp_date():
    today = datetime.today()
    exp_date = today + timedelta(days=7)
    return exp_date


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    notes = models.TextField(blank=True)
    link = models.CharField(max_length=254)
    exp_date = models.DateTimeField(default=get_exp_date)
    created = models.DateTimeField(auto_now_add=True)  # added only on creation
    updated = models.DateTimeField(auto_now=True)  # updates each time the object is saved


"""
class ActivityLog(models.Model):
    client = models.IntegerField()
    type = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)  # added only on creation"""