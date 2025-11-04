from django.db import models


class Requirement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    interval_fh = models.PositiveIntegerField(
        null=True, blank=True, help_text="Interval in flight hours"
    )
    interval_months = models.PositiveIntegerField(
        null=True, blank=True, help_text="Interval in months"
    )

    def __str__(self):
        return self.name


class Component(models.Model):
    part = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    tsn = models.FloatField(help_text="Total hours since new")
    tso = models.FloatField(help_text="Total hours since overhaul")
    tsi = models.FloatField(help_text="Hours since installation")
    removed_from_ac = models.CharField(max_length=50, blank=True, null=True)
    installed_in_ac = models.CharField(max_length=50, blank=True, null=True)
    requirements = models.ManyToManyField(
        Requirement, related_name="components", blank=True
    )

    def __str__(self):
        return f"{self.part} ({self.serial_number})"
