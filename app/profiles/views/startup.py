from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import StartupCreatePermission
from profiles.models.startup import Startup
from profiles.permissions import OnboardingPermission, UpdateStartupPermission
from profiles.serializers.startup import (
    StartupBaseSerializer,
    StartupSerializer,
    StartupUpdateSerializer,
)


class StartUpCreateView(generics.CreateAPIView):
    """Онбоардинг стартап"""

    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer
    permission_classes = (
        IsAuthenticated,
        StartupCreatePermission,
        OnboardingPermission,
    )


class StartUpUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | Изменение стартапа"""

    http_method_names = ["get", "put"]
    permission_classes = (
        IsAuthenticated,
        UpdateStartupPermission,
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StartupSerializer
        return StartupUpdateSerializer

    def get_object(self):
        obj = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(owner=self.request.user.id)
        ).first()
        self.check_object_permissions(self.request, obj)
        return obj


class AllStartupListView(generics.ListAPIView):
    """Список всех стартапов сайта"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer


class AllStartupRetrieveView(generics.RetrieveAPIView):
    """Детальное получение стартапа"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
