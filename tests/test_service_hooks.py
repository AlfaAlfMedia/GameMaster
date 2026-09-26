"""Tests for the commands an administrator adds to the service of a server.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from gamemaster import permissions, service, zomboid
from gamemaster.errors import GameMasterError

REPOSITORY = Path(__file__).resolve().parent.parent
TEMPLATES = REPOSITORY / "usr/share/gamemaster/zomboid"

CONF = """\
PZ_SERVER_PORT=16261
PZ_UDP_PORT=16262
"""


class ParseCommandTest(unittest.TestCase):
    def test_prefixes_and_arguments(self) -> None:
        command = service.parse_command("-+/usr/bin/env a b")
        self.assertEqual(command.prefix, "-+")
        self.assertEqual(command.program, Path("/usr/bin/env"))
        self.assertEqual(command.arguments, "a b")
        self.assertTrue(command.as_root)
        self.assertEqual(command.line, "-+/usr/bin/env a b")

    def test_without_prefix_runs_as_the_server_user(self) -> None:
        self.assertFalse(service.parse_command("/usr/bin/true").as_root)

    def test_refused(self) -> None:
        for text in ("", "true", "++/usr/bin/true", "!/usr/bin/true",
                     "+/usr/../bin/true", "/usr/bin/true \x1b[0m", "+ /usr/bin/true"):
            with self.subTest(text=text), self.assertRaises(GameMasterError):
                service.parse_command(text)


class RootOnlyTest(unittest.TestCase):
    def test_system_program(self) -> None:
        self.assertEqual(
            permissions.require_root_only(Path("/usr/bin/true")), Path("/usr/bin/true")
        )

    def test_program_behind_a_link(self) -> None:
        # /bin is a link to /usr/bin on current Debian; both must pass
        real = permissions.require_root_only(Path("/bin/true"))
        self.assertTrue(real.name == "true")

    def test_program_of_a_user_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "hook.sh"
            script.write_text("#!/bin/sh\n")
            script.chmod(0o755)
            with self.assertRaises(permissions.PermissionsError):
                permissions.require_root_only(script)

    def test_not_a_program(self) -> None:
        with self.assertRaises(permissions.PermissionsError):
            permissions.require_root_only(Path("/etc/hostname"))


class UnitHooksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.conf_file = self.base / "zomboid.conf"
        self.server = zomboid.Server(
            username="zomboid",
            server_user="zomboid",
            data_dir=self.base / "Zomboid",
            install_dir=Path("/opt/pzserver"),
            admin_password="admin",
            branch="public",
            conf_file=self.conf_file,
        )
        patch = mock.patch.object(
            zomboid, "SERVICE_TEMPLATE", TEMPLATES / "template.service"
        )
        patch.start()
        self.addCleanup(patch.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def unit(self, hooks: str) -> str:
        self.conf_file.write_text(CONF + hooks)
        return zomboid.build_unit(self.server, "bonn")

    def test_no_hooks_leaves_no_marker(self) -> None:
        unit = self.unit("")
        self.assertNotIn("@", unit)
        self.assertIn("ExecStart=/opt/pzserver/start-server.sh -servername bonn", unit)

    def test_stopped_like_ctrl_c(self) -> None:
        # systemctl stop and a shutdown of the machine must let the server
        # save first, as Ctrl+C does
        lines = self.unit("").splitlines()
        self.assertIn("KillSignal=SIGINT", lines)
        self.assertNotIn("KillSignal=SIGTERM", lines)

    def test_hooks_in_order_after_gamemaster(self) -> None:
        unit = self.unit(
            "PZ_EXEC_START_PRE_10=/usr/bin/echo ten\n"
            "PZ_EXEC_START_PRE_2=+/usr/bin/echo $PZ_SERVER_PORT $PZ_UDP_PORT\n"
            "PZ_EXEC_STOP_POST_1=-/usr/bin/echo stopped\n"
            "PZ_EXEC_START_POST_1=\n"
        )
        lines = unit.splitlines()
        update = lines.index("ExecStartPre=-+/usr/sbin/zomboid -u zomboid update")
        two = lines.index("ExecStartPre=+/usr/bin/echo 16261 16262")
        ten = lines.index("ExecStartPre=/usr/bin/echo ten")
        self.assertLess(update, two)
        self.assertLess(two, ten)
        self.assertIn("ExecStopPost=-/usr/bin/echo stopped", lines)
        self.assertNotIn("ExecStartPost=", unit)

    def test_root_hook_of_a_user_is_refused(self) -> None:
        script = self.base / "setupSnat.sh"
        script.write_text("#!/bin/sh\n")
        script.chmod(0o755)

        with self.assertRaises(GameMasterError) as caught:
            self.unit(f"PZ_EXEC_START_PRE_1=+{script}\n")
        self.assertIn("PZ_EXEC_START_PRE_1", str(caught.exception))

    def test_hook_as_server_user_may_live_anywhere(self) -> None:
        unit = self.unit(f"PZ_EXEC_START_POST_1={self.base}/notify.sh\n")
        self.assertIn(f"ExecStartPost={self.base}/notify.sh", unit)


if __name__ == "__main__":
    unittest.main()
