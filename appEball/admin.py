from django.contrib import admin
from .models import CustomUser, Tournament, Team, Notification, Tactic, Player, Field, Game, Slot, Reserve, Substitute

admin.site.register(CustomUser)
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Notification)
admin.site.register(Tactic)
admin.site.register(Player)
admin.site.register(Field)
admin.site.register(Game)
admin.site.register(Reserve)
admin.site.register(Substitute)
admin.site.register(Slot)

