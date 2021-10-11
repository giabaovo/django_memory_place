from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from memory.models import Memory


@admin.register(Memory)
class MemoryAdmin(LeafletGeoAdmin):
    list_display = ['name', 'created_at', 'updated_at']
