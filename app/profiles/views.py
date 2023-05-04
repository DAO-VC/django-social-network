from django.shortcuts import render
from rest_framework import generics

from profiles.models import Startup, Professional, Investor
from profiles.serializers import (
    StartupBaseSerializer,
    ProfessionalBaseSerializer,
    InvestorBaseSerializer,
)


class StartUpCreateView(generics.CreateAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer


class ProfessionalCreateView(generics.CreateAPIView):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalBaseSerializer


class InvestorCreateView(generics.CreateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorBaseSerializer


class StartListCreateView(generics.ListCreateAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer


# class StartUpUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Startup.objects.all()
