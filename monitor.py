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
    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    page.goto(
        "https://gestiona.comunidad.madrid/ctac_cita/registro#",
        wait_until="networkidle"
    )

    page.wait_for_timeout(3000)

    # Solicitar cita
    page.get_by_role(
        "link",
        name="SOLICITAR CITA"
    ).click()

    page.wait_for_timeout(3000)

    # Registro Civil de Getafe (222)
    page.locator("#combo1").evaluate(
        "(el) => { el.value = '222'; el.dispatchEvent(new Event('change', { bubbles: true })); }"
    )

    page.wait_for_timeout(3000)

    # Apertura Expedientes de Matrimonio (434)
    page.locator("#comboServicios").evaluate(
        "(el) => { el.value = '434'; el.dispatchEvent(new Event('change', { bubbles: true })); }"
    )

    page.wait_for_timeout(3000)

    # Continuar
    page.locator('input[value="Continuar"]').first.click()

    page.wait_for_timeout(8000)

    texto = page.locator("body").inner_text()

    mensagem_indisponibilidade = (
        "No hay disponibilidad de cita para el servicio"
    )

    if mensagem_indisponibilidade in texto:
        print("Sem vagas disponíveis.")
    else:
        send_telegram(
            "🚨 POSSÍVEL VAGA ENCONTRADA!\n\n"
            "Registro Civil de Getafe\n"
            "Apertura Expedientes de Matrimonio\n\n"
            "Acesse imediatamente:\n"
            "https://gestiona.comunidad.madrid/ctac_cita/registro#"
        )

    browser.close()
