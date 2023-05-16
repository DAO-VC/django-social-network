from django.urls import path
from image.views import ImageViewSet, FilesViewSet

image_list = ImageViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

image_detail = ImageViewSet.as_view({"get": "retrieve", "delete": "destroy"})

file_list = FilesViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

file_detail = FilesViewSet.as_view({"get": "retrieve", "delete": "destroy"})
urlpatterns = [
    path("images/", image_list, name="image_list"),
    path("images/<int:pk>/", image_detail, name="image_detail"),
    path("documents/", file_list, name="file_list"),
    path("documents/<int:pk>/", file_detail, name="file_detail"),
]
