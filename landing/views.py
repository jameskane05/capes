from django.shortcuts import render, redirect
from landing.models import Client
from django.core.mail import send_mail
from landing.serializers import ClientSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import logging
from rest_framework import generics
from django.template.loader import render_to_string
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from landing.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import AuthenticationFailed

__author__ = 'James'


@permission_classes((IsAuthenticated, ))
def capes(request):
    if request.user.is_authenticated():
        return render(request, "landing/index.html")
    else: return render(request, "landing/login.html")

def link_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserList(generics.ListCreateAPIView):
    #  generics.ListCreateAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('List' and 'Create'):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except AuthenticationFailed:
            redirect('/')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleUser(generics.RetrieveUpdateDestroyAPIView):
    #  generics.RetrieveUpdateDestoryAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('Get', 'Put' and 'Create'):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClientList(generics.ListCreateAPIView):
    #  generics.ListCreateAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('List' and 'Create'):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleClient(generics.RetrieveUpdateDestroyAPIView):
    #  generics.RetrieveUpdateDestoryAPIView is an abbreviation of mixin code
    #  for standard API CRUD processes ('Get', 'Put' and 'Create'):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@csrf_exempt
def email_client(request):
    logging.warning(request)
    id = request.POST.get('id')
    email_subject = request.POST.get('email_subject')
    custom_email_text = request.POST.get('custom_email_text')
    client = Client.objects.get(id=id)
    msg_html = render_to_string('landing/email.html', {'client': client, 'custom_email_text': custom_email_text})
    send_mail(email_subject, '', 'jp@lelander.com', [client.email], html_message=msg_html, fail_silently=False)
    return redirect('/')