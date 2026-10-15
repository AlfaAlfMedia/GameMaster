"""Tests for the permissions of the data directory in gamemaster.zomboid.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from gamemaster import permissions, zomboid

REPOSITORY = Path(__file__).resolve().parent.parent
TEMPLATES = REPOSITORY / "usr/share/gamemaster/zomboid"

OWNER = permissions.Owner(os.getuid(), os.getgid())

CONF = """\
PZ_SERVER_RCON_PASSWORD=secret
PZ_SERVER_PORT=16261
PZ_UDP_PORT=16262
PZ_RCON_PORT=27015
"""


def mode(path: Path) -> int:
    return stat.S_IMODE(path.lstat().st_mode)


class DataDirectoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.home = base / "home"
        self.home.mkdir(mode=0o700)
        self.data_dir = self.home / "Zomboid"

        conf_file = base / "zomboid.conf"
        conf_file.write_text(CONF)

        self.server = zomboid.Server(
            username="zomboid",
            server_user="zomboid",
            data_dir=self.data_dir,
            install_dir=base / "pzserver",
            admin_password="admin",
            branch="public",
            conf_file=conf_file,
        )

        for patch in (
            mock.patch.object(zomboid, "owner_of", return_value=OWNER),
            mock.patch.object(zomboid, "LOG_DIR", base / "log"),
            mock.patch.object(zomboid, "INI_TEMPLATE", TEMPLATES / "template.ini"),
            mock.patch.object(
                zomboid, "SANDBOX_TEMPLATE", TEMPLATES / "template_SandboxVars.lua"
            ),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_create_world_from_nothing(self) -> None:
        ini_file, sandbox_file, save_dir = zomboid.create_world_files(
            self.server, "bonn"
        )

        self.assertEqual(mode(self.data_dir), 0o2750)
        self.assertEqual(mode(self.data_dir / "Server"), 0o2770)
        self.assertEqual(mode(self.data_dir / "Saves"), 0o2770)
        self.assertEqual(mode(self.data_dir / "Saves/Multiplayer"), 0o2770)
        self.assertEqual(mode(ini_file), 0o660)
        self.assertEqual(mode(sandbox_file), 0o660)
        self.assertEqual(mode(save_dir), 0o2770)
        self.assertIn("RCONPassword=secret", ini_file.read_text())
        self.assertEqual(zomboid.find_worlds(self.data_dir), ([], ["bonn"]))

    def test_create_world_twice_is_refused(self) -> None:
        zomboid.create_world_files(self.server, "bonn")
        with self.assertRaises(zomboid.GameMasterError):
            zomboid.create_world_files(self.server, "bonn")

    def test_fix_permissions_without_data_dir(self) -> None:
        self.assertIsNone(zomboid.fix_permissions(self.server))
        self.assertEqual(mode(self.home), 0o750)

    def test_fix_permissions_sorts_the_parts(self) -> None:
        # Roughly what a live server looks like, after the agent made a
        # directory of its own at the top and root put a backup back
        for directory in ("Server", "Saves/Multiplayer/bonn", "db", "backups",
                          "Backups", "mods", "Workshop"):
            (self.data_dir / directory).mkdir(parents=True)
        for name in ("Server/bonn.ini", "Saves/Multiplayer/bonn/map_1_1.bin",
                     "db/bonn.db", "server-console.txt"):
            (self.data_dir / name).write_text("x")
        for path in [self.data_dir, *self.data_dir.rglob("*")]:
            path.chmod(0o775 if path.is_dir() else 0o644)
        (self.data_dir / "Logs").symlink_to("/var/log")

        report = zomboid.fix_permissions(self.server)

        self.assertEqual(mode(self.data_dir), 0o2750)
        self.assertEqual(mode(self.data_dir / "Server/bonn.ini"), 0o660)
        self.assertEqual(mode(self.data_dir / "Saves/Multiplayer/bonn"), 0o2770)
        self.assertEqual(mode(self.data_dir / "Saves/Multiplayer/bonn/map_1_1.bin"), 0o660)
        self.assertEqual(mode(self.data_dir / "mods"), 0o2770)
        self.assertEqual(mode(self.data_dir / "db"), 0o700)
        self.assertEqual(mode(self.data_dir / "db/bonn.db"), 0o600)
        self.assertEqual(mode(self.data_dir / "backups"), 0o2750)
        self.assertEqual(mode(self.data_dir / "Backups"), 0o2750)
        self.assertEqual(mode(self.data_dir / "server-console.txt"), 0o640)
        self.assertEqual(
            report.skipped, [permissions.Skipped("Logs", "symbolic link")]
        )

    def test_fix_permissions_refuses_linked_data_dir(self) -> None:
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        self.data_dir.symlink_to(elsewhere)

        with self.assertRaises(zomboid.GameMasterError):
            zomboid.fix_permissions(self.server)


if __name__ == "__main__":
    unittest.main()
