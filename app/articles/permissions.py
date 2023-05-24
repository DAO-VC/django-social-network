from django.db.models import Q
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from articles.models import Article
from profiles.models import Startup
from vacancy.models import WorkTeam


class ArticlePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        obj = Article.objects.filter(id=view.kwargs["pk"]).first()
        try:
            startup: Startup = Startup.objects.get(owner=obj.company_id.owner)

        except AttributeError:
            raise NotFound("Object don't exist")

        if obj.company_id.owner.id == request.user.id:
            return True
        if request.user.id in [
            item.candidate_id.professional_id.owner.id
            for item in startup.work_team.all()
        ]:
            work_obj: WorkTeam = startup.work_team.filter(
                candidate_id__professional_id__owner_id=request.user.id
            ).first()
            if work_obj.articles_and_news_management:
                return True
        return False


class ArticleBasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        startup = Startup.objects.filter(
            Q(work_team__candidate_id__professional_id__owner__in=[request.user.id])
            | Q(owner=request.user.id)
        ).first()
        if not startup:
            raise NotFound("Object don't exist")
        if request.method == "POST":
            if startup.owner.id == request.user.id:
                return True
            if request.user.id in [
                item.candidate_id.professional_id.owner.id
                for item in startup.work_team.all()
            ]:
                work_obj: WorkTeam = startup.work_team.filter(
                    candidate_id__professional_id__owner_id=request.user.id
                ).first()
                if work_obj.articles_and_news_management:
                    return True
            return False

        if request.method == "GET":
            return True
