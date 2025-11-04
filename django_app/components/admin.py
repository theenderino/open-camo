from django.contrib import admin
from .models import Component, Requirement

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("part", "part_number", "serial_number", "installed_in_ac")

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ("name", "interval_fh", "interval_months")
