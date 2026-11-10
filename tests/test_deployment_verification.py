"""Offline checks for deployment verification."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_deployment import Assets


class DeploymentVerificationTests(unittest.TestCase):
    def test_local_html_references_exactly_three_versioned_assets(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        parser = Assets()
        parser.feed(html)
        self.assertEqual(len(parser.paths), 3)
        self.assertEqual(len(set(parser.paths)), 3)
        self.assertTrue(all("?v=" in path for path in parser.paths))

    def test_missing_asset_is_not_accepted(self):
        parser = Assets()
        parser.feed('<script src="assets/app.js?v=1"></script>')
        self.assertEqual(len(parser.paths), 1)


if __name__ == "__main__":
    unittest.main()
