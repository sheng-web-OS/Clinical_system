"""Prevent the real Google Cloud 32-character WIF display-name failure."""
from pathlib import Path
import re
import unittest


class WorkloadIdentityScriptTests(unittest.TestCase):
    def test_all_display_names_fit_cloud_limit(self):
        script = Path("tools/setup_drive_agent_wif.sh").read_text(encoding="utf-8")
        names = re.findall(r'--display-name="([^"]+)"', script)
        self.assertGreaterEqual(len(names), 2)
        for name in names:
            self.assertLessEqual(len(name), 32, name)

    def test_github_identity_restricted_to_exact_repo_and_workflow(self):
        script = Path("tools/setup_drive_agent_wif.sh").read_text(encoding="utf-8")
        self.assertIn('REPO_ID="1427690253"', script)
        self.assertIn("assertion.repository_id", script)
        self.assertIn("assertion.workflow_ref", script)
        self.assertIn("assertion.ref=='refs/heads/main'", script)

    def test_unattended_schedule_requires_separate_authorization(self):
        workflow = Path(".github/workflows/drive-source-agent.yml").read_text(encoding="utf-8")
        self.assertIn("CLINICAL_OS_AGENT_SCHEDULE_ENABLED", workflow)
        self.assertIn("CLINICAL_OS_AGENT_ENABLED", workflow)
        self.assertIn("CLINICAL_OS_DRAFT_WRITES_ENABLED", workflow)
        self.assertIn("github.event_name == 'workflow_dispatch'", workflow)



if __name__ == "__main__":
    unittest.main()
