from django.contrib import admin
from django.urls import reverse

from profiles.models.investor import Investor
from profiles.models.other_models import (
    Industries,
    Achievements,
    Purpose,
    Links,
    SaleRegions,
)
from profiles.models.professional import Professional
from profiles.models.startup import Startup
from django.utils.safestring import mark_safe


@admin.register(Industries)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type")


@admin.register(Achievements)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Links)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(SaleRegions)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Purpose)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner_link")
    search_fields = (
        "name__startswith",
        "id",
    )
    # list_filter = ("name", "owner")
    ordering = ("id",)
    filter_horizontal = ("work_team", "business_type", "regions", "industries")

    def owner_link(self, startup: Startup):
        url = reverse("admin:core_user_change", args=[startup.owner.id])
        link = '<a href="%s">%s</a>' % (url, startup.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Владелец"


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "owner_link")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    # list_filter = ['name', ('owner', admin.RelatedOnlyFieldListFilter)]
    ordering = ("id",)
    filter_horizontal = ("skills",)

    def owner_link(self, professional: Professional):
        url = reverse("admin:core_user_change", args=[professional.owner.id])
        link = '<a href="%s">%s</a>' % (url, professional.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Владелец"


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "owner_link")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    # list_filter = ['name', ('owner', admin.RelatedOnlyFieldListFilter)]
    ordering = ("id",)
    filter_horizontal = ("interest",)

    def owner_link(self, investor: Investor):
        url = reverse("admin:core_user_change", args=[investor.owner.id])
        link = '<a href="%s">%s</a>' % (url, investor.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Владелец"
