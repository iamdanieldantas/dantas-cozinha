"""Valida o site real em desktop e celular, incluindo rotas das receitas."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
import threading

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run():
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/index.html"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            errors = []
            desktop = browser.new_page(viewport={"width": 1440, "height": 900})
            desktop.on("pageerror", lambda error: errors.append(str(error)))
            desktop.route("https://**/*", lambda route: route.abort())
            desktop.goto(base, wait_until="domcontentloaded")
            desktop.locator("#home-recipes .recipe-card").first.wait_for()
            assert desktop.locator("#home-recipes .recipe-card").count() == 3

            desktop.locator(".hero-actions [data-goto='receitas']").click()
            assert desktop.locator("#recipe-list .recipe-card").count() == 26
            assert desktop.locator("#curation-list .curation-card").count() == 3, "Seleções da semana ausentes"
            assert desktop.locator("#curation-list a[href='https://panelinha.com.br/receita/empanadas-de-carne']").count() == 1
            assert desktop.locator("#curation-list .curation-ingredients li").count() >= 10
            assert desktop.locator("#curation-list .detail-steps").count() == 0
            desktop.locator("#recipe-search").fill("brownie")
            assert desktop.locator("#recipe-list .recipe-card").count() >= 3

            recipe_id = "adaptacao-brownie-forma-20x30"
            desktop.locator(f"#recipe-list button.inline-link[data-recipe='{recipe_id}']").click()
            assert desktop.locator('[data-view="receita"]').is_visible(), "Página completa não visível"
            assert desktop.locator("#recipe-detail h1").inner_text().startswith("Brownie de chocolate")
            assert desktop.locator("#ingredients-list .ingredient-entry").count() == 9, "Ingredientes ausentes"
            assert desktop.locator("#recipe-detail .detail-steps li").count() == 7, "Modo de preparo ausente"
            assert desktop.locator("#serving-number").inner_text() == "12"
            desktop.locator("#serving-plus").click()
            assert desktop.locator("#serving-number").inner_text() == "13"
            desktop.locator("#recipe-note").fill("Fiz o teste da página completa.")
            desktop.locator(".detail-back").click()
            desktop.goto(base + "#receita/" + recipe_id, wait_until="domcontentloaded")
            assert desktop.locator("#ingredients-list .ingredient-entry").count() == 9, "Falha ao abrir link direto"
            assert desktop.locator("#recipe-note").input_value() == "Fiz o teste da página completa."

            desktop.goto(base + "#tecnicas", wait_until="domcontentloaded")
            desktop.locator("#tech-grid details").first.locator("summary").click()
            assert desktop.locator("#tech-grid details").first.get_attribute("open") is not None
            assert desktop.locator("#tech-grid details").first.locator(".tech-lesson").count() >= 3

            mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
            mobile.on("pageerror", lambda error: errors.append("mobile: " + str(error)))
            mobile.route("https://**/*", lambda route: route.abort())
            mobile.goto(base + "#receitas", wait_until="domcontentloaded")
            assert mobile.locator("#recipe-list .recipe-card").count() == 26
            assert mobile.locator("#curation-list .curation-card").count() == 3
            mobile.goto(base + "#workshops", wait_until="domcontentloaded")
            assert mobile.locator("#workshop-list .workshop-card").count() == 9
            mobile.goto(base + "#receitas", wait_until="domcontentloaded")
            mobile.locator("#recipe-list button.inline-link[data-recipe='curadoria-torta-de-frango-classica']").click()
            assert mobile.locator("#recipe-detail h1").inner_text() == "Torta de frango clássica"
            assert mobile.locator("#ingredients-list .ingredient-entry").count() >= 10
            assert mobile.locator("#recipe-detail .detail-steps li").count() >= 7
            assert mobile.locator("#recipe-detail").is_visible()

            assert not errors, "Erros JavaScript no navegador: " + repr(errors)
            print("SMOKE OK: desktop, celular, curadoria verificada, oficinas, ingredientes, preparo, aulas e navegação direta")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    run()
