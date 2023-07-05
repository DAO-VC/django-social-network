from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from vacancy.models.candidate import Candidate
from vacancy.models.vacancy import Vacancy, Skill, Requirement
from vacancy.models.workteam import WorkTeam


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

    def has_module_permission(self, request):
        return False


@admin.register(Requirement)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

    def has_module_permission(self, request):
        return False


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "company_link", "is_visible", "created_at")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    list_filter = ("is_visible", ("company_id", admin.RelatedOnlyFieldListFilter))
    ordering = (
        "id",
        "created_at",
        "is_visible",
    )
    filter_horizontal = ("skills", "requirements")

    def company_link(self, vacancy: Vacancy):
        url = reverse("admin:profiles_startup_change", args=[vacancy.company_id.id])
        link = '<a href="%s">%s</a>' % (url, vacancy.company_id.id)
        return mark_safe(link)

    company_link.short_description = "Владелец"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "professional_link",
        "vacancy_link",
        "base_status",
        "accept_status",
        "created_at",
        "is_favorite",
    )
    search_fields = ("id",)
    list_filter = (
        ("professional_id", admin.RelatedOnlyFieldListFilter),
        ("vacancy_id", admin.RelatedOnlyFieldListFilter),
        "base_status",
        "accept_status",
        "is_favorite",
    )
    ordering = ("id", "created_at", "accept_status", "base_status")

    def professional_link(self, candidate: Candidate):
        url = reverse(
            "admin:profiles_professional_change", args=[candidate.professional_id.id]
        )
        link = '<a href="%s">%s</a>' % (url, candidate.professional_id.id)
        return mark_safe(link)

    professional_link.short_description = "Профессионал"

    def vacancy_link(self, candidate: Candidate):
        url = reverse("admin:vacancy_vacancy_change", args=[candidate.vacancy_id.id])
        link = '<a href="%s">%s</a>' % (url, candidate.vacancy_id.id)
        return mark_safe(link)

    vacancy_link.short_description = "Вакансия"


@admin.register(WorkTeam)
class WorkTeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "candidate_link",
        "startup_link",
        "position",
    )
    list_filter = (
        ("candidate_id", admin.RelatedOnlyFieldListFilter),
        ("startup_id", admin.RelatedOnlyFieldListFilter),
    )
    ordering = ("id",)

    def candidate_link(self, work_team: WorkTeam):
        url = reverse(
            "admin:vacancy_candidate_change", args=[work_team.candidate_id.id]
        )
        link = '<a href="%s">%s</a>' % (url, work_team.candidate_id.id)
        return mark_safe(link)

    candidate_link.short_description = "Кандидат"

    def startup_link(self, work_team: WorkTeam):
        url = reverse("admin:profiles_startup_change", args=[work_team.startup_id.id])
        link = '<a href="%s">%s</a>' % (url, work_team.startup_id.id)
        return mark_safe(link)

    startup_link.short_description = "Стартап"
