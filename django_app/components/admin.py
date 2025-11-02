from django.contrib import admin
from .models import Part

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_name', 'part_number', 'serial_number', 'tsi', 'tso', 'tsn', 'installed_in_ac')
    list_filter = ('installed_in_ac',)
    search_fields = ('part_name', 'part_number', 'serial_number')
