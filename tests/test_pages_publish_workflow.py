"""Regression tests for GitHub Pages publisher artifact naming.

Rerunning a failed deployment job under the same workflow run must not
accumulate identically named artifacts that deploy-pages cannot disambiguate.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "site.yml"


class PagesArtifactContractTests(unittest.TestCase):
    def test_upload_and_deploy_use_identical_per_attempt_artifact(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        expected = "github-pages-${{ github.run_id }}-${{ github.run_attempt }}"
        upload = re.search(
            r"uses:\s*actions/upload-pages-artifact@v4\s*\n"
            r"\s*with:\s*\n(?:(?:\s+[^\n]+)\n)*?"
            r"\s*name:\s*([^\n#]+)", text
        )
        deploy = re.search(
            r"uses:\s*actions/deploy-pages@v4\s*\n"
            r"\s*with:\s*\n\s*artifact_name:\s*([^\n#]+)", text
        )
        self.assertIsNotNone(upload, "Pages upload must name its artifact.")
        self.assertIsNotNone(deploy, "Pages deploy must select its artifact.")
        self.assertEqual(upload.group(1).strip(), expected)
        self.assertEqual(deploy.group(1).strip(), expected)

    def test_publish_requires_release_validation(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^\s+needs:\s*validar-release\s*$")


if __name__ == "__main__":
    unittest.main()
