from django.db import models
from datetime import date, timedelta

class Aircraft(models.Model):
    registration = models.CharField(max_length=20, unique=True, null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    date_of_manufacture = models.DateField(null=True, blank=True)
    
    # Flugstunden im Format "HH:MM"
    tfh = models.CharField("Total Flight Hours", max_length=10, default="0:00")
    
    dow = models.DecimalField("Dry Operating Weight (kg)", max_digits=6, decimal_places=1, null=True, blank=True)
    mtw = models.DecimalField("Maximum Takeoff Weight (kg)", max_digits=6, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["registration"]

    def __str__(self):
        return f"{self.registration}"

    @property
    def tsn(self):
        """Berechnet die Zeit seit Neuauslieferung als Jahre/Monate/Tage."""
        if not self.date_of_manufacture:
            return "-"
        today = date.today()
        delta = today - self.date_of_manufacture
        total_days = delta.days
        years, days = divmod(total_days, 365)
        months, days = divmod(days, 30)
        return f"{years} Jahre, {months} Monate, {days} Tage"

    @property
    def tfh_hours(self):
        """Gibt tfh als Stunden+Minuten Tuple zurück."""
        try:
            h, m = self.tfh.split(":")
            return int(h), int(m)
        except:
            return 0, 0

    @tfh_hours.setter
    def tfh_hours(self, value):
        """Setzt tfh von Stunden+Minuten Tuple."""
        hours, minutes = value
        self.tfh = f"{hours}:{minutes:02d}"
