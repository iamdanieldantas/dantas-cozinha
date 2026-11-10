"""Consolidated release: search, study, cooking and installable shell."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]


class ConsolidatedTests(unittest.TestCase):
    def test_study_progress_survives_backup(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn("completedLessons:Array.isArray(x.completedLessons)",app)
        self.assertIn("completedLessons:Array.isArray(s.completedLessons)",app)
        self.assertIn('data-lesson-complete=',app)

    def test_cooking_timer_is_bounded_and_optional(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        self.assertIn("function setupCookingTools()",app)
        self.assertIn("minutes>180",app)
        self.assertIn("navigator.wakeLock.request('screen')",app)
        self.assertIn("function stopCookingTimer()",app)

    def test_pwa_scope_and_offline_limits(self):
        manifest=json.loads((ROOT/"manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["scope"],"./")
        self.assertEqual(manifest["start_url"],"./")
        sw=(ROOT/"sw.js").read_text(encoding="utf-8")
        self.assertIn("request.method!=='GET'",sw)
        self.assertIn("origin!==self.location.origin",sw)
        self.assertIn("caches.keys()",sw)
        workflow=(ROOT/".github/workflows/site.yml").read_text(encoding="utf-8")
        self.assertIn("cp manifest.webmanifest sw.js robots.txt _site/",workflow)
        self.assertIn('rel="manifest"',(ROOT/"index.html").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()
