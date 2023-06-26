from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from articles.filters import ArticleFilter
from articles.models import Article
from articles.permissions import (
    ArticlePermission,
    ArticleBasePermission,
    RetrieveArticlePermission,
)
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
    ArticleBaseSerializer,
    ArticleUpdateVisionSerializer,
)

from django.db.models import F, Q


class ArticleListCreateView(generics.ListCreateAPIView):
    """Список всех постов стартапа | создание поста"""

    permission_classes = (IsAuthenticated, ArticleBasePermission)
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    filterset_fields = ("company_id",)
    ordering_fields = ("created_at", "view_count")
    search_fields = ("name",)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleCreateSerializer

    def get_queryset(self):
        obj = Article.objects.filter(
            Q(
                company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(company_id__owner=self.request.user.id)
        )
        self.check_object_permissions(self.request, obj)
        return obj


# class ArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
#     """Изменение | удаление поста"""
#
#     queryset = Article.objects.all()
#     http_method_names = ["get", "put", "delete"]
#     permission_classes = (IsAuthenticated, ArticlePermission)
#
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return ArticleBaseSerializer
#         return ArticleUpdateSerializer


class ArticleParamView(generics.ListAPIView):
    """Список всех статей | Поиск по названию поста"""

    serializer_class = ArticleBaseSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    filterset_fields = ("company_id",)
    ordering_fields = ("created_at", "view_count")
    search_fields = ("name",)

    def get_queryset(self):
        return Article.objects.filter(is_visible=True)


# class ArticleVisibleView(generics.UpdateAPIView):
#     """Обновление видимости статьи стартапом"""
#
#     serializer_class = ArticleUpdateVisionSerializer
#     http_method_names = ["put"]
#     permission_classes = (IsAuthenticated, ArticlePermission)
#
#     def get_queryset(self):
#         return Article.objects.filter(
#             Q(
#                 company_id__work_team__candidate_id__professional_id__owner__in=[
#                     self.request.user.id
#                 ]
#             )
#             | Q(company_id__owner=self.request.user.id)
#         )


class AllArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Список всех статей по id"""

    queryset = Article.objects.all()
    filterset_class = ArticleFilter
    permission_classes = (RetrieveArticlePermission,)
    http_method_names = ["get", "put", "delete"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance: Article = self.get_object()
        instance.view_count = F("view_count") + 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class StartupAllArticles(generics.ListAPIView):
    """Список всех статей стартапа по id"""

    serializer_class = ArticleBaseSerializer

    # permission_classes = (IsAuthenticated, VacancyGetCreatePermission)
    # TODO: решить пермишены
    def get_queryset(self):
        return Article.objects.filter(company_id=self.kwargs["pk"])


class ArticleVisibleView(generics.UpdateAPIView):
    """Обновление видимости статьи стартапом"""

    queryset = Article.objects.all()
    serializer_class = ArticleUpdateVisionSerializer
    http_method_names = ["put"]
    permission_classes = (RetrieveArticlePermission,)


# class AllArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
#     """Список всех статей по id"""
#
#     queryset = Article.objects.all()
#     filterset_class = ArticleFilter
#     permission_classes = (RetrieveArticlePermission,)
#     http_method_names = ["get", "put", "delete"]
#
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return ArticleBaseSerializer
#         return ArticleUpdateSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance: Article = self.get_object()
#         instance.view_count = F("view_count") + 1
#         instance.save()
#         return super().retrieve(request, *args, **kwargs)
