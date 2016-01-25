from django.shortcuts import render, redirect
from landing.models import Client
from datetime import *
import logging
from work.models import Work
from work.serializers import WorkSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
import re


__author__ = 'James Kane'


def work_sample(request):
    split_req = re.split('[/]', request.get_full_path())
    link = split_req[2]
    try:
        # This .get method throws a DoesNotExist exception if no objects match the query
        client = Client.objects.get(link=link)
        logging.warning(client)
        if client:
            if datetime.today().isoformat() > client.exp_date.isoformat():
                return render(request, "work/worksamples.html", {'status': 2})
            return render(request, "work/worksamples.html",  {'status': 0})
    except ObjectDoesNotExist:
        return render(request, "work/worksamples.html", {'status': 1})


class WorkList(generics.ListCreateAPIView):
    parser_classes = (FormParser, MultiPartParser,)
    #  generics.ListCreateAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('List' and 'Create'):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleWork(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser,)
    #  generics.RetrieveUpdateDestoryAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('Get', 'Put' and 'Create'):

    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)