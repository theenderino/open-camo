"""
Testskript für Components und Installationen
--------------------------------------------
- Erstellt Aircraft und Components
- Fügt Requirements hinzu
- Baut Components ein/aus
- Addiert Flugstunden auf aktuell eingebauten Komponenten
- Eigenständig ausführbar: Django-Umgebung wird automatisch geladen
"""

import os
import sys
import django
import datetime

# -------------------------------
# Django-Umgebung initialisieren
# -------------------------------
sys.path.append("/workspace")  # <-- hier liegt open_camo
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "open_camo.settings")
django.setup()

# -------------------------------
# Imports nach Django-Setup
# -------------------------------
from fleet.models import Aircraft
from components.models import Component, Requirement, Installation

# -------------------------------
# Hilfsfunktion: Flugstunden verteilen
# -------------------------------
def add_flight_hours(aircraft, flight_hours):
    """
    Addiert flight_hours auf alle aktuell eingebauten Komponenten eines Aircraft.
    TSN (Total since new) und TSI (Time since installation) werden aktualisiert.
    """
    for inst in aircraft.installations.filter(removed_at__isnull=True):
        comp = inst.component
        comp.tsn += flight_hours
        comp.tsi += flight_hours
        comp.save()
        print(f"Added {flight_hours}h to {comp} (TSN: {comp.tsn}, TSI: {comp.tsi})")

# -------------------------------
# Testdaten erstellen und Ablauf simulieren
# -------------------------------
def run_test():
    # 1️⃣ Aircraft erstellen
    ac, created = Aircraft.objects.get_or_create(
        registration="D-TEST",
        defaults={"manufacturer": "TestAir", "type": "TA-100"}
    )
    print(f"Aircraft: {ac} (created={created})")

    # 2️⃣ Requirements erstellen
    req1, _ = Requirement.objects.get_or_create(name="Inspection 500 FH", interval_fh=500)
    req2, _ = Requirement.objects.get_or_create(name="Overhaul 2500 FH", interval_fh=2500)

    # 3️⃣ Components erstellen
    comp1, _ = Component.objects.get_or_create(
        part="Engine",
        part_number="ENG-001",
        serial_number="E100",
        tsn=1000,
        tso=500,
        tsi=0
    )
    comp1.requirements.add(req1, req2)

    comp2, _ = Component.objects.get_or_create(
        part="Landing Gear",
        part_number="LG-001",
        serial_number="LG100",
        tsn=200,
        tso=0,
        tsi=0
    )
    comp2.requirements.add(req1)

    # 4️⃣ Komponenten einbauen
    today = datetime.date.today()
    inst1, _ = Installation.objects.get_or_create(
        aircraft=ac,
        component=comp1,
        installed_at=today
    )
    inst2, _ = Installation.objects.get_or_create(
        aircraft=ac,
        component=comp2,
        installed_at=today
    )

    print("Components installed.")

    # 5️⃣ Flugstunden hinzufügen
    add_flight_hours(ac, 5)  # 5 FH Flug
    add_flight_hours(ac, 3)  # 3 FH Flug

    # 6️⃣ Eine Komponente ausbauen
    inst2.removed_at = today + datetime.timedelta(days=1)
    inst2.save()
    print(f"{inst2.component} removed from {inst2.aircraft}.")

    # 7️⃣ Weitere Flugstunden
    add_flight_hours(ac, 2)  # nur Engine bekommt weitere FH

# -------------------------------
# Skript ausführen
# -------------------------------
if __name__ == "__main__":
    run_test()
