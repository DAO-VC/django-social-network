from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.utils import IntegrityError
from profiles.models import Startup, Professional
from profiles.serializers import ProfessionalSerializer
from vacancy.models import Vacancy, Candidate, WorkTeam
from rest_framework.exceptions import ValidationError
from django.db.models import Q


class VacancyBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор вакансии"""

    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCreateSerializer(serializers.ModelSerializer):
    """Сериализато создания вакансии"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__in=[
                    self.context["request"].user.id
                ]
            )
            | Q(owner=self.context["request"].user)
        ).first()

        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("Минимум один скил")
        with transaction.atomic():
            vacancy = Vacancy.objects.create(**validated_data, company_id=company_id)
            vacancy.skills.set(skills)

        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления вакансии"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills")
        if len(skills) > 0:
            instance.skills.set(skills)

        return super().update(instance, validated_data)


class VacancyVisibleSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости вакансии"""

    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = (
            "company_id",
            "position",
            "requirements",
            "is_visible",
            "salary",
            "skills",
        )

    def update(self, instance: Vacancy, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True
        instance.save()
        return instance


class CandidateCreateSerializer(serializers.ModelSerializer):
    """Сериализатор подачи заявки кандидата на вакансию -> Создание кандидата"""

    professional_id = serializers.PrimaryKeyRelatedField(read_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(read_only=True)
    accept_status = serializers.CharField(read_only=True)
    base_status = serializers.CharField(read_only=True)

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
        try:
            candidate = Candidate.objects.create(
                vacancy_id=vacancy_id,
                professional_id=professional,
                accept_status=Candidate.AcceptStatus.PENDING_FOR_APPROVAL,
                base_status=Candidate.BaseStatus.NEW,
            )
        except IntegrityError:
            raise ValidationError("Вы уже подались на эту вакансию")

        return candidate


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
        work_team_obj = WorkTeam.objects.create(
            candidate_id=instance, position=position
        )

        if work_team_obj in startup.work_team.all():
            raise ValidationError("This candidate already in startups team")
        with transaction.atomic():
            startup.work_team.add(work_team_obj)
            startup.save()
            instance.base_status = Candidate.BaseStatus.VIEWED
            instance.accept_status = Candidate.AcceptStatus.IN_THE_TEAM
            instance.save()
        # TODO : нужно переводить в статус скрыта
        return instance


class StartupAcceptRetrieveCandidate(serializers.ModelSerializer):
    """Сериализатор изменения статуса кандидата на ACCEPT"""

    professional_id = ProfessionalSerializer(read_only=True)
    vacancy_id = VacancyBaseSerializer(read_only=True)

    class Meta:
        model = Candidate

        fields = ["professional_id", "vacancy_id", "base_status", "accept_status"]

    def update(self, instance: Candidate, validated_data):
        with transaction.atomic():
            instance.accept_status = Candidate.AcceptStatus.ACCEPT
            instance.save()
        return instance


class WorkTeamBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор участника команды"""

    candidate_id = CandidateBaseSerializer(read_only=True)

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
