from django.contrib import admin
from .models import Component, Requirement, Installation

# -------------------------------
# Admin Interface für Components
# -------------------------------
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("part", "part_number", "serial_number")
    filter_horizontal = ("requirements",)  # ManyToMany bequem auswählbar

# -------------------------------
# Admin Interface für Requirements
# -------------------------------
@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ("name", "interval_fh", "interval_months")

# -------------------------------
# Admin Interface für Installationen
# -------------------------------
@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ("component", "aircraft", "installed_at", "removed_at", "is_installed")
