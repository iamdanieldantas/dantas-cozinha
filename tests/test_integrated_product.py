"""Integrated product regression checks for learning journey and editorial consistency."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]


class IntegratedProductTests(unittest.TestCase):
    def test_learning_dashboard_is_accessible(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        for marker in ('id="school-progress"','role="progressbar"','id="school-next-lesson"','id="home-learning-progress"'):
            self.assertIn(marker,html)
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        for marker in ("function learningLessons()","function updateLearningProgress()","updateLearningProgress();","state.completedLessons"):
            self.assertIn(marker,app)

    def test_recipe_recommendations_and_editorial_notice(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn('class="related-recipes"',app)
        self.assertIn('class="recipe-content-status"',app)
        self.assertIn('x.category===r.category',app)

    def test_recipe_descriptions_do_not_claim_missing_preparation(self):
        recipes=json.loads((ROOT/"content/recipes.json").read_text(encoding="utf-8"))["recipes"]
        for recipe in recipes:
            self.assertNotIn("quantidades e o preparo exatos no site original",recipe.get("description","").lower(),recipe["id"])
            self.assertTrue(recipe.get("steps"),recipe["id"])
            self.assertTrue(recipe.get("ingredients"),recipe["id"])

    def test_audit_document_exists(self):
        report=(ROOT/"docs/auditoria-editorial-pendente.md").read_text(encoding="utf-8")
        self.assertIn("revisão humana",report.lower())
        self.assertIn("licença",report.lower())

if __name__=="__main__":
    unittest.main()
