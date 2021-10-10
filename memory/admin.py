from django.contrib import admin

from memory.models import Memory


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
