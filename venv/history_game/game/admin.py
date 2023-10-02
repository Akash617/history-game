from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, Match, User


# Register your models here.
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'events', 'game_won', 'user_playing')

    def events(self, events):
        return ",\n".join([e.name for e in events.event_list.all()])

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'description', 'category', 'topic')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'highscore', 'is_staff', 'is_active', 'last_login')
admin.site.register(User, UserAdmin)
