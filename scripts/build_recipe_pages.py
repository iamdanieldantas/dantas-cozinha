"""Generate standalone, crawlable recipe pages in the Pages build directory."""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote, urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

from build_dataset import assemble

BASE = "https://iamdanieldantas.github.io/dantas-cozinha/"


def generate(destination: Path) -> int:
    recipes = assemble()["recipes"]
    destination.mkdir(parents=True, exist_ok=True)
    sitemap = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for url in [BASE]:
        SubElement(SubElement(sitemap, "url"), "loc").text = url
    seen = set()
    for recipe in recipes:
        slug = recipe["id"]
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Unsafe recipe id: {slug!r}")
        if slug in seen:
            raise ValueError(f"Duplicate recipe id: {slug}")
        seen.add(slug)
        url = BASE + "receitas/" + quote(slug) + "/"
        title = escape(recipe["title"])
        description = escape(recipe.get("description") or "Receita do Dantas Cozinha")
        ingredients = []
        for item in recipe.get("ingredients", []):
            if isinstance(item, str):
                ingredients.append(item)
            else:
                qty = item.get("quantity", "")
                unit = item.get("unit", "")
                name = item.get("name", "")
                ingredients.append(" ".join(str(x) for x in (qty, unit, name) if x is not None and x != ""))
        steps = [str(step) for step in recipe.get("steps", [])]
        if not ingredients or not steps:
            raise ValueError(f"Incomplete recipe: {slug}")
        instructions = "".join("<li>" + escape(step) + "</li>" for step in steps)
        ingredient_html = "".join("<li>" + escape(item) + "</li>" for item in ingredients)
        app_url = BASE + "#receita/" + quote(slug)
        image_url = recipe.get("image", "")
        parsed_image = urlparse(image_url) if isinstance(image_url, str) else None
        image_html = ""
        if parsed_image and parsed_image.scheme == "https" and parsed_image.netloc:
            image_credit = escape(recipe.get("imageCredit") or "Crédito não informado")
            image_source_url = recipe.get("imageSourceUrl", "")
            image_license_url = recipe.get("imageLicenseUrl", "")
            source_link = (f'<a href="{escape(image_source_url, quote=True)}" rel="noopener noreferrer">fonte da imagem</a>' if urlparse(image_source_url).scheme == "https" and urlparse(image_source_url).netloc else "")
            license_link = (f'<a href="{escape(image_license_url, quote=True)}" rel="noopener noreferrer">licença</a>' if urlparse(image_license_url).scheme == "https" and urlparse(image_license_url).netloc else "")
            attribution_links = " · ".join(link for link in (source_link, license_link) if link)
            image_html = f'<figure class="recipe-hero"><img src="{escape(image_url, quote=True)}" alt="{title}" loading="eager"><figcaption>Imagem ilustrativa · {image_credit} {("· " + attribution_links) if attribution_links else ""}</figcaption></figure>'
        source_url = recipe.get("sourceUrl", "")
        parsed_source = urlparse(source_url) if isinstance(source_url, str) else None
        source_link = (f'<p>Referência: <a href="{escape(source_url, quote=True)}" rel="noopener noreferrer">{escape(recipe.get("source") or "Fonte original")}</a></p>' if parsed_source and parsed_source.scheme == "https" and parsed_source.netloc else "")
        # Only include attributes supported by the editorial dataset; no ratings or fabricated imagery.
        schema = {
            "@context": "https://schema.org",
            "@type": "Recipe",
            "name": recipe["title"],
            "description": recipe.get("description", ""),
            "inLanguage": "pt-BR",
            "recipeIngredient": ingredients,
            "recipeInstructions": [{"@type": "HowToStep", "text": step} for step in steps],
            "url": url,
        }
        if isinstance(recipe.get("servings"), (int, float)) and recipe["servings"] > 0:
            schema["recipeYield"] = str(recipe["servings"]) + " porções"
        if isinstance(recipe.get("minutes"), (int, float)) and recipe["minutes"] > 0:
            schema["totalTime"] = "PT" + str(int(recipe["minutes"])) + "M"
        structured = json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")
        page = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} • Dantas Cozinha</title><meta name="description" content="{description}">
<link rel="canonical" href="{url}"><meta property="og:type" content="article">
<meta property="og:title" content="{title} • Dantas Cozinha"><meta property="og:description" content="{description}">
<meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{structured}</script>
<style>body{{margin:0;background:#faf6ef;color:#33342d;font:16px/1.75 system-ui,sans-serif}}main{{max-width:780px;margin:0 auto;padding:32px 22px 70px}}h1,h2{{font-family:Georgia,serif;color:#2e4838;line-height:1.2}}h1{{font-size:clamp(34px,5vw,54px)}}a{{color:#a54d2f}}.brand{{font-weight:750;color:#2e4838}}.intro{{font-size:18px}}.panel{{background:#fffdf8;border:1px solid #e9e3d9;border-radius:18px;padding:24px;margin:25px 0}}.recipe-hero{{margin:24px 0}}.recipe-hero img{{display:block;width:100%;height:auto;border-radius:16px}}.recipe-hero figcaption{{font-size:13px;color:#68685f;margin-top:8px}}li{{margin-bottom:9px}}a:focus-visible{{outline:3px solid #a54d2f;outline-offset:3px}}</style>
</head><body><main><nav aria-label="Navegação"><a class="brand" href="{BASE}">Dantas Cozinha</a> / Receitas</nav>
<article><h1>{title}</h1><p class="intro">{description}</p>{image_html}
<p>Rendimento: {escape(str(recipe.get("servingsLabel") or str(recipe.get("servings", "Não informado")) + " porções"))}</p>
<section class="panel"><h2>Ingredientes</h2><ul>{ingredient_html}</ul></section>
<section class="panel"><h2>Modo de preparo</h2><ol>{instructions}</ol></section>
<p><a href="{app_url}">Abrir versão interativa: ajustar porções, salvar favoritos e planejar</a></p>
{source_link}<p><small>Conteúdo editorial informativo. Consulte a referência original quando indicada no catálogo.</small></p></article></main></body></html>"""
        target = destination / "receitas" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        SubElement(SubElement(sitemap, "url"), "loc").text = url
    ElementTree(sitemap).write(destination / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    return len(seen)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    count = generate(args.out)
    print(f"Generated {count} recipe pages and sitemap at {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
