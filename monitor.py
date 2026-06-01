import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://gestiona.comunidad.madrid/ctac_cita/registro#",
        wait_until="networkidle"
    )
    page.wait_for_timeout(3000)

    # Seleciona Getafe

    page.select_option("#combo1", value="222")

    page.wait_for_timeout(5000)

    print("=== TODOS OS SELECTS ===")

    for select in page.locator("select").all():
        print("ID:", select.get_attribute("id"))
        print("-------------------")
