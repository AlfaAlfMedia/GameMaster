"""Tests for the program gamemaster.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import importlib.machinery
import importlib.util
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from gamemaster.errors import GameMasterError

REPOSITORY = Path(__file__).resolve().parent.parent

# The program has no .py extension, so it is loaded by path
_loader = importlib.machinery.SourceFileLoader(
    "gamemaster_program", str(REPOSITORY / "usr/sbin/gamemaster")
)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
program = importlib.util.module_from_spec(_spec)
_loader.exec_module(program)


class FindInstallDirTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.default = str(self.base / "opt/pzserver")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def server(self, directory: Path) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "start-server.sh").write_text("#!/bin/sh\n")
        return directory

    def find(self) -> str:
        with redirect_stdout(StringIO()):
            return program.find_install_dir(self.default, self.home)

    def test_default_directory_comes_first(self) -> None:
        self.server(Path(self.default))
        self.server(self.home / "ProjectZomboidServer")
        self.assertEqual(self.find(), self.default)

    def test_one_server_in_the_home(self) -> None:
        found = self.server(self.home / "ProjectZomboidServer")
        self.assertEqual(self.find(), str(found))

    def test_two_levels_down(self) -> None:
        found = self.server(self.home / "games" / "pz")
        self.assertEqual(self.find(), str(found))

    def test_more_than_one_is_refused(self) -> None:
        self.server(self.home / "one")
        self.server(self.home / "two")
        with self.assertRaises(GameMasterError) as caught:
            self.find()
        self.assertIn("-d/--installdir", str(caught.exception))

    def test_none_says_what_to_do(self) -> None:
        with self.assertRaises(GameMasterError) as caught:
            self.find()
        self.assertIn("-d/--installdir", str(caught.exception))
        self.assertIn("gamemaster install zomboid", str(caught.exception))

    def test_too_deep_is_not_found(self) -> None:
        self.server(self.home / "a" / "b" / "c")
        with self.assertRaises(GameMasterError):
            self.find()


if __name__ == "__main__":
    unittest.main()
