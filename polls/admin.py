from django.contrib import admin

from .models import Stat, Dummy, Analysis, Session

admin.site.register(Stat)
admin.site.register(Dummy)
admin.site.register(Analysis)
admin.site.register(Session)
