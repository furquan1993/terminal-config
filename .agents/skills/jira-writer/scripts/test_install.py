#!/usr/bin/env python3
"""Offline tests for the jira-writer skill installer."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("install.sh").resolve()
SOURCE = SCRIPT.parent.parent.resolve()
DESTINATIONS = (
    ".agents/skills/jira-writer",  # Codex and Agent Skills compatible agents
    ".claude/skills/jira-writer",
    ".gemini/config/skills/jira-writer",  # Antigravity IDE
    ".gemini/antigravity-cli/skills/jira-writer",
    ".config/opencode/skills/jira-writer",
    ".pi/agent/skills/jira-writer",
)


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "home with spaces"
        self.home.mkdir()

    def run_installer(self, *args):
        return subprocess.run(
            ["sh", str(SCRIPT), *args],
            cwd=self.tmp.name,
            env={**os.environ, "HOME": str(self.home)},
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installs_all_locations_and_reruns_without_changes(self):
        first = self.run_installer()
        self.assertEqual(0, first.returncode, first.stderr)
        for relative in DESTINATIONS:
            link = self.home / relative
            self.assertTrue(link.is_symlink(), relative)
            self.assertEqual(SOURCE, link.resolve())
        again = self.run_installer()
        self.assertEqual(0, again.returncode, again.stderr)
        self.assertEqual(6, again.stdout.count("already installed:"))

    def test_conflict_prevents_partial_install(self):
        conflict = self.home / DESTINATIONS[4]
        conflict.parent.mkdir(parents=True)
        conflict.mkdir()
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertIn(str(conflict), result.stderr)
        for relative in DESTINATIONS:
            self.assertFalse((self.home / relative).is_symlink())

    def test_file_in_later_parent_prevents_partial_install(self):
        blocked = self.home / ".config/opencode"
        blocked.parent.mkdir()
        blocked.write_text("keep me")
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertIn(str(blocked), result.stderr)
        self.assertEqual("keep me", blocked.read_text())
        for relative in DESTINATIONS:
            self.assertFalse((self.home / relative).is_symlink())

    def test_dangling_link_in_parent_prevents_partial_install(self):
        blocked = self.home / ".gemini/config"
        blocked.parent.mkdir()
        blocked.symlink_to("missing")
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertIn(str(blocked), result.stderr)
        self.assertEqual("missing", os.readlink(blocked))
        for relative in DESTINATIONS:
            self.assertFalse((self.home / relative).is_symlink())

    def test_dangling_link_is_not_overwritten(self):
        conflict = self.home / DESTINATIONS[0]
        conflict.parent.mkdir(parents=True)
        conflict.symlink_to("missing")
        result = self.run_installer()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("missing", os.readlink(conflict))

    def test_rejects_arguments_without_installing(self):
        result = self.run_installer("unexpected")
        self.assertEqual(2, result.returncode)
        self.assertFalse((self.home / DESTINATIONS[0]).exists())


if __name__ == "__main__":
    unittest.main()
