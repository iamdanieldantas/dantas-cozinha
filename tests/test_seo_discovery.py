"""SEO metadata and discoverability contract."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
URL="https://iamdanieldantas.github.io/dantas-cozinha/"


class SeoTests(unittest.TestCase):
    def test_canonical_and_social_metadata(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn(f'<link rel="canonical" href="{URL}">',html)
        for marker in ('property="og:title"','property="og:description"','property="og:url"','application/ld+json'):
            self.assertIn(marker,html)

    def test_sitemap_has_only_crawlable_entry(self):
        root=ET.parse(ROOT/"sitemap.xml").getroot()
        ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs=[x.text for x in root.findall(".//s:loc",ns)]
        self.assertEqual(locs,[URL])

    def test_robots_points_to_sitemap(self):
        robots=(ROOT/"robots.txt").read_text(encoding="utf-8")
        self.assertIn(URL+"sitemap.xml",robots)

    def test_route_metadata_and_no_misleading_hash_sitemap(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn("function setPageMeta(",app)
        self.assertIn("setPageMeta(page,",app)
        self.assertIn("Escola de Gastronomia",app)

if __name__=="__main__":
    unittest.main()
