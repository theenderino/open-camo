from django.contrib import admin
from .models import Aircraft

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("manufacturer", "type", "date_of_manufacture", "tfh", "tsn", "dow", "mtw")
    readonly_fields = ("tsn",)
    search_fields = ("manufacturer", "type")
