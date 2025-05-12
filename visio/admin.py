from django.contrib import admin
from .models import Meeting

# Register your models here.
@admin.register(Meeting)
class Meeting(admin.ModelAdmin):
    list_display = ('creator', 'title_of_meeting', 'created_at', 'updated_at', 'starting_date_time', 'unique_meeting_name')
    search_fields = ('creator',)
    ordering = ('creator', 'created_at', 'updated_at', 'starting_date_time', 'unique_meeting_name')