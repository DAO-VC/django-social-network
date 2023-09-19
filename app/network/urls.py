from django.urls import path

from network.views import (
    CreateMyNetwork,
    ListMyNetwork,
    UpdateDeleteMyNetwork,
    MyNetworkChangeStatus,
)

urlpatterns = [
    path("create_network/", CreateMyNetwork.as_view(), name="create_new_network"),
    path("my_network/", ListMyNetwork.as_view(), name="my_network"),
    path(
        "update_my_network/", UpdateDeleteMyNetwork.as_view(), name="update_my_network"
    ),
    path(
        "change_status_my_network/",
        MyNetworkChangeStatus.as_view(),
        name="change_status_my_network",
    ),
]
