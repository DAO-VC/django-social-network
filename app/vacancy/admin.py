from django.contrib import admin

from vacancy.models import Vacancy, WorkTeam, Candidate

admin.site.register(Vacancy)
admin.site.register(WorkTeam)
admin.site.register(Candidate)
