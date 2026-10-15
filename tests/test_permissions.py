"""Tests for gamemaster.permissions.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests

They need no root: files are handed to the user running the tests, which
any user may do.
"""

import os
import stat
import tempfile
import unittest
from pathlib import Path

from gamemaster import permissions
from gamemaster.permissions import GROUP_READABLE, GROUP_WRITABLE, PRIVATE

OWNER = permissions.Owner(os.getuid(), os.getgid())


def policy(names: tuple[str, ...]) -> permissions.Modes:
    """A small policy like the one of a game: one open, one closed part."""
    if names and names[0] == "open":
        return GROUP_WRITABLE
    if names and names[0] == "closed":
        return PRIVATE
    return GROUP_READABLE


def mode(path: Path) -> int:
    return stat.S_IMODE(path.lstat().st_mode)


class FixTreeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "data"
        self.outside = self.base / "outside"

        for directory in ("open/sub", "closed", "other"):
            (self.root / directory).mkdir(parents=True)
        for name in ("open/sub/a.ini", "closed/world.db", "other/log.txt", "top.ini"):
            (self.root / name).write_text("x")
        for path in self.root.rglob("*"):
            path.chmod(0o777 if path.is_dir() else 0o666)

        self.outside.mkdir()
        (self.outside / "secret").write_text("x")
        (self.outside / "secret").chmod(0o600)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_modes_follow_the_policy(self) -> None:
        report = permissions.fix_tree(self.root, OWNER, policy)

        self.assertEqual(mode(self.root), 0o2750)
        self.assertEqual(mode(self.root / "open"), 0o2770)
        self.assertEqual(mode(self.root / "open/sub"), 0o2770)
        self.assertEqual(mode(self.root / "open/sub/a.ini"), 0o660)
        self.assertEqual(mode(self.root / "closed"), 0o700)
        self.assertEqual(mode(self.root / "closed/world.db"), 0o600)
        self.assertEqual(mode(self.root / "other/log.txt"), 0o640)
        self.assertEqual(mode(self.root / "top.ini"), 0o640)
        self.assertEqual(report.skipped, [])
        self.assertGreater(report.changed, 0)

    def test_second_run_changes_nothing(self) -> None:
        permissions.fix_tree(self.root, OWNER, policy)
        report = permissions.fix_tree(self.root, OWNER, policy)
        self.assertEqual(report.changed, 0)

    def test_executable_stays_executable(self) -> None:
        script = self.root / "open/run.sh"
        script.write_text("#!/bin/sh\n")
        script.chmod(0o755)

        permissions.fix_tree(self.root, OWNER, policy)
        self.assertEqual(mode(script), 0o770)

    def test_link_to_file_is_not_followed(self) -> None:
        (self.root / "open/evil").symlink_to(self.outside / "secret")

        report = permissions.fix_tree(self.root, OWNER, policy)

        self.assertEqual(mode(self.outside / "secret"), 0o600)
        self.assertIn(permissions.Skipped("open/evil", "symbolic link"), report.skipped)

    def test_link_to_directory_is_not_entered(self) -> None:
        (self.root / "Logs").symlink_to(self.outside)

        report = permissions.fix_tree(self.root, OWNER, policy)

        self.assertEqual(mode(self.outside / "secret"), 0o600)
        self.assertEqual(stat.S_IMODE(self.outside.stat().st_mode) & 0o2000, 0)
        self.assertIn(permissions.Skipped("Logs", "symbolic link"), report.skipped)

    def test_hard_link_is_left_alone(self) -> None:
        os.link(self.outside / "secret", self.root / "open/hard")

        report = permissions.fix_tree(self.root, OWNER, policy)

        self.assertEqual(mode(self.outside / "secret"), 0o600)
        self.assertIn(permissions.Skipped("open/hard", "hard link"), report.skipped)

    def test_special_file_is_left_alone(self) -> None:
        os.mkfifo(self.root / "open/pipe")

        report = permissions.fix_tree(self.root, OWNER, policy)

        self.assertIn(
            permissions.Skipped("open/pipe", "neither file nor directory"),
            report.skipped,
        )

    def test_root_that_is_a_link_is_refused(self) -> None:
        link = self.base / "link"
        link.symlink_to(self.root)

        with self.assertRaises(permissions.PermissionsError):
            permissions.fix_tree(link, OWNER, policy)


class CreateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.outside = self.base / "outside"
        self.outside.mkdir()
        self.fd = permissions.open_directory(self.base)

    def tearDown(self) -> None:
        os.close(self.fd)
        self.temp.cleanup()

    def test_make_directories_creates_with_modes(self) -> None:
        fd = permissions.make_directories(
            self.fd, ("a", "b"), OWNER, lambda names: 0o2770 if len(names) == 2 else 0o2750
        )
        os.close(fd)

        self.assertEqual(mode(self.base / "a"), 0o2750)
        self.assertEqual(mode(self.base / "a/b"), 0o2770)

    def test_make_directories_leaves_existing_alone(self) -> None:
        (self.base / "a").mkdir()
        (self.base / "a").chmod(0o755)

        os.close(permissions.make_directories(self.fd, ("a",), OWNER, lambda _n: 0o2770))

        self.assertEqual(mode(self.base / "a"), 0o755)

    def test_make_directories_does_not_follow_a_link(self) -> None:
        (self.base / "a").symlink_to(self.outside)

        with self.assertRaises(permissions.PermissionsError):
            permissions.make_directories(self.fd, ("a", "b"), OWNER, lambda _n: 0o2770)

        self.assertFalse((self.outside / "b").exists())

    def test_create_file(self) -> None:
        permissions.create_file(self.fd, "new.ini", "content", OWNER, 0o660)

        self.assertEqual((self.base / "new.ini").read_text(), "content")
        self.assertEqual(mode(self.base / "new.ini"), 0o660)

    def test_create_file_refuses_existing_file(self) -> None:
        (self.base / "old.ini").write_text("keep")

        with self.assertRaises(permissions.PermissionsError):
            permissions.create_file(self.fd, "old.ini", "new", OWNER, 0o660)

        self.assertEqual((self.base / "old.ini").read_text(), "keep")

    def test_create_file_refuses_link(self) -> None:
        (self.base / "evil.ini").symlink_to(self.outside / "target")

        with self.assertRaises(permissions.PermissionsError):
            permissions.create_file(self.fd, "evil.ini", "new", OWNER, 0o660)

        self.assertFalse((self.outside / "target").exists())

    def test_read_text_refuses_link(self) -> None:
        (self.outside / "secret").write_text("RCONPassword=x")
        (self.base / "world.ini").symlink_to(self.outside / "secret")

        with self.assertRaises(permissions.PermissionsError):
            permissions.read_text(self.base / "world.ini")

    def test_open_to_group(self) -> None:
        home = self.base / "home"
        home.mkdir()
        home.chmod(0o700)

        self.assertTrue(permissions.open_to_group(home))
        self.assertEqual(mode(home), 0o750)
        self.assertFalse(permissions.open_to_group(home))


class LogDirectoryTest(unittest.TestCase):
    def test_logs_are_readable_for_the_group(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / "log" / "valheim"
            directory.mkdir(parents=True)
            # As systemd leaves it: for its owner alone, with UMask=0007
            (directory / "old.log").write_text("x")
            (directory / "old.log").chmod(0o660)
            (directory / "link.log").symlink_to(directory / "old.log")

            permissions.prepare_log_directory(directory, OWNER, ("new.log",))

            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o750)
            self.assertEqual(stat.S_IMODE((directory / "old.log").stat().st_mode), 0o640)
            self.assertEqual(stat.S_IMODE((directory / "new.log").stat().st_mode), 0o640)
            self.assertEqual((directory / "old.log").read_text(), "x")
            self.assertTrue((directory / "link.log").is_symlink())


if __name__ == "__main__":
    unittest.main()
