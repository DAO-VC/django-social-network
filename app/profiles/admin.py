from django.contrib import admin

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

admin.site.register(Startup)
admin.site.register(Investor)
admin.site.register(Professional)
admin.site.register(Industries)
admin.site.register(Achievements)
admin.site.register(Purpose)
admin.site.register(Links)
admin.site.register(SaleRegions)
