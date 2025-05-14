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

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'view_count', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'author__username')
    readonly_fields = ('view_count',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'type', 'author', 'is_private', 'deleted_at')
        }),
        ('Statistiques', {
            'fields': ('view_count',),
            'description': 'Nombre de fois que cette ressource a été consultée'
        }),
    )

admin.site.register(Type)