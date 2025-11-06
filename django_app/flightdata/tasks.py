# flightdata/tasks.py
import time
from .parser import fetch_flight_hours

def start_parser_loop(interval_minutes=10):
    """
    Führt den Parser periodisch aus.
    """
    while True:
        print("Starte Datenabruf...")
        fetch_flight_hours()
        print(f"Warte {interval_minutes} Minuten bis zum nächsten Lauf...")
        time.sleep(interval_minutes * 60)
