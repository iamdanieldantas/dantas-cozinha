"""Validação determinística dos conteúdos publicados. Sem dependências externas."""
from __future__ import annotations

import argparse
from datetime import date
import json
import math
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "assets" / "data.js"
PREFIX = "window.DANTAS_DATA = "
CATEGORIES = {"entrada", "principal", "sobremesa"}
KINDS = ("recipes", "techniques", "workshops", "videos", "curatedDiscoveries")


def load_data(path: Path = CONTENT) -> dict:
    source = path.read_text(encoding="utf-8").strip()
    if not source.startswith(PREFIX) or not source.endswith(";"):
        raise ValueError("assets/data.js deve exportar window.DANTAS_DATA = {...};")
    data = json.loads(source[len(PREFIX):-1])
    if not isinstance(data, dict):
        raise ValueError("A raiz do conteúdo deve ser objeto JSON.")
    return data


def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def is_date(value):
    if not isinstance(value, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def is_url(value):
    if not isinstance(value, str):
        return False
    url = urlparse(value)
    return url.scheme == "https" and bool(url.netloc) and not any(c.isspace() for c in value)


def validate(data: dict) -> dict:
    errors, warnings = [], []
    stats = {}
    if not isinstance(data, dict):
        return {"ok": False, "errors": ["Raiz deve ser um objeto."], "warnings": [], "counts": {}}

    required = {
        "recipes": ("id", "title", "category", "description", "difficulty", "tip", "createdAt", "source"),
        "techniques": ("id", "title", "category", "summary", "why", "practice", "createdAt", "deepDive"),
        "workshops": ("id", "name", "neighborhood", "address", "description", "tag", "verifiedAt"),
        "videos": ("id", "title", "topic", "description", "platform", "verifiedAt"),
        "curatedDiscoveries": ("id", "title", "category", "description", "author", "sourceName", "verifiedAt", "createdAt", "curationStatus"),
    }
    for kind in KINDS:
        rows = data.get(kind)
        if not isinstance(rows, list):
            errors.append(kind + ": precisa ser uma lista.")
            continue
        stats[kind] = len(rows)
        if kind in ("recipes", "techniques") and not rows:
            errors.append(kind + ": a lista não pode estar vazia.")
        ids, titles, source_urls = set(), set(), set()
        for index, row in enumerate(rows):
            label = f"{kind}[{index}]"
            if not isinstance(row, dict):
                errors.append(label + ": item precisa ser objeto.")
                continue
            for field in required[kind]:
                if not is_text(row.get(field)):
                    errors.append(label + f": campo {field} ausente ou vazio.")
            item_id = row.get("id")
            if is_text(item_id):
                if item_id in ids:
                    errors.append(label + ": ID duplicado: " + item_id)
                ids.add(item_id)
                label += f" ({item_id})"
            title = row.get("name" if kind == "workshops" else "title")
            if is_text(title):
                key = title.strip().casefold()
                if key in titles:
                    errors.append(label + ": título duplicado: " + title)
                titles.add(key)

            if kind == "recipes":
                if row.get("category") not in CATEGORIES:
                    errors.append(label + ": categoria de receita inválida.")
                for field in ("minutes", "servings"):
                    value = row.get(field)
                    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                        errors.append(label + f": {field} deve ser positivo.")
                ingredients = row.get("ingredients")
                if not isinstance(ingredients, list) or len(ingredients) < 2:
                    errors.append(label + ": ingredientes insuficientes.")
                else:
                    for i, ingredient in enumerate(ingredients):
                        if not isinstance(ingredient, dict):
                            errors.append(label + f": ingredients[{i}] precisa ser objeto.")
                            continue
                        amount = ingredient.get("quantity")
                        if type(amount) not in (int, float) or not math.isfinite(amount) or amount <= 0:
                            errors.append(label + f": quantidade inválida no ingrediente {i}.")
                        if not is_text(ingredient.get("unit")) or not is_text(ingredient.get("name")):
                            errors.append(label + f": unidade/nome ausente no ingrediente {i}.")
                steps = row.get("steps")
                if not isinstance(steps, list) or len(steps) < 2 or not all(is_text(x) for x in steps):
                    errors.append(label + ": modo de preparo precisa de etapas textuais.")
                if not is_url(row.get("image")):
                    errors.append(label + ": imagem deve usar uma URL HTTPS.")
                if "sourceUrl" in row and not is_url(row["sourceUrl"]):
                    errors.append(label + ": sourceUrl inválida.")
                if not is_date(row.get("createdAt")):
                    errors.append(label + ": createdAt deve ser YYYY-MM-DD.")

            elif kind == "techniques":
                if not is_date(row.get("createdAt")):
                    errors.append(label + ": createdAt inválida.")
                lessons = row.get("lesson")
                if not isinstance(lessons, list) or len(lessons) < 2:
                    errors.append(label + ": aula precisa de ao menos duas seções.")
                elif any(not isinstance(x, dict) or not is_text(x.get("heading")) or not is_text(x.get("body")) for x in lessons):
                    errors.append(label + ": lesson deve ter heading e body em cada seção.")
                mistakes = row.get("mistakes")
                if not isinstance(mistakes, list) or not mistakes or not all(is_text(x) for x in mistakes):
                    errors.append(label + ": mistakes deve conter erros comuns.")

            elif kind == "workshops":
                if not is_url(row.get("url")):
                    errors.append(label + ": URL da oficina inválida.")
                if not is_date(row.get("verifiedAt")):
                    errors.append(label + ": verifiedAt inválida.")
                event_date = row.get("eventDate")
                if event_date is not None and not is_date(event_date):
                    errors.append(label + ": eventDate deve ser data ISO ou null.")
                if "instagram" in row and row["instagram"] is not None and not is_url(row["instagram"]):
                    errors.append(label + ": Instagram inválido.")
                if is_date(event_date) and event_date < date.today().isoformat():
                    warnings.append(label + ": evento passado mantido no histórico (não deve aparecer no site).")

            elif kind == "videos":
                if not is_url(row.get("url")) or not is_date(row.get("verifiedAt")):
                    errors.append(label + ": vídeo sem URL oficial HTTPS ou data de verificação válida.")

            elif kind == "curatedDiscoveries":
                if row.get("category") not in CATEGORIES:
                    errors.append(label + ": categoria de curadoria inválida.")
                for field in ("sourceUrl",):
                    value = row.get(field)
                    if not is_url(value):
                        errors.append(label + f": {field} precisa ser HTTPS.")
                    elif value in source_urls:
                        errors.append(label + ": URL de fonte duplicada.")
                    else:
                        source_urls.add(value)
                for field in ("verifiedAt", "createdAt"):
                    if not is_date(row.get(field)):
                        errors.append(label + f": {field} inválida.")
                ingredients = row.get("mainIngredients")
                if not isinstance(ingredients, list) or not ingredients or not all(is_text(x) for x in ingredients):
                    errors.append(label + ": mainIngredients deve ser lista de nomes.")
                if "ingredients" in row or "steps" in row:
                    errors.append(label + ": ficha editorial não deve conter receita completa; use recipes somente com autoria e permissão.")

    if data.get("curationPolicy", {}).get("version", 0) < 2:
        errors.append("Política editorial verificada versão 2 não encontrada.")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "counts": stats}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=CONTENT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = validate(load_data(args.path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "errors": [str(exc)], "warnings": [], "counts": {}}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Contrato editorial:", "OK" if result["ok"] else "FALHOU", result["counts"])
        for message in result["errors"]:
            print("ERRO:", message)
        for message in result["warnings"]:
            print("AVISO:", message)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
