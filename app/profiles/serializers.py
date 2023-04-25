from rest_framework import serializers

from profiles.models import Industries, Achievements, Purpose, Links, SaleRegions


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
