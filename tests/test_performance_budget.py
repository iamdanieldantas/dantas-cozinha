"""Regression checks for image loading priorities and performance budgets."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from audit_asset_budget import audit


class PerformanceTests(unittest.TestCase):
    def test_assets_under_transfer_budget(self):
        self.assertEqual(audit(),[])

    def test_hero_image_is_prioritized(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('fetchpriority="high"',html)
        self.assertIn('loading="eager"',html)
        self.assertIn('rel="preconnect" href="https://images.unsplash.com"',html)

    def test_recipe_images_are_lazy_and_have_dimensions(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn('loading="lazy" decoding="async" width="940" height="705"',app)

if __name__=="__main__":
    unittest.main()
