from django.shortcuts import render
from rest_framework import generics

from profiles.models import Startup
from profiles.serializers import StartupBaseSerializer


class StartUpCreateView(generics.CreateAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer
