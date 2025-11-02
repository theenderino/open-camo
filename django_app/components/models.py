from django.db import models
from django.utils import timezone


class Part(models.Model):
    part_name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)

    # Flugzeugbezug
    removed_from_ac = models.ForeignKey(
        'fleet.Aircraft',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='removed_parts'
    )
    installed_in_ac = models.ForeignKey(
        'fleet.Aircraft',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='installed_parts'
    )

    # Zeitstempel
    date_installed = models.DateTimeField(null=True, blank=True)
    date_removed = models.DateTimeField(null=True, blank=True)
    date_overhauled = models.DateTimeField(null=True, blank=True)

    # Betriebszeiten in Stunden
    tsi = models.IntegerField(default=0)  # Time Since Installation
    tso = models.IntegerField(default=0)  # Time Since Overhaul
    tsn = models.IntegerField(default=0)  # Total Time Since New

    def save(self, *args, **kwargs):
        now = timezone.now()

        # === TSI (Time Since Installation) ===
        if self.date_installed:
            if self.date_removed:
                self.tsi = int((self.date_removed - self.date_installed).total_seconds() / 3600)
            else:
                self.tsi = int((now - self.date_installed).total_seconds() / 3600)
        else:
            self.tsi = 0

        # === TSO (Time Since Overhaul) ===
        if self.date_overhauled:
            if self.date_removed:
                self.tso = int((self.date_removed - self.date_overhauled).total_seconds() / 3600)
            else:
                self.tso = int((now - self.date_overhauled).total_seconds() / 3600)
        else:
            self.tso = self.tsn  # falls nie überholt → = Gesamtzeit

        # === TSN (Total Since New) ===
        # (momentan = TSI; kann später kumulativ erweitert werden)
        self.tsn = self.tsi

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.part_name} ({self.part_number})"
