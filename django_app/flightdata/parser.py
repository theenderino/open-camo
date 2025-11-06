import os
import requests
from datetime import datetime
from django.conf import settings
from fleet.models import Aircraft

# ----------------------------------------
# HTTP Parser für Login + Datenabruf
# ----------------------------------------

def login_and_fetch_data():
    """
    Meldet sich mit Benutzername/Passwort an einer Webseite an
    und ruft aktuelle Flugstunden (TSN) für alle Flugzeuge ab.
    """

    login_url = settings.PARSER_LOGIN_URL
    data_url = settings.PARSER_DATA_URL
    username = settings.PARSER_USERNAME
    password = settings.PARSER_PASSWORD

    session = requests.Session()

    try:
        # 1️⃣ Login durchführen
        response = session.post(login_url, data={
            "username": username,
            "password": password,
        })
        response.raise_for_status()

        if "Login" in response.text:
            print("[ERROR] Login fehlgeschlagen – bitte Zugangsdaten prüfen.")
            return

        # 2️⃣ Daten abrufen (Beispiel: JSON-Antwort)
        response = session.get(data_url)
        response.raise_for_status()

        data = response.json()

    except Exception as e:
        print(f"[{datetime.now()}] Fehler beim Abrufen: {e}")
        return

    # 3️⃣ Daten in die Datenbank schreiben
    for record in data:
        reg = record.get("registration")
        hours = record.get("flight_hours")

        if not reg or hours is None:
            continue

        try:
            aircraft = Aircraft.objects.get(registration=reg)
            aircraft.tsn = hours
            aircraft.save()
            print(f"[{datetime.now()}] {reg}: TSN auf {hours} Std aktualisiert")
        except Aircraft.DoesNotExist:
            print(f"[WARN] Flugzeug {reg} nicht gefunden")


def run_parser():
    """Einfacher Wrapper zum manuellen Start."""
    print("Starte Parserlauf...")
    login_and_fetch_data()
    print("Parser abgeschlossen.")
