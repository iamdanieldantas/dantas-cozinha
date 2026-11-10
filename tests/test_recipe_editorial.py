"""Recipe editorial contract and audit coverage."""
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from audit_recipes import load_recipes, inspect_recipe, report


class RecipeEditorialTests(unittest.TestCase):
    def test_recipe_ingredients_and_preparation_are_complete(self):
        recipes=load_recipes()
        self.assertTrue(recipes)
        for recipe in recipes:
            with self.subTest(recipe=recipe["id"]):
                issues=inspect_recipe(recipe)
                self.assertFalse([x for x in issues if "ingrediente" in x or "preparo ausente" in x or "rendimento inválido" in x],issues)

    def test_audit_includes_all_recipes(self):
        recipes=load_recipes()
        markdown=report()
        for recipe in recipes:
            self.assertIn(recipe["title"],markdown)

    def test_recipe_page_labels_illustrative_photographs(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn("function imageAttribution",app)
        self.assertIn("A apresentação pode ser diferente",app)
        self.assertIn("imageAttribution(r)",app)

if __name__=="__main__":
    unittest.main()
