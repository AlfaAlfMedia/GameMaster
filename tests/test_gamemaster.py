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
from unittest import mock

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
            return program.find_install_dir(
                program.GAMES["zomboid"], self.default, self.home
            )

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


class FindValheimTest(unittest.TestCase):
    def test_found_by_its_program(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            server = home / "ValheimDedicatedServer"
            server.mkdir()
            (server / "valheim_server.x86_64").write_text("")
            # A Zomboid server beside it is not mistaken for one
            (home / "pz").mkdir()
            (home / "pz" / "start-server.sh").write_text("")

            with redirect_stdout(StringIO()):
                found = program.find_install_dir(
                    program.GAMES["valheim"], str(home / "opt"), home
                )
            self.assertEqual(found, str(server))


class PortsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.etc = Path(self.temp.name)
        (self.etc / "zomboid").mkdir()
        (self.etc / "valheim").mkdir()
        (self.etc / "zomboid" / "zomboid.conf").write_text(
            "PZ_SERVER_PORT=16261\nPZ_UDP_PORT=16262\nPZ_RCON_PORT=27015\n"
        )
        (self.etc / "valheim" / "valheim.conf").write_text("VH_SERVER_PORT=2456\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_ports_of_every_game_are_taken(self) -> None:
        taken = program.used_ports(self.etc)
        self.assertEqual(taken[16261], "zomboid (zomboid)")
        self.assertEqual(taken[27015], "zomboid (zomboid)")
        # Valheim opens the port after its own as well
        self.assertEqual(taken[2456], "valheim (valheim)")
        self.assertEqual(taken[2457], "valheim (valheim)")
        self.assertNotIn(2458, taken)

    def test_a_valheim_port_needs_the_next_one_free(self) -> None:
        taken = program.used_ports(self.etc)
        # 2455 itself is free, but 2456 after it is not
        with self.assertRaises(GameMasterError):
            program.check_free(2455, 2, taken)
        program.check_free(2455, 1, taken)
        self.assertEqual(program.next_free_port(2455, 2, taken), 2458)

    def test_a_zomboid_port_inside_a_valheim_pair_is_refused(self) -> None:
        taken = program.used_ports(self.etc)
        with self.assertRaises(GameMasterError) as caught:
            program.check_free(2457, 1, taken)
        self.assertIn("valheim", str(caught.exception))

    def test_given_port_beside_a_taken_one(self) -> None:
        taken = program.used_ports(self.etc)
        setting = program.GAMES["valheim"].ports[0]
        self.assertEqual(program.choose_port(setting, "2458", "2456", taken), 2458)
        with self.assertRaises(GameMasterError):
            program.choose_port(setting, "16260", "2456", taken)


class CommandLineTest(unittest.TestCase):
    def test_each_game_has_its_own_port_options(self) -> None:
        parser = program.build_parser()
        arguments = parser.parse_args(["install", "valheim", "-u", "vh", "-P", "2460"])
        self.assertEqual(arguments.port, "2460")
        self.assertEqual(arguments.game, "valheim")
        with redirect_stdout(StringIO()), mock.patch("sys.stderr", StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(["add", "valheim", "--rcon-port", "27015"])
        arguments = parser.parse_args(["add", "zomboid", "-R", "27016"])
        self.assertEqual(arguments.rcon_port, "27016")


if __name__ == "__main__":
    unittest.main()
