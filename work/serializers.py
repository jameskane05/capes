from rest_framework import serializers
from work.models import Work


__author__ = 'James Kane'


class WorkSerializer(serializers.ModelSerializer):


    class Meta:

        model = Work
        fields = ('id', 'name', 'tags', 'image', 'notes', 'created', 'updated')
