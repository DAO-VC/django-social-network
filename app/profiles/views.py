from django.shortcuts import render
from rest_framework import generics

from profiles.models import Startup, Professional
from profiles.serializers import StartupBaseSerializer, ProfessionalBaseSerializer


class StartUpCreateView(generics.CreateAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer


class ProfessionalCreateView(generics.CreateAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalBaseSerializer
