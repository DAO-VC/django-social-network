from rest_framework import serializers

from profiles.serializers.startup import StartupToArticleSerializer
from vacancy.models.workteam import WorkTeam
from vacancy.serializers.candidate import CandidateWorkTeamSerializer


class WorkTeamBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор участника команды"""

    candidate_id = CandidateWorkTeamSerializer()
    startup_id = StartupToArticleSerializer()

    class Meta:
        model = WorkTeam
        fields = "__all__"


class WorkTeamUpdatePermissionsSerializer(serializers.ModelSerializer):
    """Сериализатор обновления возможностей участника команды"""

    class Meta:
        model = WorkTeam
        fields = [
            "articles_and_news_management",
            "performers_management",
            "company_management",
            "vacancy_management",
        ]
