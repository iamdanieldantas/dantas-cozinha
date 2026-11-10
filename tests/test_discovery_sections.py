"""Validate workshops, schools, and video/profile presentation."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

class DiscoveryTests(unittest.TestCase):
    def test_events_and_permanent_schools_are_distinct(self):
        source=(ROOT/"assets/data.js").read_text(encoding="utf-8")
        data=json.loads(re.sub(r";\s*$","",re.sub(r"^window\.DANTAS_DATA\s*=\s*","",source)))
        workshops=data["workshops"]
        self.assertTrue(any(w.get("eventDate") for w in workshops))
        self.assertTrue(any(not w.get("eventDate") for w in workshops))
        for w in workshops:
            self.assertTrue(w.get("verifiedAt"))
            self.assertTrue(w.get("url","").startswith("https://"))

    def test_interface_shows_provenance_and_separate_sections(self):
        app=(ROOT/"assets/app.js").read_text(encoding="utf-8")
        for phrase in ("Próximas aulas com data","Escolas e cursos permanentes","Vídeos selecionados","Perfis para acompanhar","Informações consultadas em","Conteúdo de terceiros"):
            self.assertIn(phrase,app)

if __name__=="__main__":
    unittest.main()
