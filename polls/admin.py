from django.contrib import admin

from .models import User, Stat, Dummy

admin.site.register(User)
admin.site.register(Stat)
admin.site.register(Dummy)
