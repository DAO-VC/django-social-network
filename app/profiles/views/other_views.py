from rest_framework import generics

from profiles.models.other_models import Industries, BusinessType, SaleRegions
from profiles.serializers.others_serializers import (
    IndustriesSerializer,
    BusinessTypeSerializer,
    SaleRegionSerializer,
)


class IndustriesListView(generics.ListAPIView):
    """Список всех индустрий"""

    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    pagination_class = None


class BusinessTypeListView(generics.ListAPIView):
    """Список всех бизнес-типов"""

    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer


class RegionsListView(generics.ListAPIView):
    """Список всех регионов"""

    queryset = SaleRegions.objects.all()
    serializer_class = SaleRegionSerializer
