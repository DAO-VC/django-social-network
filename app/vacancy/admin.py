from django.contrib import admin

from vacancy.models import Vacancy, WorkTeam, Candidate, Offer

admin.site.register(Vacancy)
admin.site.register(WorkTeam)
admin.site.register(Candidate)
admin.site.register(Offer)
