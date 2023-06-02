from rest_framework import serializers

from profiles.models.other_models import (
    Industries,
    Achievements,
    Purpose,
    Links,
    SaleRegions,
    BusinessType,
)


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
