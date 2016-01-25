from rest_framework import serializers
from landing.models import Client
from urllib import *
import string
import random
from datetime import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

__author__ = 'James Kane'


def link_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_exp_date():
    return datetime.today() + timedelta(days=7)


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ('username','password')


class ClientSerializer(serializers.ModelSerializer):
    permission_classes = IsAuthenticated

    class Meta:

        model = Client
        fields = ('id', 'name', 'email', 'notes', 'link', 'exp_date', 'created', 'updated')
        extra_kwargs = {
            'link': {
                'default': link_generator
            },
            'exp_date': {
                'default': get_exp_date,
            }
        }

