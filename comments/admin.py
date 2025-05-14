from django.contrib import admin
from .models import Comment

def soft_delete_comments(modeladmin, request, queryset):
    queryset.update(is_deleted=True)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('citoyen', 'get_ressource_title', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('content', 'citoyen__username', 'ressource__title')
    date_hierarchy = 'created_at'
    actions = [soft_delete_comments]
    
    def get_ressource_title(self, obj):
        return obj.ressource.title
    get_ressource_title.short_description = 'Ressource'
    
    fieldsets = (
        (None, {
            'fields': ('citoyen', 'ressource', 'content', 'is_deleted')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Dates de création et de modification'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')