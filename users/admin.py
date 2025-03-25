from django.contrib import admin
from .models import Citoyen, Moderator, Admin, SuperAdmin

@admin.register(Citoyen)
class CitoyenAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'citycode', 'created_at', 'updated_at')
    search_fields = ('prenom', 'nom', 'email', 'citycode')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'is_active_moderator', 'created_at', 'updated_at')
    search_fields = ('prenom', 'nom', 'email')
    list_filter = ('is_active_moderator', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'is_active_admin', 'created_at', 'updated_at')
    search_fields = ('prenom', 'nom', 'email')
    list_filter = ('is_active_admin', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'is_active_superadmin', 'created_at', 'updated_at')
    search_fields = ('prenom', 'nom', 'email')
    list_filter = ('is_active_superadmin', 'created_at', 'updated_at')
    ordering = ('-created_at',)