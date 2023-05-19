from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.utils import IntegrityError
from profiles.models import Startup, Investor, Professional
from profiles.serializers import ProfessionalSerializer
from vacancy.models import Vacancy, Offer, Candidate
from rest_framework.exceptions import ValidationError


class VacancyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(owner=self.context["request"].user).first()
        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("Минимум один скил")

        vacancy = Vacancy.objects.create(**validated_data, company_id=company_id)
        vacancy.skills.set(skills)

        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
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


class OfferCreateSerializer(serializers.ModelSerializer):
    investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
        investor: Investor = Investor.objects.filter(
            owner=self.context["request"].user
        ).first()

        industries = validated_data.pop("industries")
        if len(industries) < 1:
            raise ValidationError("Минимум одина индустрия")

        resume = Offer.objects.create(**validated_data, investor_id=investor)
        resume.industries.set(industries)

        return resume


class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ("investor_id",)

    def update(self, instance, validated_data):
        industries = validated_data.pop("industries")
        if len(industries) > 0:
            instance.industries.set(industries)
        return super().update(instance, validated_data)


class CandidateCreateSerializer(serializers.ModelSerializer):
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
    # TODO : поля
    professional_id = ProfessionalSerializer()
    vacancy_id = VacancyBaseSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"


class StartupApproveCandidateSerializer(serializers.ModelSerializer):
    professional_id = ProfessionalSerializer(read_only=True)
    vacancy_id = VacancyBaseSerializer(read_only=True)

    class Meta:
        model = Candidate

        fields = ["professional_id", "vacancy_id", "base_status", "accept_status"]

    def update(self, instance: Candidate, validated_data):
        startup = Startup.objects.filter(owner=self.context["request"].user).first()
        if instance in startup.work_team.all():
            raise ValidationError("This candidate already in startups team")
        startup.work_team.add(instance)
        startup.save()
        instance.base_status = Candidate.BaseStatus.VIEWED
        instance.accept_status = Candidate.AcceptStatus.IN_THE_TEAM
        instance.save()
        # TODO : нужно переводить в статус скрыта
        return instance


class StartupAcceptRetrieveCandidate(serializers.ModelSerializer):
    professional_id = ProfessionalSerializer(read_only=True)
    vacancy_id = VacancyBaseSerializer(read_only=True)

    class Meta:
        model = Candidate

        fields = ["professional_id", "vacancy_id", "base_status", "accept_status"]

    def update(self, instance: Candidate, validated_data):
        instance.accept_status = Candidate.AcceptStatus.ACCEPT
        instance.save()
        return instance
