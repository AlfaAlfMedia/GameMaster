"""Tests for gamemaster.valheim: worlds, the log, the lists, the service.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from gamemaster import permissions, valheim
from gamemaster.errors import GameMasterError

REPOSITORY = Path(__file__).resolve().parent.parent
TEMPLATES = REPOSITORY / "usr/share/gamemaster/valheim"

OWNER = permissions.Owner(os.getuid(), os.getgid())

CONF = """\
VH_SERVER_NAME=Nordlicht am Fjord
VH_SERVER_PASSWORD=geheim
VH_SERVER_PUBLIC=1
VH_CROSSPLAY=0
VH_SERVER_PORT=2456
VH_SAVE_INTERVAL=
VH_BACKUPS=
"""


def mode(path: Path) -> int:
    return stat.S_IMODE(path.lstat().st_mode)


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir(mode=0o700)
        self.data_dir = self.home / valheim.DATA_SUBDIR
        self.conf_file = self.base / "valheim.conf"
        self.conf_file.write_text(CONF)

        self.server = valheim.Server(
            username="valheim",
            server_user="valheim",
            data_dir=self.data_dir,
            install_dir=Path("/opt/valheim"),
            branch="public",
            conf_file=self.conf_file,
        )

        for patch in (
            mock.patch.object(valheim, "owner_of", return_value=OWNER),
            mock.patch.object(valheim, "SERVICE_TEMPLATE", TEMPLATES / "template.service"),
            mock.patch.object(valheim, "VALHEIM_ETC_DIR", self.base / "etc"),
            mock.patch.object(valheim, "LOG_DIR", self.base / "log"),
        ):
            patch.start()
            self.addCleanup(patch.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()


class WorldsTest(Base):
    def test_no_data_dir_means_no_worlds(self) -> None:
        self.assertEqual(valheim.find_worlds(self.data_dir), [])

    def test_world_directories_and_old_world_files(self) -> None:
        worlds = self.data_dir / "worlds_local"
        (worlds / "Grollhusen").mkdir(parents=True)
        (worlds / "Grollhusen" / "_main.3.fwl2").write_text("")
        (worlds / "Grollhusen" / "_main.3.db2").write_text("")
        # The file layout older versions used
        (worlds / "alt.fwl").write_text("")
        (worlds / "alt.db").write_text("")
        # Not worlds: an empty directory, a backup, a link
        (worlds / "leer").mkdir()
        (worlds / "alt_backup_auto-20260101.fwl").write_text("")
        (worlds / "verlinkt").symlink_to(worlds / "Grollhusen")

        self.assertEqual(valheim.find_worlds(self.data_dir), ["alt", "Grollhusen"])


LOG = """\
[UnityMemory] Configuration Parameters - Can be set up in boot.config
10/15/2026 11:00:00: Got handshake from client 76561198000000009
10/15/2026 11:00:05: Got character ZDOID from Alter Lauf : -1:1
10/15/2026 11:00:09: Game server connected
[UnityMemory] Configuration Parameters - Can be set up in boot.config
Mono path[0] = '/opt/valheim/valheim_server_Data/Managed'
10/15/2026 12:00:00: Game server connected
10/15/2026 12:01:00: Got handshake from client 76561198000000001
10/15/2026 12:01:05: Got character ZDOID from Ragnar : -1234:1
10/15/2026 12:02:00: Got handshake from client 76561198000000002
10/15/2026 12:02:04: Got character ZDOID from Sigrid Eisenhand : 5678:1
10/15/2026 12:05:00: Got character ZDOID from Ragnar : 0:0
10/15/2026 12:05:30: Got character ZDOID from Ragnar : -1234:2
10/15/2026 12:10:00: Closing socket 76561198000000002
"""


class LogTest(Base):
    def test_only_the_last_run_counts(self) -> None:
        lines = valheim.current_run(LOG)
        self.assertTrue(lines[0].startswith("Mono path[0]"))
        self.assertNotIn("Alter Lauf", "\n".join(lines))

    def test_ready_after_the_line(self) -> None:
        self.assertTrue(valheim.is_ready(valheim.current_run(LOG)))
        self.assertFalse(valheim.is_ready(["Mono path[0] = 'x'", "Load world: x"]))

    def test_players_come_and_go(self) -> None:
        players = valheim.players_from_log(valheim.current_run(LOG))
        # Sigrid left; Ragnar died and came back, and counts once
        self.assertEqual(players, [valheim.Player("Ragnar", "76561198000000001")])

    def test_lines_of_a_real_steam_server(self) -> None:
        # The order a server on the Steam backend writes them in, taken from
        # a live log; ID and name are made up
        lines = [
            "11/22/2025 21:03:28: Got connection SteamID 76561197900000001",
            "11/22/2025 21:03:28: Got handshake from client 76561197900000001",
            "11/22/2025 21:03:57: Got character ZDOID from Halvar : -423468202:1",
        ]
        self.assertEqual(
            valheim.players_from_log(lines),
            [valheim.Player("Halvar", "76561197900000001")],
        )
        lines.append("11/22/2025 21:42:44: Closing socket 76561197900000001")
        self.assertEqual(valheim.players_from_log(lines), [])

    def test_crossplay_players_are_known_by_their_platform_id(self) -> None:
        lines = [
            "PlayFab socket with remote ID playfab/ABC received local Platform ID Steam_76561198000000003",
            "Got character ZDOID from Ylva : 42:1",
        ]
        self.assertEqual(
            valheim.players_from_log(lines),
            [valheim.Player("Ylva", "Steam_76561198000000003")],
        )

    def test_reads_the_log_file(self) -> None:
        path = valheim.log_file(self.server, "Grollhusen")
        path.parent.mkdir(parents=True)
        path.write_text(LOG)
        lines = valheim.read_current_run(path)
        self.assertEqual(valheim.players_from_log(lines)[0].name, "Ragnar")
        self.assertEqual(valheim.read_current_run(path.with_name("none.log")), [])


class RulesTest(Base):
    def setUp(self) -> None:
        super().setUp()
        patch = mock.patch.object(
            valheim, "WORLD_TEMPLATE", TEMPLATES / "template_world.conf"
        )
        patch.start()
        self.addCleanup(patch.stop)

    def test_create_from_nothing(self) -> None:
        # A server that has never started: not even ~/.config is there
        path = valheim.create_rules(self.server, "Nordmark")
        self.assertEqual(path, self.data_dir / "gamemaster" / "Nordmark.conf")
        self.assertIn("VH_PRESET=", path.read_text())
        self.assertEqual(mode(path), 0o660)
        self.assertEqual(mode(self.data_dir / "gamemaster"), 0o2770)
        self.assertEqual(mode(self.data_dir), 0o2750)
        self.assertEqual(mode(self.home / ".config") & 0o070, 0o010)

    def test_create_twice_is_refused(self) -> None:
        valheim.create_rules(self.server, "Nordmark")
        with self.assertRaises(GameMasterError) as caught:
            valheim.create_rules(self.server, "Nordmark")
        self.assertIn("created already", str(caught.exception))

    def test_template_gives_only_the_preset(self) -> None:
        valheim.create_rules(self.server, "Nordmark")
        self.assertEqual(
            valheim.rule_options(self.server, "Nordmark"), ["-preset", "normal"]
        )

    def test_rules_become_options(self) -> None:
        path = valheim.create_rules(self.server, "Nordmark")
        text = path.read_text()
        for old, new in (("VH_PRESET=", "VH_PRESET=hard"),
                         ("VH_RAIDS=", "VH_RAIDS=none"),
                         ("VH_NOMAP=0", "VH_NOMAP=1")):
            text = text.replace(old, new)
        path.write_text(text)
        self.assertEqual(
            valheim.rule_options(self.server, "Nordmark"),
            ["-preset", "hard", "-modifier", "raids", "none", "-setkey", "nomap"],
        )

    def test_wrong_values_are_refused(self) -> None:
        path = valheim.create_rules(self.server, "Nordmark")
        for old, new in (("VH_PRESET=", "VH_PRESET=brutal"),
                         ("VH_COMBAT=", "VH_COMBAT=medium"),
                         ("VH_NOMAP=0", "VH_NOMAP=yes")):
            path.write_text(path.read_text().replace(old, new))
            with self.subTest(new=new), self.assertRaises(GameMasterError):
                valheim.rule_options(self.server, "Nordmark")
            path.write_text(path.read_text().replace(new, old))

    def test_world_without_rules_keeps_its_own(self) -> None:
        self.assertEqual(valheim.rule_options(self.server, "Grollhusen"), [])

    def test_rules_reach_the_service(self) -> None:
        path = valheim.create_rules(self.server, "Nordmark")
        path.write_text(path.read_text().replace("VH_PRESET=", "VH_PRESET=hard"))
        settings = valheim.read_service_settings(self.server)
        unit = valheim.build_unit(self.server, "Nordmark", settings)
        self.assertIn("-world Nordmark -password ${VH_PASSWORD} -public 1 -preset hard\n", unit)

    def test_created_worlds_until_valheim_makes_them(self) -> None:
        valheim.create_rules(self.server, "Nordmark")
        self.assertEqual(valheim.find_created_worlds(self.server), ["Nordmark"])
        world = self.data_dir / "worlds_local" / "Nordmark"
        world.mkdir(parents=True)
        (world / "_main.1.fwl2").write_text("")
        self.assertEqual(valheim.find_created_worlds(self.server), [])

    def test_link_in_place_of_the_rules_is_refused(self) -> None:
        target = self.base / "elsewhere.conf"
        target.write_text("VH_PRESET=hard\n")
        (self.data_dir / "gamemaster").mkdir(parents=True)
        (self.data_dir / "gamemaster" / "Nordmark.conf").symlink_to(target)
        with self.assertRaises(GameMasterError):
            valheim.rule_options(self.server, "Nordmark")


class StateTest(Base):
    def test_server_started_without_gamemaster(self) -> None:
        running = valheim.RunningServer(4242, "Grollhusen")
        with mock.patch.object(valheim, "find_running_server", return_value=running):
            state, found, lines = valheim.server_state(self.server)
            self.assertEqual((state, found, lines), (valheim.UNMANAGED, running, []))

            path = valheim.log_file(self.server, "Grollhusen")
            path.parent.mkdir(parents=True)
            path.write_text("Mono path[0] = 'x'\n")
            self.assertEqual(valheim.server_state(self.server)[0], valheim.STARTING)

            path.write_text("Mono path[0] = 'x'\nGame server connected\n")
            self.assertEqual(valheim.server_state(self.server)[0], valheim.RUNNING)

    def test_nothing_running(self) -> None:
        with mock.patch.object(valheim, "find_running_server", return_value=None):
            self.assertEqual(valheim.server_state(self.server)[0], valheim.NOT_RUNNING)


class ListsTest(Base):
    def setUp(self) -> None:
        super().setUp()
        self.data_dir.mkdir(parents=True)
        (self.data_dir / "bannedlist.txt").write_text(
            "// List banned players ID  ONE per line\n76561198000000001\n"
        )

    def test_read_without_comments(self) -> None:
        self.assertEqual(valheim.read_list(self.server, "banned"), ["76561198000000001"])
        self.assertEqual(valheim.read_list(self.server, "admin"), [])

    def test_add_and_remove_keep_the_comment(self) -> None:
        self.assertTrue(valheim.add_to_list(self.server, "banned", "Steam_76561198000000002"))
        self.assertFalse(valheim.add_to_list(self.server, "banned", "Steam_76561198000000002"))
        self.assertTrue(valheim.remove_from_list(self.server, "banned", "76561198000000001"))
        self.assertFalse(valheim.remove_from_list(self.server, "banned", "76561198000000001"))

        path = self.data_dir / "bannedlist.txt"
        self.assertEqual(
            path.read_text(),
            "// List banned players ID  ONE per line\nSteam_76561198000000002\n",
        )
        self.assertEqual(mode(path), 0o660)

    def test_missing_list_is_created_with_its_header(self) -> None:
        valheim.add_to_list(self.server, "admin", "Steam_76561198000000005")
        path = self.data_dir / "adminlist.txt"
        self.assertEqual(
            path.read_text(),
            "// List admin players ID  ONE per line\nSteam_76561198000000005\n",
        )

    def test_list_that_is_a_link_is_refused(self) -> None:
        target = self.base / "elsewhere.txt"
        target.write_text("untouched\n")
        (self.data_dir / "adminlist.txt").symlink_to(target)
        with self.assertRaises(GameMasterError):
            valheim.add_to_list(self.server, "admin", "Steam_1")
        self.assertEqual(target.read_text(), "untouched\n")

    def test_hard_link_is_refused(self) -> None:
        target = self.base / "elsewhere.txt"
        target.write_text("// header\n")
        os.link(target, self.data_dir / "permittedlist.txt")
        with self.assertRaises(GameMasterError):
            valheim.add_to_list(self.server, "permitted", "Steam_1")
        self.assertEqual(target.read_text(), "// header\n")

    def test_bad_ids_are_refused(self) -> None:
        for text in ("", "Steam_", "a b", "Steam_1\nSteam_2", "../x", "x" * 80):
            with self.subTest(text=text), self.assertRaises(GameMasterError):
                valheim.add_to_list(self.server, "banned", text)


class PermissionsTest(Base):
    def test_without_data_dir(self) -> None:
        self.assertIsNone(valheim.fix_permissions(self.server))
        self.assertEqual(mode(self.home) & 0o050, 0o050)

    def test_sorts_the_parts_and_the_way_there(self) -> None:
        (self.data_dir / "worlds_local" / "Grollhusen").mkdir(parents=True)
        world_file = self.data_dir / "worlds_local" / "Grollhusen" / "_main.1.db2"
        world_file.write_text("")
        for name in ("adminlist.txt", "bannedlist.txt", "permittedlist.txt", "prefs"):
            (self.data_dir / name).write_text("")
        # What the server leaves behind with UMask=0007
        for directory in (".config", ".config/unity3d", ".config/unity3d/IronGate"):
            (self.home / directory).chmod(0o770)

        valheim.fix_permissions(self.server)

        self.assertEqual(mode(self.data_dir), 0o2750)
        self.assertEqual(mode(self.data_dir / "worlds_local"), 0o2770)
        self.assertEqual(mode(world_file), 0o660)
        self.assertEqual(mode(self.data_dir / "bannedlist.txt"), 0o660)
        self.assertEqual(mode(self.data_dir / "prefs"), 0o640)
        # The group may pass through ~/.config and below, nothing more
        for directory in (".config", ".config/unity3d", ".config/unity3d/IronGate"):
            with self.subTest(directory=directory):
                self.assertEqual(mode(self.home / directory) & 0o070, 0o010)


class ServiceTest(Base):
    def test_unit_has_no_password(self) -> None:
        settings = valheim.read_service_settings(self.server)
        unit = valheim.build_unit(self.server, "Grollhusen", settings)
        self.assertNotIn("geheim", unit)
        self.assertNotIn("@", unit)
        lines = unit.splitlines()
        self.assertIn(
            "ExecStart=/opt/valheim/valheim_server.x86_64 -nographics -batchmode "
            "-name ${VH_NAME} -port 2456 -world Grollhusen -password ${VH_PASSWORD} "
            "-public 1",
            lines,
        )
        self.assertIn("KillSignal=SIGINT", lines)
        self.assertIn(f"EnvironmentFile={self.base}/etc/valheim.env", lines)
        self.assertEqual(valheim.unit_world_from_text(unit), "Grollhusen")

    def test_options_and_crossplay(self) -> None:
        self.conf_file.write_text(
            CONF.replace("VH_CROSSPLAY=0", "VH_CROSSPLAY=1")
            + "VH_SAVE_INTERVAL=600\nVH_EXEC_START_PRE_1=/usr/bin/echo $VH_SERVER_PORT\n"
        )
        settings = valheim.read_service_settings(self.server)
        unit = valheim.build_unit(self.server, "Grollhusen", settings)
        self.assertIn("-public 1 -saveinterval 600 -crossplay\n", unit)
        self.assertIn("ExecStartPre=/usr/bin/echo 2456\n", unit)

    def test_password_rules_of_the_server(self) -> None:
        for password, name in (("abcd", "Server"), ("Nord", "Nordlicht")):
            self.conf_file.write_text(
                f"VH_SERVER_NAME={name}\nVH_SERVER_PASSWORD={password}\nVH_SERVER_PORT=2456\n"
            )
            with self.subTest(password=password), self.assertRaises(GameMasterError):
                valheim.read_service_settings(self.server)

    def test_flags_must_be_0_or_1(self) -> None:
        self.conf_file.write_text(CONF.replace("VH_SERVER_PUBLIC=1", "VH_SERVER_PUBLIC=yes"))
        with self.assertRaises(GameMasterError):
            valheim.read_service_settings(self.server)

    def test_environment_file(self) -> None:
        self.conf_file.write_text(
            'VH_SERVER_NAME=Halle "Nord" 100$ a\\b\nVH_SERVER_PASSWORD=ge`heim!\n'
            "VH_SERVER_PORT=2456\n"
        )
        settings = valheim.read_service_settings(self.server)
        (self.base / "etc").mkdir()
        path = valheim.write_environment(self.server, settings)
        self.assertEqual(mode(path), 0o600)
        self.assertIn('VH_NAME="Halle \\"Nord\\" 100\\$ a\\\\b"\n', path.read_text())
        self.assertIn('VH_PASSWORD="ge`heim!"\n', path.read_text())


if __name__ == "__main__":
    unittest.main()
