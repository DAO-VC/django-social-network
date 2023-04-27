from rest_framework import serializers

from profiles.models import (
    Industries,
    Achievements,
    Purpose,
    Links,
    SaleRegions,
    Startup,
    BusinessType,
)


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = "__all__"


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = "__all__"


class SaleRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleRegions
        fields = "__all__"


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = "__all__"


class StartupBaseSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer()
    purpose = PurposeSerializer()
    social_links = LinkSerializer()
    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Startup
        fields = "__all__"

    def create(self, validated_data):
        achievement = validated_data.pop("achievements")
        purpose = validated_data.pop("purpose")
        social_links = validated_data.pop("social_links")
        industries = validated_data.pop("industries")
        regions = validated_data.pop("regions")
        business_type = validated_data.pop("business_type")

        achievement_obj = Achievements.objects.create(**achievement)
        purpose_obj = Purpose.objects.create(**purpose)
        social_links_obj = Links.objects.create(**social_links)
        owner = self.context["request"].user
        startup = Startup.objects.create(
            **validated_data,
            achievements=achievement_obj,
            purpose=purpose_obj,
            social_links=social_links_obj,
            owner=owner
        )

        startup.industries.set(industries)
        startup.regions.set(regions)
        startup.business_type.set(business_type)
        # TODO : добавить транзакции
        return startup
