from django.contrib import admin
from django.urls import reverse

from image.models import Image
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
    list_display = ("id", "title_link", "type")

    def title_link(self, industries: Industries):
        url = reverse("admin:profiles_industries_change", args=[industries.id])
        link = '<a href="%s">%s</a>' % (url, industries.title)
        return mark_safe(link)

    title_link.short_description = "Название"


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
    list_display = ("id", "title_link")

    def title_link(self, sale_region: SaleRegions):
        url = reverse("admin:profiles_saleregions_change", args=[sale_region.id])
        link = '<a href="%s">%s</a>' % (url, sale_region.name)
        return mark_safe(link)

    title_link.short_description = "Название"


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     # print(request.resolver_match.kwargs['object_id'])
    #
    #     if db_field.name == "logo":
    #         kwargs["queryset"] = Image.objects.filter(id=request.resolver_match.kwargs['object_id'])
    #     return super(StartupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(StartupAdmin, self).get_form(request, obj, **kwargs)
    #     # form.base_fields["logo"].disabled = True
    #     # form.base_fields["logo"].can_change_related = False
    #     form.base_fields["logo"].queryset = Image.objects.filter(id=obj.logo.id)
    #
    #     form.base_fields["background"].disabled = True
    #     form.base_fields["background"].can_change_related = False
    #     form.base_fields["pitch_presentation"].disabled = True
    #     form.base_fields["background"].queryset = None
    #     return form
    list_display = (
        "id",
        "name_link",
        "owner_link",
    )
    search_fields = (
        "name__startswith",
        "id",
    )
    ordering = ("id",)
    filter_horizontal = ("work_team", "business_type", "regions", "industries")
    autocomplete_fields = ("logo", "background", "pitch_presentation")

    def owner_link(self, startup: Startup):
        url = reverse("admin:core_user_change", args=[startup.owner.id])
        link = '<a href="%s">%s</a>' % (
            url,
            f"{startup.owner.id}-{startup.owner.email}",
        )
        return mark_safe(link)

    owner_link.short_description = "Владелец"

    def name_link(self, startup: Startup):
        url = reverse("admin:profiles_startup_change", args=[startup.id])
        link = '<a href="%s">%s</a>' % (url, startup.name)
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
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ProfessionalAdmin, self).get_form(request, obj, **kwargs)
    #     # form.base_fields["photo"].disabled = True
    #     form.base_fields["photo"].disabled = True
    #     form.base_fields["cv"].disabled = True
    #     return form

    list_display = ("id", "name_link", "email_link", "owner_link")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    # list_filter = ['name', ('owner', admin.RelatedOnlyFieldListFilter)]
    ordering = ("id",)
    filter_horizontal = ("skills",)
    autocomplete_fields = (
        "photo",
        "cv",
    )

    def owner_link(self, professional: Professional):
        url = reverse("admin:core_user_change", args=[professional.owner.id])
        link = '<a href="%s">%s</a>' % (url, professional.owner.email)
        return mark_safe(link)

    owner_link.short_description = "Владелец"

    def email_link(self, professional: Professional):
        url = reverse(
            "admin:profiles_professional_change", args=[professional.owner.id]
        )
        link = '<a href="%s">%s</a>' % (url, professional.email)
        return mark_safe(link)

    email_link.short_description = "Email"

    def name_link(self, professional: Professional):
        url = reverse(
            "admin:profiles_professional_change", args=[professional.owner.id]
        )
        link = '<a href="%s">%s</a>' % (url, professional.name)
        return mark_safe(link)

    name_link.short_description = "Имя"


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(InvestorAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields["photo"].disabled = True
    #     form.base_fields["cv"].disabled = True
    #     return form

    list_display = ("id", "name_link", "email_link", "owner_link")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    # list_filter = ['name', ('owner', admin.RelatedOnlyFieldListFilter)]
    ordering = ("id",)
    filter_horizontal = ("interest",)
    autocomplete_fields = (
        "photo",
        "cv",
    )

    def owner_link(self, investor: Investor):
        url = reverse("admin:core_user_change", args=[investor.owner.id])
        link = '<a href="%s">%s</a>' % (url, investor.owner.email)
        return mark_safe(link)

    owner_link.short_description = "Владелец"

    def email_link(self, investor: Investor):
        url = reverse("admin:profiles_investor_change", args=[investor.id])
        link = '<a href="%s">%s</a>' % (url, investor.email)
        return mark_safe(link)

    email_link.short_description = "Email"

    def name_link(self, investor: Investor):
        url = reverse("admin:profiles_investor_change", args=[investor.id])
        link = '<a href="%s">%s</a>' % (url, investor.name)
        return mark_safe(link)

    email_link.short_description = "Имя"
