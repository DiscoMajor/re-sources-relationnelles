from django.contrib import admin
from .models import HealthFacilityType, HealthFacility, AddressSearch

@admin.register(HealthFacilityType)
class HealthFacilityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    search_fields = ('name',)
    ordering = ('display_order', 'name')

@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'city', 'department', 'is_active')
    list_filter = ('facility_type', 'is_active', 'city', 'department', 'wheelchair')
    search_fields = ('name', 'city', 'department', 'phone')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'external_id')
    list_per_page = 50

@admin.register(AddressSearch)
class AddressSearchAdmin(admin.ModelAdmin):
    list_display = ('query', 'label', 'city', 'postcode', 'created_at')
    list_filter = ('type', 'city', 'postcode')
    search_fields = ('query', 'label', 'city', 'street')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_per_page = 50