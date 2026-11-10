"""Regression checks for modular editorial content."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_dataset import assemble, render
from validate_dataset import load_dataset, validate


class ModularContentTests(unittest.TestCase):
    def test_domain_sources_match_published_data(self):
        self.assertEqual(assemble(),load_dataset())

    def test_assembled_content_respects_contract(self):
        self.assertEqual(validate(assemble()),[])

    def test_browser_global_is_preserved(self):
        generated=render(assemble())
        self.assertTrue(generated.startswith("window.DANTAS_DATA = {"))
        self.assertTrue(generated.endswith(";\n"))

    def test_all_content_domains_are_present(self):
        data=assemble()
        for key in ("siteName","recipes","techniques","workshops","videos","curatedDiscoveries","curationPolicy"):
            self.assertIn(key,data)

if __name__=="__main__":
    unittest.main()
