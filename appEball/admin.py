from django.contrib import admin
from .models import CustomUser, Tournament

admin.site.register(CustomUser)
admin.site.register(Tournament)
