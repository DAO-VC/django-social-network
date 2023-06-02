from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.permissions import ProfessionalCreatePermission, UpdatePermission
from profiles.models.professional import Professional
from profiles.permissions import OnboardingPermission
from profiles.serializers.professional import (
    ProfessionalBaseSerializer,
    ProfessionalUpdateSerializer,
    ProfessionalSerializer,
)


class ProfessionalCreateView(generics.CreateAPIView):
    """Онбоардинг профессионал"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalBaseSerializer
    permission_classes = (
        IsAuthenticated,
        ProfessionalCreatePermission,
        OnboardingPermission,
    )


class ProfessionalUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение профессионала"""

    serializer_class = ProfessionalUpdateSerializer
    http_method_names = [
        "get",
        "put",
    ]
    permission_classes = (IsAuthenticated, UpdatePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfessionalSerializer
        return ProfessionalUpdateSerializer

    def get_object(self):
        obj = Professional.objects.filter(owner__id=self.request.user.id).first()
        return obj


class AllProfessionalsListView(generics.ListAPIView):
    """Список всех профессионалов сайта"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


class AllProfessionalRetrieveView(generics.RetrieveAPIView):
    """Детальное получение профессионалов"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
