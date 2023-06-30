from django.contrib import admin

from vacancy.models.candidate import Candidate
from vacancy.models.vacancy import Vacancy, Skill, Requirement
from vacancy.models.workteam import WorkTeam

admin.site.register(Vacancy)
admin.site.register(WorkTeam)
admin.site.register(Candidate)
admin.site.register(Skill)
admin.site.register(Requirement)
