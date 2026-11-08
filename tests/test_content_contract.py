"""Testes de contrato dinâmicos (não dependem da quantidade de itens)."""
from copy import deepcopy
from pathlib import Path
import unittest

from harness.validate_content import load_data, validate


class ContentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()

    def test_catalogo_existente_satisfaz_contrato(self):
        result = validate(self.data)
        self.assertTrue(result["ok"], result["errors"])

    def test_receita_sem_quantidade_e_rejeitada(self):
        data = deepcopy(self.data)
        data["recipes"][0]["ingredients"][0]["quantity"] = None
        result = validate(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("quantidade" in msg for msg in result["errors"]))

    def test_titulo_duplicado_e_rejeitado(self):
        data = deepcopy(self.data)
        data["techniques"][1]["title"] = data["techniques"][0]["title"]
        result = validate(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("título duplicado" in msg for msg in result["errors"]))

    def test_aula_sem_secoes_e_rejeitada(self):
        data = deepcopy(self.data)
        data["techniques"][0]["lesson"] = []
        result = validate(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("duas seções" in msg for msg in result["errors"]))

    def test_curation_sem_fonte_e_rejeitada(self):
        data = deepcopy(self.data)
        if not data.get("curatedDiscoveries"):
            self.skipTest("Não há fichas de curadoria")
        data["curatedDiscoveries"][0]["sourceUrl"] = "http://inseguro.example"
        result = validate(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("sourceUrl" in msg for msg in result["errors"]))

    def test_oficina_expirada_nao_derruba_pipeline(self):
        data = deepcopy(self.data)
        data["workshops"][0]["eventDate"] = "2020-01-01"
        result = validate(data)
        self.assertTrue(result["ok"], result["errors"])
        self.assertTrue(any("evento passado" in msg for msg in result["warnings"]))


if __name__ == "__main__":
    unittest.main()
