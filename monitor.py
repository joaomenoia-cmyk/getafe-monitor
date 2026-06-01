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
# TESTE
send_telegram("✅ Teste do monitor Getafe")

exit ()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://gestiona.comunidad.madrid/ctac_cita/registro#",
        wait_until="networkidle"
    )

    # Aguarda carregamento dos combos
    page.wait_for_timeout(3000)

    content = page.content().lower()

    if "registro civil de getafe" not in content:
        send_telegram(
            "⚠️ O monitor não conseguiu localizar os elementos da página. Verifique o portal."
        )

    if "no hay disponibilidad de cita" not in content:
        send_telegram(
            "🚨 ATENÇÃO!\n\n"
            "Possível vaga detectada para Apertura de Expedientes de Matrimonio em Getafe.\n\n"
            "Acesse imediatamente:\n"
            "https://gestiona.comunidad.madrid/ctac_cita/registro#"
        )

    browser.close()
