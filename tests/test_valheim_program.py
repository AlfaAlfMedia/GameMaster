"""Tests for the program valheim: setting worlds up, and wrong commands.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import argparse
import importlib.machinery
import importlib.util
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from gamemaster.errors import GameMasterError

REPOSITORY = Path(__file__).resolve().parent.parent

# The program has no .py extension, so it is loaded by path
_loader = importlib.machinery.SourceFileLoader(
    "valheim_program", str(REPOSITORY / "usr/sbin/valheim")
)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
program = importlib.util.module_from_spec(_spec)
_loader.exec_module(program)

valheim = program.valheim


class InitWorldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = mock.Mock(username="valheim", server_user="valheim",
                                data_dir=Path("/nowhere"))
        self.arguments = argparse.Namespace(name="Grollhusen")
        self.output = StringIO()

        for name, value in (("find_running_server", None),
                            ("find_worlds", []),
                            ("has_rules", False)):
            patch = mock.patch.object(valheim, name, return_value=value)
            setattr(self, name, patch.start())
            self.addCleanup(patch.stop)

        self.install_unit = self.patch(valheim, "install_unit",
                                       return_value=Path("/etc/systemd/system/x.service"))
        self.enable = self.patch(program.service, "enable")
        self.start = self.patch(program.service, "start")

    def patch(self, target, name, **kwargs):
        patcher = mock.patch.object(target, name, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def init(self) -> str:
        with redirect_stdout(self.output):
            program.init_world_command(self.server, self.arguments)
        return self.output.getvalue()

    def test_takes_over_a_world_the_server_has(self) -> None:
        self.find_worlds.return_value = ["Grollhusen"]
        output = self.init()
        self.assertIn("world 'Grollhusen' is already initialised", output)
        self.install_unit.assert_called_once_with(self.server, "Grollhusen")
        self.enable.assert_called_once()
        # Set up, not started: that is 'valheim start'
        self.start.assert_not_called()
        self.assertIn("valheim -u valheim start", output)

    def test_sets_up_a_created_world_without_starting_it(self) -> None:
        self.has_rules.return_value = True
        output = self.init()
        self.assertIn("Valheim makes world 'Grollhusen' when the server starts", output)
        self.install_unit.assert_called_once()
        self.start.assert_not_called()

    def test_unknown_world_points_to_create(self) -> None:
        with self.assertRaises(GameMasterError) as caught:
            self.init()
        self.assertIn("valheim -u valheim world create Grollhusen", str(caught.exception))
        self.install_unit.assert_not_called()

    def test_refused_while_a_server_runs_outside_gamemaster(self) -> None:
        self.find_worlds.return_value = ["Grollhusen"]
        self.find_running_server.return_value = valheim.RunningServer(42, "Grollhusen")
        with mock.patch.object(valheim.service, "is_active", return_value=False):
            with self.assertRaises(GameMasterError) as caught:
                self.init()
        self.assertIn("not started by GameMaster", str(caught.exception))
        self.install_unit.assert_not_called()


class CreateAndSwitchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = mock.Mock(username="valheim", data_dir=Path("/nowhere"))

    def test_create_of_an_existing_world_points_to_init(self) -> None:
        with mock.patch.object(valheim, "find_worlds", return_value=["Grollhusen"]):
            with self.assertRaises(GameMasterError) as caught:
                program.create_world_command(
                    self.server, argparse.Namespace(name="Grollhusen")
                )
        self.assertIn("world init Grollhusen", str(caught.exception))

    def test_switch_needs_a_service_as_for_zomboid(self) -> None:
        with mock.patch.object(valheim, "find_worlds", return_value=["Grollhusen"]), \
             mock.patch.object(program.service, "exists", return_value=False):
            with self.assertRaises(GameMasterError) as caught:
                program.switch_world_command(
                    self.server, argparse.Namespace(name="Grollhusen")
                )
        self.assertIn("world init", str(caught.exception))

    def test_switch_to_a_world_not_started_yet(self) -> None:
        with mock.patch.object(valheim, "find_worlds", return_value=[]), \
             mock.patch.object(valheim, "has_rules", return_value=True):
            with self.assertRaises(GameMasterError) as caught:
                program.switch_world_command(
                    self.server, argparse.Namespace(name="Nordmark")
                )
        self.assertIn("not been started yet", str(caught.exception))


class WrongCommandTest(unittest.TestCase):
    def parse(self, *words: str) -> tuple[str, str, int]:
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            with self.assertRaises(SystemExit) as caught:
                program.build_parser().parse_args(list(words))
        return out.getvalue(), err.getvalue(), caught.exception.code

    def test_lists_the_commands_of_that_level(self) -> None:
        out, err, code = self.parse("player", "kick", "Ragnar")
        self.assertEqual(code, 1)
        self.assertIn("unadmin", out)
        self.assertEqual(
            err.strip().splitlines()[-1],
            "ERROR: 'kick' is not a command of valheim player. "
            "The commands are listed above.",
        )

    def test_top_level(self) -> None:
        out, err, code = self.parse("save")
        self.assertEqual(code, 1)
        self.assertIn("world", out)
        self.assertIn("ERROR: 'save' is not a command of valheim.", err)


if __name__ == "__main__":
    unittest.main()
