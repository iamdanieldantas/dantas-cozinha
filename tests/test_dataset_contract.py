"""Dataset contract regression tests."""
import copy
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_dataset import load_dataset, validate


class DatasetContractTests(unittest.TestCase):
    def test_published_data_is_valid(self):
        self.assertEqual(validate(load_dataset()),[])

    def test_duplicate_id_is_rejected(self):
        data=load_dataset()
        data["videos"][0]["id"]=data["recipes"][0]["id"]
        self.assertTrue(any("duplicate id" in issue for issue in validate(data)))

    def test_missing_recipe_steps_is_rejected(self):
        data=load_dataset()
        data["recipes"][0]["steps"]=[]
        self.assertTrue(any("steps" in issue for issue in validate(data)))

    def test_invalid_video_url_is_rejected(self):
        data=load_dataset()
        data["videos"][0]["url"]="javascript:alert(1)"
        self.assertTrue(any("HTTPS URL" in issue for issue in validate(data)))

    def test_school_blocks_remain_optional(self):
        data=load_dataset()
        data["techniques"][0].pop("contentBlocks",None)
        self.assertFalse(any("contentBlocks" in issue for issue in validate(data)))

if __name__=="__main__":
    unittest.main()
