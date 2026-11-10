"""Basic visual identity regression checks."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class BrandTests(unittest.TestCase):
    def test_brand_asset_exists_and_is_referenced(self):
        logo=ROOT/"assets/logo-mark.svg"
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertTrue(logo.is_file())
        self.assertIn('src="assets/logo-mark.svg"',html)
        self.assertIn('aria-label="Dantas Cozinha',html)

    def test_accessible_focus_and_reduced_motion(self):
        css=(ROOT/"assets/styles.css").read_text(encoding="utf-8")
        self.assertIn("summary:focus-visible",css)
        self.assertIn("prefers-reduced-motion:reduce",css)
        self.assertIn(".nav a[aria-current=\"page\"]",css)

if __name__=="__main__":
    unittest.main()
