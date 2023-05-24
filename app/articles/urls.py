from django.urls import path

from articles.views import (
    ArticleListCreateView,
    ArticleRetrieveView,
    ArticleParamView,
    ArticleVisibleView,
    AllArticleRetrieveView,
)

urlpatterns = [
    path("main/articles/", ArticleListCreateView.as_view(), name="list_create_article"),
    path("common/articles/", ArticleParamView.as_view(), name="all_articles"),
    path(
        "common/articles/<int:pk>",
        AllArticleRetrieveView.as_view(),
        name="retrieve_all_articles",
    ),
    path(
        "main/articles/<int:pk>",
        ArticleRetrieveView.as_view(),
        name="retrieve_article",
    ),
    path(
        "main/articles/<int:pk>/visible",
        ArticleVisibleView.as_view(),
        name="change_visible_article",
    ),
]
