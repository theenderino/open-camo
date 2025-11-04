from django.db import models
from fleet.models import Aircraft  # Bestehendes Flugzeugmodell

# -------------------------------
# Requirement Modell
# -------------------------------
class Requirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    interval_fh = models.FloatField(null=True, blank=True)   # Intervall in Flugstunden
    interval_months = models.FloatField(null=True, blank=True)  # Intervall in Monaten (optional)

    def __str__(self):
        return self.name

# -------------------------------
# Component Modell
# -------------------------------
class Component(models.Model):
    part = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    tsn = models.FloatField(default=0.0, help_text="Total hours since new")
    tso = models.FloatField(default=0.0, help_text="Time since overhaul")
    tsi = models.FloatField(default=0.0, help_text="Time since installation")
    requirements = models.ManyToManyField(Requirement, blank=True, related_name="components")

    def __str__(self):
        return f"{self.part} ({self.serial_number})"

# -------------------------------
# Installation Modell
# Dokumentiert Einbau/Ausbau einer Komponente in ein Aircraft
# -------------------------------
class Installation(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="installations")
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="installations")
    installed_at = models.DateField()
    removed_at = models.DateField(null=True, blank=True)  # null = noch eingebaut

    # Prüfen, ob die Komponente aktuell eingebaut ist
    def is_installed(self):
        return self.removed_at is None

    def __str__(self):
        status = "Installed" if self.is_installed() else f"Removed {self.removed_at}"
        return f"{self.component} in {self.aircraft} ({status})"
