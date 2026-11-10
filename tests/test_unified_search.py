"""Unified search accessibility and route regression tests."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


class UnifiedSearchTests(unittest.TestCase):
    def test_search_view_and_accessible_controls(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        for marker in ('data-view="buscar"','id="unified-search"','aria-controls="unified-results"','id="unified-count"','aria-live="polite"','data-search-kind="receitas"','data-search-kind="aulas"'):
            self.assertIn(marker,html)

    def test_search_ranking_and_deep_links(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        for marker in ('function normalizedSearch','function searchScore','function unifiedMatches','function renderUnifiedSearch','function openUnifiedResult','target.open=true','openRecipe(id)'):
            self.assertIn(marker,app)
        self.assertIn("'buscar'",app)
        self.assertIn("normalize('NFD')",app)

    def test_original_searches_and_storage_remain(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        for marker in ("'dantas-cozinha-v1'","function renderRecipes()","function renderTechniques()","selectedSchoolCategory","selectedFilter"):
            self.assertIn(marker,app)

if __name__=="__main__":
    unittest.main()
