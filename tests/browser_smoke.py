"""Smoke tests desktop/mobile baseados nos dados reais, sem números fixos."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path
import threading
from urllib.parse import quote

from playwright.sync_api import sync_playwright

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
            desktop.on("pageerror", lambda err: errors.append(str(err)))
            desktop.route("https://**/*", lambda route: route.abort())
            desktop.goto(base + "#receitas", wait_until="domcontentloaded")
            desktop.locator("#recipe-list .recipe-card").first.wait_for()
            data = desktop.evaluate("window.DANTAS_DATA")
            recipes = data["recipes"]
            discoveries = data["curatedDiscoveries"]
            techniques = data["techniques"]
            assert recipes, "O catálogo de receitas está vazio"
            assert techniques, "A Escola está vazia"

            assert desktop.locator("#home-recipes .recipe-card").count() == min(3, len(recipes))
            assert desktop.locator("#recipe-list .recipe-card").count() == len(recipes) + len(discoveries)
            assert desktop.locator("#recipe-list .curated-card").count() == len(discoveries)
            assert "Risoto de cogumelos" in desktop.locator("#recipe-list .recipe-card").first.inner_text() or "Bolo de cenoura com especiarias" in desktop.locator("#recipe-list .recipe-card").first.inner_text()
            assert desktop.locator("#curation-list .curation-card").count() == len(discoveries)
            assert desktop.locator("#curation-list .curation-card a[href^='https://']").count() == len(discoveries)
            assert desktop.locator("#curation-list .curation-ingredients li").count() == sum(
                len(item["mainIngredients"]) for item in discoveries
            ), "Ingredientes da curadoria não correspondem aos dados"
            assert desktop.locator("#curation-list .detail-steps").count() == 0

            example = recipes[0]
            search = example["title"].split()[0]
            desktop.locator("#recipe-search").fill(search)
            assert desktop.locator("#recipe-list .recipe-card").count() >= 1
            desktop.locator("#recipe-search").fill("")
            desktop.locator(
                f"#recipe-list button.inline-link[data-recipe='{example['id']}']"
            ).click()
            assert desktop.locator('[data-view="receita"]').is_visible()
            assert desktop.locator("#recipe-detail h1").inner_text() == example["title"]
            assert desktop.locator("#ingredients-list .ingredient-entry").count() == len(example["ingredients"])
            assert desktop.locator("#recipe-detail .detail-steps li").count() == len(example["steps"])
            servings = int(example["servings"])
            assert desktop.locator("#serving-number").inner_text() == str(servings)
            desktop.locator("#serving-plus").click()
            assert desktop.locator("#serving-number").inner_text() == str(min(40, servings + 1))
            desktop.locator("#recipe-note").fill("Teste de persistência e navegação.")
            desktop.locator(".detail-back").click()
            assert desktop.locator('[data-view="receitas"]').is_visible()
            desktop.goto(base + "#receita/" + quote(example["id"]), wait_until="domcontentloaded")
            assert desktop.locator("#recipe-detail h1").inner_text() == example["title"]
            assert desktop.locator("#recipe-note").input_value() == "Teste de persistência e navegação."

            desktop.goto(base + "#inicio", wait_until="domcontentloaded")
            assert desktop.locator("#home-learning-progress").inner_text()
            desktop.goto(base + "#buscar", wait_until="domcontentloaded")
            desktop.locator("#unified-search").fill(example["title"].split()[0])
            assert desktop.locator("#unified-results .unified-result").count() >= 1
            desktop.goto(base + "#tecnicas", wait_until="domcontentloaded")
            assert desktop.locator("#school-progress-bar").get_attribute("aria-valuenow") is not None
            desktop.locator("#school-next-lesson").click()
            assert desktop.locator("#tech-grid details[open]").count() >= 1
            desktop.goto(base + "#tecnicas", wait_until="domcontentloaded")
            assert desktop.locator("#tech-grid details").count() == len(techniques)
            first = desktop.locator("#tech-grid details").first
            if first.get_attribute("open") is None:
                first.locator("summary").click()
            assert first.get_attribute("open") is not None
            assert first.locator(".tech-lesson").count() >= 3
            for topic in ("Antipasto, entrada, couvert e aperitivo",
                          "Contaminação direta dos alimentos",
                          "Contaminação cruzada: direta e indireta"):
                # São conteúdos mínimos do acervo. Qualquer alteração exige revisão editorial.
                lesson = desktop.locator("#tech-grid details").filter(
                    has=desktop.locator("summary h3", has_text=topic)
                )
                assert lesson.count() == 1, "Aula essencial ausente: " + topic
                if lesson.get_attribute("open") is None:
                    lesson.locator("summary").click()
                assert lesson.get_attribute("open") is not None

            mobile = browser.new_page(
                viewport={"width": 390, "height": 844}, device_scale_factor=1,
                is_mobile=True, has_touch=True
            )
            mobile.on("pageerror", lambda err: errors.append("mobile: " + str(err)))
            mobile.route("https://**/*", lambda route: route.abort())
            mobile.goto(base + "#receitas", wait_until="domcontentloaded")
            assert mobile.locator("#recipe-list .recipe-card").count() == len(recipes)
            assert mobile.locator("#curation-list .curation-card").count() == len(discoveries)
            mobile.goto(base + "#workshops", wait_until="domcontentloaded")
            expected = mobile.evaluate("""() => {
              const today = new Date();
              const ymd = [today.getFullYear(), String(today.getMonth()+1).padStart(2,'0'),
                String(today.getDate()).padStart(2,'0')].join('-');
              return window.DANTAS_DATA.workshops.filter(w => !w.eventDate || w.eventDate >= ymd).length;
            }""")
            assert mobile.locator("#workshop-list .workshop-card").count() == expected, (
                "Oficinas visíveis divergem da filtragem de datas"
            )
            mobile.goto(base + "#receitas", wait_until="domcontentloaded")
            mobile.locator(
                f"#recipe-list button.inline-link[data-recipe='{example['id']}']"
            ).click()
            assert mobile.locator("#recipe-detail h1").inner_text() == example["title"]
            assert mobile.locator("#ingredients-list .ingredient-entry").count() == len(example["ingredients"])
            assert mobile.locator("#recipe-detail .detail-steps li").count() == len(example["steps"])
            assert mobile.locator("#recipe-detail").is_visible()
            assert not errors, "Erros JavaScript: " + repr(errors)
            print("SMOKE OK: desktop/mobile, curadoria, receitas completas, notas, Escola e oficinas")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    run()
