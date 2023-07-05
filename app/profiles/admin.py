from django.contrib import admin
from django.urls import reverse
from profiles.models.investor import Investor
from profiles.models.other_models import (
    Industries,
    Achievements,
    Links,
    SaleRegions,
)
from profiles.models.professional import Professional
from profiles.models.startup import Startup
from django.utils.safestring import mark_safe


@admin.register(Industries)
class IndustriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type")


@admin.register(Achievements)
class AchievementsAdmin(admin.ModelAdmin):
    list_display = ("id",)

    def has_module_permission(self, request):
        return False


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ("id",)

    def has_module_permission(self, request):
        return False


@admin.register(SaleRegions)
class SaleRegionsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(StartupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["logo"].disabled = True
        form.base_fields["background"].disabled = True
        form.base_fields["pitch_presentation"].disabled = True
        return form

    list_display = (
        "id",
        "name",
        "owner_link",
    )
    search_fields = (
        "name__startswith",
        "id",
    )
    ordering = ("id",)
    filter_horizontal = ("work_team", "business_type", "regions", "industries")

    def owner_link(self, startup: Startup):
        url = reverse("admin:core_user_change", args=[startup.owner.id])
        link = '<a href="%s">%s</a>' % (url, startup.owner.id)
        return mark_safe(link)

    owner_link.short_description = "Владелец"

    # def image_link(self, startup: Startup):
    #     try:
    #         if Image.objects.filter(id=startup.logo.id).exists():
    #             subject_object = Image.objects.get(id=startup.logo.id)
    #             return mark_safe(
    #                 '<img src="%s" style="width: 90px; height:90px;" />'
    #                 % subject_object.image.url
    #             )
    #     except Exception:
    #         return "No Image"


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ProfessionalAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["photo"].disabled = True
        form.base_fields["cv"].disabled = True
        return form

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
    def get_form(self, request, obj=None, **kwargs):
        form = super(InvestorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["photo"].disabled = True
        form.base_fields["cv"].disabled = True
        return form

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
