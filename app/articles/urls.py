from django.urls import path
from django.views.decorators.cache import cache_page

from articles.views import (
    ArticleListCreateView,
    ArticleParamView,
    ArticleVisibleView,
    AllArticleRetrieveView,
    StartupAllArticles,
)

urlpatterns = [
    path(
        "main/articles/",
        cache_page(20)(ArticleListCreateView.as_view()),
        name="list_create_article",
    ),
    path(
        "common/articles/",
        cache_page(20)(ArticleParamView.as_view()),
        name="all_articles",
    ),
    path(
        "common/articles/<int:pk>/",
        cache_page(20)(AllArticleRetrieveView.as_view()),
        name="retrieve_all_articles",
    ),
    path(
        "common/startup/<int:pk>/articles/",
        StartupAllArticles.as_view(),
        name="all_articles_to_startup_id",
    ),
    path(
        "common/articles/<int:pk>/visible/",
        ArticleVisibleView.as_view(),
        name="change_visible_article",
    ),
]
