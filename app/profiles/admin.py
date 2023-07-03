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

# admin.site.register(Startup)
admin.site.register(Investor)
# admin.site.register(Professional)
admin.site.register(Industries)
admin.site.register(Achievements)
admin.site.register(Purpose)
admin.site.register(Links)
admin.site.register(SaleRegions)


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner_link")
    search_fields = (
        "name",
        "id",
    )
    list_filter = ("name",)
    ordering = ("id",)
    filter_horizontal = ("work_team", "business_type", "regions", "industries")

    def owner_link(self, startup: Startup):
        url = reverse("admin:core_user_change", args=[startup.owner.id])
        link = '<a href="%s">%s</a>' % (url, startup.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Owner"


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "owner_link")
    search_fields = (
        "name",
        "id",
        "email",
    )
    list_filter = ("name",)
    ordering = ("id",)
    filter_horizontal = ("skills",)

    def owner_link(self, professional: Professional):
        url = reverse("admin:core_user_change", args=[professional.owner.id])
        link = '<a href="%s">%s</a>' % (url, professional.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Owner"
