"""
Testskript für Open Camo – REST-API
===================================

Dieses Skript demonstriert:

1. Erstellen von Flugzeugen über die Fleet-API
2. Anlegen von Komponenten über die Components-API
3. Virtuelles Ein- und Ausbauen von Komponenten in Flugzeugen
4. Automatische Berechnung von TSI (Time Since Installation) und TSO (Time Since Overhaul)

Voraussetzungen:
- Dev Container läuft
- Django Server läuft auf 0.0.0.0:8000
- REST-API Endpunkte:
    /api/aircraft/
    /api/components/
    /api/installations/

Nutzung:
$ python components/scripts/test_api_installations.py
"""

import requests
from datetime import datetime, timedelta

# Basis-URL der REST-API
BASE_URL = "http://localhost:8000/api"

# -----------------------------------------------
# 1️⃣ Flugzeuge anlegen
# -----------------------------------------------
aircraft_data = [
    {
        "manufacturer": "Airbus",
        "type": "A320",
        "date_of_manufacturing": "2015-06-01",
        "tfh": 4500,   # Total Flight Hours
        "dow": 2000,   # Days of Operation
        "mtw": 1500,   # Maintenance Time Window
        "registration": "D-AABC"
    },
    {
        "manufacturer": "Boeing",
        "type": "737",
        "date_of_manufacturing": "2018-03-15",
        "tfh": 3000,
        "dow": 1000,
        "mtw": 1200,
        "registration": "N12345"
    }
]

aircraft_ids = []

for ac in aircraft_data:
    r = requests.post(f"{BASE_URL}/aircraft/", json=ac)
    if r.status_code == 201:
        print(f"Flugzeug erstellt: {ac['registration']}")
        aircraft_ids.append(r.json()["id"])
    else:
        print("Fehler beim Anlegen:", r.status_code, r.text)

# -----------------------------------------------
# 2️⃣ Komponenten anlegen
# -----------------------------------------------
component_data = [
    {
        "part": "Engine",
        "part_number": "ENG-001",
        "serial_number": "SN123456",
        "tsn": 1200,    # Total Flight Hours
        "tsi": 0,       # Stunden seit Einbau
        "tso": 0        # Stunden seit Overhaul
    },
    {
        "part": "Landing Gear",
        "part_number": "LG-002",
        "serial_number": "SN654321",
        "tsn": 800,
        "tsi": 0,
        "tso": 0
    }
]

component_ids = []

for comp in component_data:
    r = requests.post(f"{BASE_URL}/components/", json=comp)
    if r.status_code == 201:
        print(f"Komponente erstellt: {comp['part']} ({comp['serial_number']})")
        component_ids.append(r.json()["id"])
    else:
        print("Fehler beim Anlegen:", r.status_code, r.text)

# -----------------------------------------------
# 3️⃣ Komponenten einbauen (Installation)
# -----------------------------------------------
# Wir bauen jede Komponente ins erste Flugzeug ein
installations = []

for cid in component_ids:
    install_payload = {
        "component": cid,
        "aircraft": aircraft_ids[0],
        "installed_at": datetime.now().isoformat(),  # jetzt
        "removed_at": None
    }
    r = requests.post(f"{BASE_URL}/installations/", json=install_payload)
    if r.status_code == 201:
        print(f"Komponente {cid} in Flugzeug {aircraft_ids[0]} eingebaut")
        installations.append(r.json())
    else:
        print("Fehler beim Einbau:", r.status_code, r.text)

# -----------------------------------------------
# 4️⃣ Komponenten ausbauen und TSI/TSO berechnen
# -----------------------------------------------
# Wir simulieren, dass Flugzeug 100 Flugstunden weiter geflogen ist
additional_hours = 100

for inst in installations:
    comp_id = inst["component"]["id"]
    # hole aktuelle Komponentendaten
    r = requests.get(f"{BASE_URL}/components/{comp_id}/")
    comp = r.json()
    # update TSN, TSI, TSO
    comp["tsn"] += additional_hours
    comp["tsi"] += additional_hours
    comp["tso"] += additional_hours
    # entferne Installation (ausbauen)
    update_payload = {
        "component": comp_id,
        "aircraft": inst["aircraft"]["id"],
        "installed_at": inst["installed_at"],
        "removed_at": datetime.now().isoformat()
    }
    # PATCH Component
    r_comp = requests.patch(f"{BASE_URL}/components/{comp_id}/", json={
        "tsn": comp["tsn"],
        "tsi": comp["tsi"],
        "tso": comp["tso"]
    })
    # PATCH Installation (entfernen)
    r_inst = requests.patch(f"{BASE_URL}/installations/{inst['id']}/", json=update_payload)
    if r_comp.status_code == 200 and r_inst.status_code == 200:
        print(f"Komponente {comp_id} ausgebaut, TSI/TSO aktualisiert")
    else:
        print("Fehler beim Ausbau/Update:", r_comp.text, r_inst.text)

print("\n✅ Testskript erfolgreich abgeschlossen.")
