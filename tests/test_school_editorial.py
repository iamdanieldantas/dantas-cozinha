"""Editorial contract for the modular Escola content and discovery UI."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SchoolEditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/"assets/data.js").read_text(encoding="utf-8")
        cls.data=json.loads(re.sub(r";\s*$","",re.sub(r"^window\.DANTAS_DATA\s*=\s*","",raw)))

    def test_each_lesson_has_appropriate_optional_learning_resource(self):
        lessons=self.data["techniques"]
        self.assertTrue(lessons)
        allowed={"bullets","steps","callout","image","workflow","orgchart","glossary"}
        for lesson in lessons:
            with self.subTest(lesson=lesson["id"]):
                blocks=lesson.get("contentBlocks",[])
                self.assertGreaterEqual(len(blocks),1)
                for block in blocks:
                    self.assertIn(block["type"],allowed)
                    if block["type"] in {"bullets","steps","workflow","orgchart","glossary"}:
                        self.assertTrue(block.get("items"))
                    if block["type"]=="image":
                        self.assertTrue(block.get("alt") and block.get("src"))

    def test_school_search_and_filter_controls_present(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        for marker in ['id="school-search"','id="school-filters"','id="school-count"']:
            self.assertIn(marker,html)
        self.assertIn("renderSchoolFilters",app)
        self.assertIn("selectedSchoolSearch",app)
        self.assertIn("school-deep-dive",app)

if __name__=="__main__":
    unittest.main()
