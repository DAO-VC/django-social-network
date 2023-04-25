from django.contrib import admin

from profiles.models import (
    Startup,
    Investor,
    Professional,
    SaleRegions,
    Links,
    Purpose,
    Achievements,
    Industries,
)

# Register your models here.
admin.site.register(Startup)
admin.site.register(Investor)
admin.site.register(Professional)
admin.site.register(Industries)
admin.site.register(Achievements)
admin.site.register(Purpose)
admin.site.register(Links)
admin.site.register(SaleRegions)
