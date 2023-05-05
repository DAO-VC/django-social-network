from django.shortcuts import render
from rest_framework import generics

from profiles.models import Startup, Professional, Investor
from profiles.serializers import (
    StartupBaseSerializer,
    ProfessionalBaseSerializer,
    InvestorBaseSerializer,
    StartupUpdateSerializer,
    ProfessionalUpdateSerializer,
    InvestorUpdateSerializer,
)


class StartUpCreateView(generics.CreateAPIView):
    """Онбоардинг стартап"""

    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer


class ProfessionalCreateView(generics.CreateAPIView):
    """Онбоардинг профессионал"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalBaseSerializer


class InvestorCreateView(generics.CreateAPIView):
    """Онбоардинг инвестор"""

    queryset = Investor.objects.all()
    serializer_class = InvestorBaseSerializer


# class StartListCreateView(generics.ListCreateAPIView):
#     """Создание стартапа"""
#     queryset = Startup.objects.all()
#     serializer_class = StartupBaseSerializer


class StartUpUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение стартапа"""

    queryset = Startup.objects.all()
    serializer_class = StartupUpdateSerializer
    http_method_names = ["put"]

    def get_object(self):
        obj = Professional.objects.filter(owner__id=self.request.user.id).first()
        return obj


class ProfessionalUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение профессионала"""

    serializer_class = ProfessionalUpdateSerializer
    http_method_names = [
        "put",
    ]

    def get_object(self):
        obj = Professional.objects.filter(owner__id=self.request.user.id).first()
        return obj


class InvestorUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение инвестора"""

    serializer_class = InvestorUpdateSerializer
    http_method_names = [
        "put",
    ]

    def get_object(self):
        obj = Professional.objects.filter(owner__id=self.request.user.id).first()
        return obj
