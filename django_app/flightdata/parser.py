import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import django

# Django initialisieren
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "open_camo.settings")
django.setup()
from fleet.models import Aircraft
from django.conf import settings

MAX_RETRIES = 3

def create_driver():
    """Chrome WebDriver erstellen."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Kann für Debugging weggelassen werden
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(driver, timeout=15):
    """Login an der Webseite mit Selenium."""
    driver.get(settings.PARSER_LOGIN_URL)
    wait = WebDriverWait(driver, timeout)

    try:
        # Optional: Cookie-Hinweis schließen
        try:
            cookie_close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close-cookie")))
            cookie_close.click()
        except TimeoutException:
            pass

        # Benutzername und Passwort-Felder
        username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        password_input = wait.until(EC.visibility_of_element_located((By.NAME, "passwort")))

        username_input.clear()
        username_input.send_keys(settings.PARSER_USERNAME)
        password_input.clear()
        password_input.send_keys(settings.PARSER_PASSWORD)

        # Login-Button klicken
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()

        # Prüfen, ob Login erfolgreich war
        wait.until(EC.url_changes(settings.PARSER_LOGIN_URL))
        print(f"[{datetime.now()}] Login erfolgreich")
        return True

    except (TimeoutException, ElementClickInterceptedException) as e:
        print(f"[{datetime.now()}] [ERROR] Login-Fehler: {e}")
        return False

def logout(driver):
    """Optionaler Logout."""
    logout_url = getattr(settings, "PARSER_LOGOUT_URL", None)
    if logout_url:
        try:
            driver.get(logout_url)
        except:
            pass

def fetch_aircraft_data(driver):
    """Flugdaten abrufen und HH:MM extrahieren."""
    driver.get(settings.PARSER_DATA_URL)
    wait = WebDriverWait(driver, 15)

    try:
        table_rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
    except TimeoutException:
        print(f"[{datetime.now()}] [ERROR] tbody der Tabelle nicht gefunden")
        return []

    records = []
    for tr in table_rows:
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) < 3:
            continue
        reg = tds[0].text.strip()
        flight_hours_text = tds[2].text.strip()  # z.B. "5732 h 35 m"

        # hh:mm extrahieren
        try:
            parts = flight_hours_text.replace("h", "").replace("m", "").split()
            hours = int(parts[0])
            minutes = int(parts[1])
            flight_hours = f"{hours}:{minutes:02d}"
        except Exception as e:
            print(f"[{datetime.now()}] [WARN] Fehler beim Parsen der Flugstunden für {reg}: {e}")
            flight_hours = None

        records.append({"registration": reg, "flight_hours": flight_hours})
    return records

def update_aircraft(records):
    """Flugstunden in die DB schreiben – nur bei Änderung."""
    for rec in records:
        reg = rec["registration"]
        hours = rec["flight_hours"]
        if not hours:
            continue
        try:
            aircraft = Aircraft.objects.get(registration=reg)
            if str(aircraft.tfh) != hours:
                aircraft.tfh = hours
                aircraft.save()
                print(f"[{datetime.now()}] {reg}: Flugstunden auf {hours} aktualisiert")
        except Aircraft.DoesNotExist:
            print(f"[{datetime.now()}] [WARN] Flugzeug {reg} nicht gefunden")

def run_parser_once():
    """Einmaliger Parserlauf mit Retry bei Login/Netzwerkproblemen."""
    print(f"[{datetime.now()}] Starte Parserlauf...")
    driver = create_driver()
    retries = 0
    success = False

    while retries < MAX_RETRIES and not success:
        try:
            if not login(driver):
                retries += 1
                print(f"[{datetime.now()}] Retry {retries}/{MAX_RETRIES} in 5 Sekunden...")
                time.sleep(5)
                continue

            records = fetch_aircraft_data(driver)
            update_aircraft(records)
            success = True

        except Exception as e:
            retries += 1
            print(f"[{datetime.now()}] [ERROR] Parserfehler: {e} – Retry {retries}/{MAX_RETRIES} in 5 Sekunden...")
            time.sleep(5)
        finally:
            logout(driver)

    driver.quit()

    if not success:
        print(f"[{datetime.now()}] Parserlauf gescheitert nach {MAX_RETRIES} Versuchen")
    else:
        print(f"[{datetime.now()}] Parserlauf abgeschlossen.")

def run_parser_loop(interval_minutes=10):
    """Parser alle X Minuten laufen lassen."""
    while True:
        run_parser_once()
        print(f"[{datetime.now()}] Warte {interval_minutes} Minuten bis zum nächsten Lauf...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    run_parser_loop()
