from django.urls import path

from articles.views import ArticleListCreateView, ArticleRetrieveView

urlpatterns = [
    path(
        "common/article/", ArticleListCreateView.as_view(), name="list_create_article"
    ),
    path(
        "common/article/<int:pk>",
        ArticleRetrieveView.as_view(),
        name="retrieve_article",
    ),
]
