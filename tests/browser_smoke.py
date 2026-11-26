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
            assert desktop.locator("#recipe-list .recipe-card").count() == len(recipes)
            assert desktop.locator("#recipe-list .curated-card").count() == 0
            latest_recipe = sorted(recipes, key=lambda item: item.get("createdAt", ""), reverse=True)[0]
            assert latest_recipe["title"] in desktop.locator("#recipe-list .recipe-card").first.inner_text()
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
            # Search must open the standalone lesson, not the former inline accordion.
            desktop.locator('[data-search-kind="aulas"]').click()
            desktop.locator("#unified-search").fill(techniques[0]["title"])
            result = desktop.locator(f'[data-unified-open="{techniques[0]["id"]}"][data-unified-type="aula"]')
            result.wait_for()
            result.click()
            desktop.locator("#school-lesson-detail h1").wait_for()
            assert desktop.locator('[data-view="aula"]').is_visible()
            assert desktop.locator("#school-lesson-detail h1").inner_text() == techniques[0]["title"]
            assert desktop.evaluate("location.hash") == "#aula/" + techniques[0]["id"]
            desktop.goto(base + "#tecnicas", wait_until="domcontentloaded")
            assert desktop.locator("#school-progress-bar").get_attribute("aria-valuenow") is not None
            categories = list(dict.fromkeys(item["category"] for item in techniques))
            assert desktop.locator("#school-filters .school-module-card").count() == len(categories)
            assert desktop.locator("#tech-grid .school-lesson-link").count() == 0
            assert desktop.locator('#school-filters [data-school-category="todas"]').is_visible()
            covers = desktop.locator("#school-filters .school-module-card img").all()
            assert len(covers) == len(categories)
            for cover in covers:
                cover.evaluate("img => img.loading = 'eager'")
                cover.evaluate("img => img.decode()")
                assert cover.evaluate("img => img.naturalWidth") > 0
            desktop.locator("#school-filters .school-module-card").first.click()
            desktop.locator("#tech-grid .school-lesson-link").first.wait_for()
            assert desktop.locator("#tech-grid .school-lesson-link").count() == sum(
                item["category"] == categories[0] for item in techniques)
            desktop.locator("#tech-grid .school-lesson-link").first.click()
            desktop.locator("#school-lesson-detail h1").wait_for()
            assert desktop.locator('[data-view="aula"]').is_visible()
            assert desktop.locator("#school-lesson-detail h1").inner_text() == techniques[0]["title"]
            assert desktop.locator("#school-lesson-detail .tech-lesson").count() >= 3
            desktop.locator("[data-lesson-complete]").click()
            assert desktop.locator("[data-lesson-complete]").get_attribute("aria-pressed") == "true"
            desktop.reload(wait_until="domcontentloaded")
            assert desktop.locator("[data-lesson-complete]").get_attribute("aria-pressed") == "true"
            desktop.locator("[data-lesson-complete]").click()
            desktop.go_back(wait_until="domcontentloaded")
            desktop.locator("#tech-grid .school-lesson-link").first.wait_for()
            assert desktop.locator("#tech-grid .school-lesson-link").count() == sum(
                item["category"] == categories[0] for item in techniques)
            desktop.locator('[data-school-category="modulos"]').click()
            desktop.locator("#school-filters .school-module-card").first.wait_for()
            # All lessons use the same hierarchy and sibling actions at both ends.
            for lesson in techniques:
                desktop.goto(base + "#aula/" + lesson["id"], wait_until="domcontentloaded")
                desktop.locator("#school-lesson-detail h1").wait_for()
                top = desktop.locator('[data-school-nav="top"]')
                bottom = desktop.locator('[data-school-nav="bottom"]')
                assert top.count() == bottom.count() == 1
                assert top.inner_text() == bottom.inner_text()
                module_lessons = [item for item in techniques if item["category"] == lesson["category"]]
                index = next(i for i, item in enumerate(module_lessons) if item["id"] == lesson["id"])
                for nav in (top, bottom):
                    assert nav.locator("[data-school-prev]").count() == int(index > 0)
                    assert nav.locator("[data-school-next]").count() == int(index < len(module_lessons) - 1)
                    assert nav.locator(".school-nav-dropdown, .school-breadcrumb").count() == 0
                    assert nav.locator("[data-school-parent]").count() == 1
                    assert nav.locator("a").count() == 1 + int(index > 0) + int(index < len(module_lessons) - 1)
                    assert nav.locator("[data-school-parent]").get_attribute("href") == top.locator("[data-school-parent]").get_attribute("href")
                bottom.locator("[data-school-parent]").click()
                desktop.locator("#tech-grid .school-lesson-link").first.wait_for()
                assert desktop.locator("#tech-grid .school-lesson-link").count() == len(module_lessons)
                assert desktop.locator("#school-filters a").count() == 1
                assert desktop.locator(".school-module-return").count() == 0
                assert not desktop.locator("#school-next-lesson").is_visible()
                desktop.locator('#school-filters [data-school-category="modulos"]').click()
                desktop.locator("#school-filters .school-module-card").first.wait_for()
            desktop.locator("#school-search").fill(techniques[-1]["title"])
            assert desktop.locator("#tech-grid .school-lesson-link").count() >= 1
            desktop.locator("#school-search").fill("")
            desktop.locator("#school-next-lesson").click()
            desktop.locator("#school-lesson-detail h1").wait_for()
            desktop.goto(base + "#tecnicas/todas", wait_until="domcontentloaded")
            desktop.locator("#tech-grid .school-lesson-link").first.wait_for()
            assert desktop.locator("#tech-grid .school-lesson-link").count() == len(techniques)
            for topic in ("Antipasto, entrada, couvert e aperitivo",
                          "Contaminação direta dos alimentos",
                          "Contaminação cruzada: direta e indireta"):
                lesson = desktop.locator("#tech-grid .school-lesson-link").filter(has_text=topic)
                assert lesson.count() == 1, "Aula essencial ausente: " + topic
                lesson.click()
                desktop.locator("#school-lesson-detail h1").wait_for()
                assert desktop.locator("#school-lesson-detail h1").inner_text() == topic
                desktop.goto(base + "#tecnicas/todas", wait_until="domcontentloaded")
                desktop.locator("#tech-grid .school-lesson-link").first.wait_for()

            desktop.goto(base + "#aula/escola-facas-cortes", wait_until="domcontentloaded")
            visual_lesson = desktop.locator("#escola-escola-facas-cortes")
            visual_lesson.wait_for()
            for image in visual_lesson.locator("img[src^='assets/school-']").all():
                image.evaluate("img => img.loading = 'eager'")
                image.evaluate("img => img.decode()")
                assert image.evaluate("img => img.naturalWidth") > 0
            desktop.goto(base + "#aula/escola-molhos-derivados", wait_until="domcontentloaded")
            family_lesson = desktop.locator("#escola-escola-molhos-derivados")
            family_lesson.wait_for()
            family = family_lesson.locator("[data-school-family]").filter(has_text="Holandês")
            assert family.get_attribute("aria-expanded") == "false"
            family.click()
            assert family.get_attribute("aria-expanded") == "true"
            assert family_lesson.get_by_text("Béarnaise", exact=True).first.is_visible()
            other = family_lesson.locator("[data-school-family]").first
            other.click()
            assert other.get_attribute("aria-expanded") == "true"
            assert family.get_attribute("aria-expanded") == "false"
            other.click()
            assert other.get_attribute("aria-expanded") == "false"

            mobile = browser.new_page(
                viewport={"width": 390, "height": 844}, device_scale_factor=1,
                is_mobile=True, has_touch=True
            )
            mobile.on("pageerror", lambda err: errors.append("mobile: " + str(err)))
            mobile.route("https://**/*", lambda route: route.abort())
            mobile.goto(base + "#receitas", wait_until="domcontentloaded")
            assert mobile.locator("#recipe-list .recipe-card").count() == len(recipes)
            assert mobile.locator("#recipe-list .curated-card").count() == 0
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
            mobile.goto(base + "#tecnicas", wait_until="domcontentloaded")
            assert mobile.locator("#school-filters .school-module-card").count() == len(categories)
            mobile.locator("#school-filters .school-module-card").first.click()
            mobile.locator("#tech-grid .school-lesson-link").first.wait_for()
            assert mobile.locator("#tech-grid .school-lesson-link").count() == sum(
                item["category"] == categories[0] for item in techniques)
            mobile.locator("#tech-grid .school-lesson-link").first.click()
            mobile.locator("#school-lesson-detail h1").wait_for()
            assert mobile.locator('[data-view="aula"]').is_visible()
            assert mobile.evaluate("document.documentElement.scrollWidth <= innerWidth")
            top = mobile.locator('[data-school-nav="top"]')
            bottom = mobile.locator('[data-school-nav="bottom"]')
            assert top.inner_text() == bottom.inner_text()
            for nav in (top, bottom):
                assert nav.locator(".school-nav-dropdown, .school-breadcrumb").count() == 0
                assert nav.locator("[data-school-parent]").is_visible()
            assert mobile.evaluate("document.documentElement.scrollWidth <= innerWidth")
            bottom.locator("[data-school-parent]").click()
            mobile.locator("#tech-grid .school-lesson-link").first.wait_for()
            assert mobile.locator("#school-filters a").count() == 1
            assert not mobile.locator("#school-next-lesson").is_visible()
            mobile.locator('#school-filters [data-school-category="modulos"]').click()
            mobile.locator("#school-filters .school-module-card").first.wait_for()
            assert mobile.locator("#school-filters .school-module-card").count() == len(categories)
            assert not errors, "Erros JavaScript: " + repr(errors)
            print("SMOKE OK: desktop/mobile, curadoria, receitas completas, notas, Escola e oficinas")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    run()
