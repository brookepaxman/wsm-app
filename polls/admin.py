from django.contrib import admin

from .models import User, Stat, Dummy, Analysis, Session

admin.site.register(User)
admin.site.register(Stat)
admin.site.register(Dummy)
admin.site.register(Analysis)
admin.site.register(Session)
