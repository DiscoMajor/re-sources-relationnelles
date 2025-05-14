from django.contrib import admin
from .models import Ressource, Type, ConnectionLog

@admin.register(ConnectionLog)
class ConnectionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'timestamp', 'ip_address', 'get_user_agent')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'user__email', 'ip_address')
    date_hierarchy = 'timestamp'
    
    def get_user_agent(self, obj):
        return obj.user_agent[:50] + '...' if obj.user_agent and len(obj.user_agent) > 50 else obj.user_agent
    get_user_agent.short_description = 'Navigateur'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Ressource)
admin.site.register(Type)