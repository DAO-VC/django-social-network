from rest_framework import permissions

from articles.models import Article


class ArticlePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Article):
        if obj.company_id.owner.id != request.user.id:
            return False
        return True
