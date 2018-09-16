from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics

from core.serializers import UserSerializer
from core.models import User, Topic, Comment


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


# Create your views here.
