from django.contrib import admin
from .models import Team, Profile  # Import your models

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'total_members')  # Customize display
    search_fields = ('name', 'leader__username')  # Search by name & leader

    def total_members(self, obj):
        return obj.profile_set.count()  # Count members in the team
    total_members.short_description = 'Total Members'

admin.site.register(Team, TeamAdmin)  # Register Team model
admin.site.register(Profile)  # Register Profile model (if not already)
