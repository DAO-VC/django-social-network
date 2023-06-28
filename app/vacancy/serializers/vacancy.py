from django.db import transaction
from rest_framework import serializers
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from profiles.models.startup import Startup
from vacancy.models.vacancy import Vacancy, Skill, Requirement


class VacancyBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор вакансии"""

    total_candidates = serializers.SerializerMethodField(read_only=True)

    def get_total_candidates(self, instance):
        return instance.candidate_vacancy.count()

    class Meta:
        model = Vacancy
        fields = "__all__"
        extra_fields = ["total_candidates"]


class VacancyCreateSerializer(serializers.ModelSerializer):
    """Сериализато создания вакансии"""

    # is_visible = serializers.BooleanField(read_only=True)
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    skills = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)
    requirements = serializers.SlugRelatedField(
        many=True, slug_field="title", read_only=True
    )
    update_skills = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )
    update_requirements = serializers.ListField(
        child=serializers.CharField(max_length=500), write_only=True
    )

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

        skills_titles = validated_data.pop("update_skills")
        requirements_titles = validated_data.pop("update_requirements")

        with transaction.atomic():
            vacancy = Vacancy.objects.create(**validated_data, company_id=company_id)
            update_skills = []
            for title in skills_titles:
                skill, created = Skill.objects.get_or_create(title=title)
                update_skills.append(skill)
            update_requirements = []
            for title in requirements_titles:
                requirement, created = Requirement.objects.get_or_create(title=title)
                update_requirements.append(requirement)
        if len(update_skills) < 1:
            raise ValidationError("Minium one skill")

        vacancy.skills.set(update_skills)
        vacancy.requirements.set(update_requirements)

        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления вакансии"""

    is_visible = serializers.BooleanField(read_only=True)
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    skills = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)
    requirements = serializers.SlugRelatedField(
        many=True, slug_field="title", read_only=True
    )
    update_skills = serializers.ListField(
        child=serializers.CharField(max_length=54), write_only=True
    )
    update_requirements = serializers.ListField(
        child=serializers.CharField(max_length=500), write_only=True
    )

    class Meta:
        model = Vacancy
        fields = "__all__"

    def update(self, instance, validated_data):
        skills_titles = validated_data.pop("update_skills")
        requirements_titles = validated_data.pop("update_requirements")
        with transaction.atomic():
            new_skills = []
            for title in skills_titles:
                skill, created = Skill.objects.get_or_create(title=title)
                new_skills.append(skill)
            update_requirements = []
            for title in requirements_titles:
                requirement, created = Requirement.objects.get_or_create(title=title)
                update_requirements.append(requirement)
        if len(new_skills) < 1:
            raise ValidationError("Minium one skill")
        instance.skills.set(new_skills)
        instance.requirements.set(update_requirements)

        return super().update(instance, validated_data)


class VacancyVisibleSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости вакансии"""

    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = (
            "company_id",
            "position",
            "salary",
            "salary_type",
            "work_schedude",
            "place",
            "skills",
            "description",
            "requirements",
            "is_visible",
            "created_at",
        )

    def update(self, instance: Vacancy, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True
        instance.save()
        return instance
