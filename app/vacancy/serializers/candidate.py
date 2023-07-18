from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError

from core.models import User
from profiles.models.professional import Professional
from profiles.models.startup import Startup
from profiles.serializers.professional import ProfessionalSerializer
from vacancy.models.candidate import Candidate
from vacancy.models.vacancy import Vacancy
from vacancy.models.workteam import WorkTeam
from vacancy.serializers.vacancy import VacancyBaseSerializer


class CandidateCreateSerializer(serializers.ModelSerializer):
    """Сериализатор подачи заявки кандидата на вакансию -> Создание кандидата"""

    professional_id = serializers.PrimaryKeyRelatedField(read_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(read_only=True)
    accept_status = serializers.CharField(read_only=True)
    base_status = serializers.CharField(read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = Candidate
        fields = "__all__"

    def create(self, validated_data):
        vacancy_id = get_object_or_404(
            Vacancy, pk=self.context.get("view").kwargs.get("pk")
        )
        professional = get_object_or_404(
            Professional, owner=self.context["request"].user
        )
        about = validated_data["about"]
        try:
            candidate = Candidate.objects.create(
                vacancy_id=vacancy_id,
                professional_id=professional,
                accept_status=Candidate.AcceptStatus.PENDING_FOR_APPROVAL,
                base_status=Candidate.BaseStatus.NEW,
                is_favorite=False,
                about=about,
            )
        except IntegrityError:
            raise ValidationError("Вы уже подались на эту вакансию")

        return candidate
        # candidate = Candidate.objects.create(
        #     vacancy_id=vacancy_id,
        #     professional_id=professional,
        #     accept_status=Candidate.AcceptStatus.PENDING_FOR_APPROVAL,
        #     base_status=Candidate.BaseStatus.NEW,
        #     is_favorite=False,
        #     about=about,
        # )
        # return candidate


class CandidateBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор кандидата"""

    # TODO : поля
    professional_id = ProfessionalSerializer()
    vacancy_id = VacancyBaseSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"


class StartupApproveCandidateSerializer(serializers.ModelSerializer):
    """Добавление подтвержденного кандидата в команду стартапа"""

    professional_id = ProfessionalSerializer(read_only=True)
    vacancy_id = VacancyBaseSerializer(read_only=True)

    class Meta:
        model = Candidate

        fields = ["professional_id", "vacancy_id", "base_status", "accept_status"]

    def update(self, instance: Candidate, validated_data):
        startup = Startup.objects.filter(id=instance.vacancy_id.company_id.id).first()
        position = instance.vacancy_id.position
        try:
            work_team_obj = WorkTeam.objects.create(
                candidate_id=instance, startup_id=startup, position=position
            )
        except IntegrityError:
            raise ValidationError("This candidate already in startups team")

        with transaction.atomic():
            startup.work_team.add(work_team_obj)
            startup.save()
            instance.base_status = Candidate.BaseStatus.VIEWED
            instance.accept_status = Candidate.AcceptStatus.IN_THE_TEAM
            instance.save()
            user = User.objects.get(id=instance.professional_id.owner.id)
            user.permissions = work_team_obj
            user.save()
        return instance


class CandidateFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости вакансии"""

    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = (
            "professional_id",
            "vacancy_id",
            "base_status",
            "accept_status",
            "is_favorite",
            "created_at",
            "about",
        )

    def update(self, instance: Candidate, validated_data):
        instance.change_favorite()
        instance.save()
        return super().update(instance, validated_data)
