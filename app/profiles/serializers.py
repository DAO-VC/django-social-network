from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from image.serializers import ImageSerializer, FileSerializer
from profiles.models import (
    Industries,
    Achievements,
    Purpose,
    Links,
    SaleRegions,
    Startup,
    BusinessType,
    Professional,
    Investor,
)
from image.tasks import cleaner, cleaner_file


class IndustriesSerializer(serializers.ModelSerializer):
    """Сериализатор индустрии"""

    class Meta:
        model = Industries
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор достижения"""

    class Meta:
        model = Achievements
        fields = "__all__"


class PurposeSerializer(serializers.ModelSerializer):
    """Сериализатор цели"""

    class Meta:
        model = Purpose
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор социальной сети"""

    class Meta:
        model = Links
        fields = "__all__"


class SaleRegionSerializer(serializers.ModelSerializer):
    """Сериализатор региона продажи"""

    class Meta:
        model = SaleRegions
        fields = "__all__"


class BusinessTypeSerializer(serializers.ModelSerializer):
    """Сериализатор бизнес типа"""

    class Meta:
        model = BusinessType
        fields = "__all__"


class StartupBaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания стартапа"""

    achievements = AchievementSerializer()
    purpose = PurposeSerializer()
    social_links = LinkSerializer()
    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Startup
        exclude = ("work_team",)

    def create(self, validated_data):
        achievement = validated_data.pop("achievements")
        purpose = validated_data.pop("purpose")
        social_links = validated_data.pop("social_links")
        industries = validated_data.pop("industries")
        if len(industries) < 1:
            raise ValidationError("Минимум одна индустрия")
        regions = validated_data.pop("regions")
        if len(regions) < 1:
            raise ValidationError("Минимум один регион")
        business_type = validated_data.pop("business_type")
        if len(business_type) < 1:
            raise ValidationError("Минимум тип")

        achievement_obj = Achievements.objects.create(**achievement)
        purpose_obj = Purpose.objects.create(**purpose)
        social_links_obj = Links.objects.create(**social_links)
        owner = self.context["request"].user
        with transaction.atomic():
            startup = Startup.objects.create(
                **validated_data,
                achievements=achievement_obj,
                purpose=purpose_obj,
                social_links=social_links_obj,
                owner=owner,
            )

            startup.industries.set(industries)
            startup.regions.set(regions)
            startup.business_type.set(business_type)
            owner.is_onboarding = True
            owner.save()
        # TODO : добавить транзакции
        return startup


class ProfessionalBaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания профессионала"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Professional
        fields = "__all__"

    def create(self, validated_data):
        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("skills : minimum  one skill")
        # interest = validated_data.pop("interest")
        # if len(skills) < 1:
        #     raise ValidationError("interest : minimum  one interest")
        owner = self.context["request"].user
        with transaction.atomic():
            professional = Professional.objects.create(**validated_data, owner=owner)

            professional.skills.set(skills)
            # professional.interest.set(interest)

            owner.is_onboarding = True
            owner.save()

        return professional


class InvestorBaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания инвестора"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"

    def create(self, validated_data):
        interest = validated_data.pop("interest")
        if len(interest) < 1:
            raise ValidationError("Минимум одна индустрия")
        owner = self.context["request"].user
        social_links = validated_data.pop("social_links")
        social_links_obj = Links.objects.create(**social_links)
        with transaction.atomic():
            investor = Investor.objects.create(
                **validated_data, owner=owner, social_links=social_links_obj
            )

            investor.interest.set(interest)

            owner.is_onboarding = True
            owner.save()

        return investor


class StartupUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения стартапа"""

    achievements = AchievementSerializer()
    purpose = PurposeSerializer()
    social_links = LinkSerializer()
    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    # registration_country = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Startup
        exclude = ("work_team",)

    def update(self, instance: Startup, validated_data):
        if "achievements" in validated_data:
            achievement_serializer = self.fields["achievements"]
            achievement_instance = instance.achievements
            achievement_data = validated_data.pop("achievements")
            achievement_serializer.update(achievement_instance, achievement_data)

        if "purpose" in validated_data:
            purpose_serializer = self.fields["purpose"]
            purpose_instance = instance.purpose
            purpose_data = validated_data.pop("purpose")
            purpose_serializer.update(purpose_instance, purpose_data)

        if "social_links" in validated_data:
            social_links_serializer = self.fields["social_links"]
            social_links_instance = instance.social_links
            social_links_data = validated_data.pop("social_links")
            social_links_serializer.update(social_links_instance, social_links_data)

        industries = validated_data.pop("industries")
        if len(industries) > 0:
            instance.industries.set(industries)

        regions = validated_data.pop("regions")
        if len(regions) > 0:
            instance.regions.set(regions)

        business_type = validated_data.pop("business_type")
        if len(business_type) > 0:
            instance.business_type.set(business_type)

        if instance.logo:
            object_logo_id = instance.logo.id
            new_logo_id = validated_data.get("logo")
            if new_logo_id:
                new_logo_id = new_logo_id.id

            cleaner.delay(object_logo_id, new_logo_id)

        if instance.background:
            object_background_id = instance.background.id
            new_background_id = validated_data.get("background")
            if new_background_id:
                new_background_id = new_background_id.id

            cleaner.delay(object_background_id, new_background_id)

        if instance.pitch_presentation:
            object_pitch_presentation_id = instance.pitch_presentation.id
            new_pitch_presentation_id = validated_data.get("pitch_presentation")
            if new_pitch_presentation_id:
                new_pitch_presentation_id = new_pitch_presentation_id.id

            cleaner_file.delay(object_pitch_presentation_id, new_pitch_presentation_id)

        return super().update(instance, validated_data)


class ProfessionalUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения профессионала"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Professional
        fields = "__all__"

    def update(self, instance: Professional, validated_data):

        skills = validated_data.pop("skills")
        if len(skills) > 0:
            instance.skills.set(skills)

        if instance.photo:
            object_photo_id = instance.photo.id
            new_photo_id = validated_data.get("photo")
            if new_photo_id:
                new_photo_id = new_photo_id.id

            cleaner.delay(object_photo_id, new_photo_id)

        if instance.cv:
            object_cv_id = instance.cv.id
            new_cv_id = validated_data.get("cv")
            if new_cv_id:
                new_cv_id = new_cv_id.id

            cleaner_file.delay(object_cv_id, new_cv_id)

        return super().update(instance, validated_data)


class InvestorUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения инвестора"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"

    def update(self, instance, validated_data):
        interest = validated_data.pop("interest")
        if len(interest) > 0:
            instance.interest.set(interest)

        if "social_links" in validated_data:
            social_links_serializer = self.fields["social_links"]
            social_links_instance = instance.social_links
            social_links_data = validated_data.pop("social_links")
            social_links_serializer.update(social_links_instance, social_links_data)

        if instance.photo:
            object_photo_id = instance.photo.id
            new_photo_id = validated_data.get("photo")
            if new_photo_id:
                new_photo_id = new_photo_id.id

            cleaner.delay(object_photo_id, new_photo_id)

        if instance.cv:
            object_cv_id = instance.cv.id
            new_cv_id = validated_data.get("cv")
            if new_cv_id:
                new_cv_id = new_cv_id.id

            cleaner_file.delay(object_cv_id, new_cv_id)

        return super().update(instance, validated_data)


# class ResumeCreateSerializer(serializers.ModelSerializer):
#     professional_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
#
#     class Meta:
#         model = Resume
#         fields = "__all__"
#
#     def create(self, validated_data):
#         professional: Professional = Professional.objects.filter(
#             owner=self.context["request"].user
#         ).first()
#         if Resume.objects.filter(professional_id=professional).exists():
#             raise ValidationError("Резюме уже существует")
#         skills = validated_data.pop("skills")
#         if len(skills) < 1:
#             raise ValidationError("Минимум один скил")
#
#         resume = Resume.objects.create(**validated_data, professional_id=professional)
#         resume.skills.set(skills)
#
#         return resume
#
#
# class ResumeUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Resume
#         exclude = ("professional_id",)
#
#     def update(self, instance, validated_data):
#         skills = validated_data.pop("skills")
#         if len(skills) > 0:
#             instance.interest.set(skills)
#         return super().update(instance, validated_data)


class StartupSerializer(serializers.ModelSerializer):
    """Базовый сериализатор  стартапа"""

    logo = ImageSerializer(read_only=True)
    background = ImageSerializer(read_only=True)
    pitch_presentation = FileSerializer(read_only=True)
    social_links = LinkSerializer()
    purpose = PurposeSerializer()
    achievements = AchievementSerializer()
    registration_country = SaleRegionSerializer(read_only=True)

    class Meta:
        model = Startup
        fields = "__all__"


class ProfessionalSerializer(serializers.ModelSerializer):
    """Базовый сериализатор профессионала"""

    photo = ImageSerializer(read_only=True)
    cv = FileSerializer(read_only=True)

    class Meta:
        model = Professional
        fields = "__all__"


class InvestorSerializer(serializers.ModelSerializer):
    """Базовый сериализатор инвестора"""

    photo = ImageSerializer(read_only=True)
    cv = FileSerializer(read_only=True)
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"
