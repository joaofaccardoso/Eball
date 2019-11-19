from django.contrib import admin
from .models import CustomUser, Tournament, Team

admin.site.register(CustomUser)
admin.site.register(Tournament)
admin.site.register(Team)
