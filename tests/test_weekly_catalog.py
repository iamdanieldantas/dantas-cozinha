"""Regression checks: editorial selections stay separate from complete recipes."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class WeeklyCatalogTests(unittest.TestCase):
    def test_recent_curation_in_canonical_dataset(self):
        data=json.loads((ROOT/"content/curation.json").read_text(encoding="utf-8"))
        ids={r["id"] for r in data["curatedDiscoveries"]}
        self.assertIn("selecao-2026-11-09-risoto-cogumelos-salsinha",ids)
        self.assertIn("selecao-2026-11-09-bolo-cenoura-especiarias",ids)

    def test_catalog_keeps_discoveries_out_of_recipe_cards(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn("function renderCuratedDiscoveries()",app)
        self.assertIn("function renderRecipes()",app)
        self.assertIn("recipes.map(card)",app)
        self.assertNotIn("curatedCard(",app)
        self.assertNotIn("...curated.map(",app)
        self.assertIn("RECIPES.slice(0,3).map(card)",app)

    def test_carrot_cake_photo_and_license(self):
        recipes=json.loads((ROOT/"content/recipes.json").read_text(encoding="utf-8"))["recipes"]
        cake=next(r for r in recipes if r["id"]=="curadoria-bolo-de-cenoura-com-cobertura-de-chocolate")
        self.assertIn("Bolo_de_Cenoura",cake["image"])
        self.assertIn("Pedro Toniazzo Terres",cake["imageCredit"])
        self.assertIn("creativecommons.org/licenses/by-sa/4.0",cake["imageLicenseUrl"])

if __name__=="__main__":unittest.main()
