from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.permissions import UserIsOnboarding
from network.models import Network
from network.permissions import NetworkOwnerPermission
from network.serializers import (
    CreateMyNetworkSerializer,
    NetworkBaseSerializer,
    UpdateNetworkSerializer,
    MyNetworkChangeStatusSerializer,
)


class CreateMyNetwork(generics.CreateAPIView):
    queryset = Network.objects.all()
    serializer_class = CreateMyNetworkSerializer
    permission_classes = (IsAuthenticated, UserIsOnboarding)


class ListMyNetwork(generics.ListAPIView):
    serializer_class = NetworkBaseSerializer
    permission_classes = (
        IsAuthenticated,
        NetworkOwnerPermission,
    )

    def get_queryset(self):
        return Network.objects.filter(owner=self.request.user)


class UpdateDeleteMyNetwork(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateNetworkSerializer
    permission_classes = (
        IsAuthenticated,
        NetworkOwnerPermission,
    )
    http_method_names = ["put", "delete"]

    def get_object(self):
        return get_object_or_404(Network, owner=self.request.user)


class MyNetworkChangeStatus(generics.UpdateAPIView):
    serializer_class = MyNetworkChangeStatusSerializer
    http_method_names = [
        "put",
    ]
    permission_classes = (
        IsAuthenticated,
        NetworkOwnerPermission,
    )

    def get_object(self):
        return get_object_or_404(Network, owner=self.request.user)
