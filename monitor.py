import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://gestiona.comunidad.madrid/ctac_cita/registro#"

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

response = requests.get(URL, timeout=30)

if response.status_code == 200:
    text = response.text.lower()

    if "no hay disponibilidad de cita" not in text:
        send_telegram(
            "🚨 POSSÍVEL VAGA DETECTADA!\n\n"
            "Verifique imediatamente:\n"
            "https://gestiona.comunidad.madrid/ctac_cita/registro#"
        )
