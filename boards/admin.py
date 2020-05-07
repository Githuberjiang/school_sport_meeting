from django.contrib import admin

from .models import StudentUser, Notice, SportMeet, SportScores

admin.site.register(SportScores)
admin.site.register(SportMeet)
admin.site.register(StudentUser)
# admin.site.register(SUser)
# admin.site.register(Application)
# admin.site.register(Score)
admin.site.register(Notice)

