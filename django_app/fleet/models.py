from django.db import models
from datetime import timedelta


class Aircraft(models.Model):
    manufacturer = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    date_of_manufacture = models.DateField(null=True, blank=True)
    tfh = models.DecimalField("Total Flight Hours", max_digits=8, decimal_places=1, default=0.0)
    tsn = models.DurationField("Time Since New", null=True, blank=True)
    dow = models.DecimalField("Dry Operating Weight (kg)", max_digits=6, decimal_places=1, null=True, blank=True)
    mtw = models.DecimalField("Maximum Takeoff Weight (kg)", max_digits=6, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["manufacturer", "type"]

    def __str__(self):
        return f"{self.manufacturer} {self.type}"

    def formatted_tsn(self):
        """Zeigt TSN schön formatiert als Jahre/Monate/Tage an."""
        if not self.tsn:
            return "-"
        total_days = self.tsn.days
        years, days = divmod(total_days, 365)
        months, days = divmod(days, 30)
        return f"{years} Jahre, {months} Monate, {days} Tage"
