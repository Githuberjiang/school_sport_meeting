from django.contrib import admin

from .models import SportMeet, Announcement, Classes, SUser, Application,Score, Notice

admin.site.register(SportMeet)
# admin.site.register(Announcement)
admin.site.register(Classes)
admin.site.register(SUser)
admin.site.register(Application)
admin.site.register(Score)
admin.site.register(Notice)

