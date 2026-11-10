"""Verify static recipe pages and sitemap generated from editorial sources."""
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_dataset import assemble
from build_recipe_pages import generate, BASE


class RecipePagesTests(unittest.TestCase):
    def test_generate_every_recipe_and_sitemap(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            recipes=assemble()["recipes"]
            self.assertEqual(generate(out),len(recipes))
            sitemap=ET.parse(out/"sitemap.xml").getroot()
            ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs=[x.text for x in sitemap.findall(".//s:loc",ns)]
            self.assertEqual(len(locs),len(recipes)+1)
            self.assertIn(BASE,locs)
            for recipe in recipes:
                page=out/"receitas"/recipe["id"]/"index.html"
                self.assertTrue(page.is_file())
                html=page.read_text(encoding="utf-8")
                self.assertIn('application/ld+json',html)
                self.assertIn('rel="canonical"',html)
                self.assertIn('#receita/'+recipe["id"],html)

if __name__=="__main__":
    unittest.main()
