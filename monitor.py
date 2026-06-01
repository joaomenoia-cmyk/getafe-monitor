import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://gestiona.comunidad.madrid/ctac_cita/registro#",
        wait_until="networkidle"
    )

    page.wait_for_timeout(3000)

    page.get_by_role("link", name="SOLICITAR CITA").click()

    page.wait_for_timeout(3000)

    page.locator("#combo1").evaluate(
        "(el) => { el.value = '222'; el.dispatchEvent(new Event('change', { bubbles: true })); }"
    )

    page.wait_for_timeout(3000)

    page.locator("#comboServicios").evaluate(
        "(el) => { el.value = '434'; el.dispatchEvent(new Event('change', { bubbles: true })); }"
    )

    page.wait_for_timeout(5000)

    print("=== HTML COMPLETO APÓS SERVIÇO ===")
    print(page.content())

    browser.close()
