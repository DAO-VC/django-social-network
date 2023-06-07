from django.urls import path

from vacancy.views.candidate import (
    CandidateCreateView,
    # StartupCandidates,
    ListAllVacancyCandidates,
    StartupRetrieveCandidates,
    ProfessionalMyApplicationsListView,
    ProfessionalMyApplicationsRetrieveView,
    StartupApproveRetrieveCandidate,
    CandidateFavoriteRetrieveView,
    StartupFavoriteCandidates,
    # StartupAcceptCandidate,
)
from vacancy.views.vacancy import (
    VacancyListCreateView,
    VacancyRetrieveView,
    VacancyVisibleRetrieveView,
    VacancyAllView,
    VacancyAllDetailView,
    StartupAllVacancies,
)
from vacancy.views.workteam import (
    ProfessionalWorkView,
    StartupWorkTeamList,
    StartupWorkTeamRetrieveDelete,
)

urlpatterns = [
    path(
        "main/vacancies/", VacancyListCreateView.as_view(), name="list_create_vacancy"
    ),
    path(
        "main/vacancies/<int:pk>/",
        VacancyRetrieveView.as_view(),
        name="retrieve_vacancy",
    ),
    path(
        "main/vacancies/<int:pk>/visible/",
        VacancyVisibleRetrieveView.as_view(),
        name="visible_retrieve_vacancy",
    ),
    path("common/vacancies/", VacancyAllView.as_view(), name="all_vacancy"),
    path(
        "common/vacancies/<int:pk>/",
        VacancyAllDetailView.as_view(),
        name="all_detail_vacancy",
    ),
    path(
        "common/startup/<int:pk>/vacancies",
        StartupAllVacancies.as_view(),
        name="all_vacancies_to_startup",
    ),
    path(
        "common/vacancies/<int:pk>/apply/",
        CandidateCreateView.as_view(),
        name="apply_candidate",
    ),
    # path(
    #     "main/startup/candidates/",
    #     StartupCandidates.as_view(),
    #     name="all_startup_candidates",
    # ),
    path(
        "main/vacancies/<int:pk>/candidates/",
        ListAllVacancyCandidates.as_view(),
        name="all_candidates_vacancy",
    ),
    path(
        "main/startup/candidates/<int:pk>/",
        StartupRetrieveCandidates.as_view(),
        name="retrieve_startup_candidates",
    ),
    path(
        "main/professional/applications/",
        ProfessionalMyApplicationsListView.as_view(),
        name="all_applications_professional",
    ),
    path(
        "main/professional/my_works/",
        ProfessionalWorkView.as_view(),
        name="work_professional",
    ),
    path(
        "main/professional/applications/<int:pk>/",
        ProfessionalMyApplicationsRetrieveView.as_view(),
        name="retrieve_applications_professional",
    ),
    path(
        "main/startup/candidates/<int:pk>/accept/",
        StartupApproveRetrieveCandidate.as_view(),
        name="accept_startup_candidates",
    ),
    # path(
    #     "main/startup/candidates/<int:pk>/accept/",
    #     StartupAcceptCandidate.as_view(),
    #     name="accept_startup_candidates",
    # ),
    path(
        "main/startup/my_team/",
        StartupWorkTeamList.as_view(),
        name="startup_work_team",
    ),
    path(
        "main/startup/my_team/<int:pk>/",
        StartupWorkTeamRetrieveDelete.as_view(),
        name="retrieve_startup_work_team",
    ),
    path(
        "main/startup/candidates/<int:pk>/favorite/",
        CandidateFavoriteRetrieveView.as_view(),
        name="add/remove_candidate_to_favorite",
    ),
    path(
        "main/startup/candidates/",
        StartupFavoriteCandidates.as_view(),
        name="all_favorite_candidates",
    ),
]
