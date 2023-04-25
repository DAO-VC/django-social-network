from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image.views import BackgroundViewSet, LogoViewSet, FilesViewSet

image_list = BackgroundViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

image_detail = BackgroundViewSet.as_view({"get": "retrieve", "delete": "destroy"})

logo_list = LogoViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

logo_detail = LogoViewSet.as_view({"get": "retrieve", "delete": "destroy"})

file_list = FilesViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

file_detail = FilesViewSet.as_view({"get": "retrieve", "delete": "destroy"})
urlpatterns = [
    path("background/", image_list, name="image_list"),
    path("background/<int:pk>/", image_detail, name="image_detail"),
    path("logo/", logo_list, name="logo_list"),
    path("logo/<int:pk>/", logo_detail, name="logo_detail"),
    path("file/", file_list, name="file_list"),
    path("file/<int:pk>/", file_detail, name="file_detail"),
]
