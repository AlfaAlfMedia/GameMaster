"""Knowledge about a Project Zomboid server: its worlds and its commands."""

from pathlib import Path

from gamemaster import configfile, validate
from gamemaster.errors import GameMasterError
from gamemaster.rcon import Rcon, RconError, quoted

SERVER_SUBDIR = "Server"
MULTIPLAYER_SUBDIR = "Saves/Multiplayer"
DATABASE_SUBDIR = "db"

RCON_PORT_KEY = "RCONPort"
RCON_PASSWORD_KEY = "RCONPassword"

ACCESS_LEVELS = ("admin", "moderator", "overseer", "gm", "observer")


# ---------------------------------------------------------------------------
# Worlds
# ---------------------------------------------------------------------------


def world_ini_file(data_dir: Path, worldname: str) -> Path:
    """Return the path of the settings file of one world."""
    return data_dir / SERVER_SUBDIR / f"{worldname}.ini"


def find_worlds(data_dir: Path) -> tuple[list[str], list[str]]:
    """Return the playable worlds and the ones that are not initialised yet.

    A world counts as created when all three parts are there: the ini file,
    the sandbox file and the save directory. It counts as playable when a
    database belongs to it as well. Anything incomplete is left out.
    """
    server_dir = data_dir / SERVER_SUBDIR
    multiplayer_dir = data_dir / MULTIPLAYER_SUBDIR
    database_dir = data_dir / DATABASE_SUBDIR

    if not server_dir.is_dir():
        raise GameMasterError(f"{server_dir} does not exist.")

    playable: list[str] = []
    created: list[str] = []

    for ini_file in sorted(server_dir.glob("*.ini"), key=lambda p: p.stem.lower()):
        name = ini_file.stem

        sandbox_file = server_dir / f"{name}_SandboxVars.lua"
        if not sandbox_file.is_file() or not (multiplayer_dir / name).is_dir():
            continue

        if (database_dir / f"{name}.db").is_file():
            playable.append(name)
        else:
            created.append(name)

    return playable, created


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


class ZomboidRcon(Rcon):
    """An RCON connection that knows the commands of a Zomboid server.

    It can do everything a plain Rcon connection can do and adds one method
    per command. Commands are sent without the leading slash that the
    in-game chat uses.
    """

    def quit_server(self) -> str:
        """Save the world and shut the server down."""
        return self.command("quit")

    def save(self) -> str:
        """Save the world without stopping the server."""
        return self.command("save")

    def server_message(self, text: str) -> str:
        """Send a message to every player on the server."""
        return self.command(f"servermsg {quoted(text)}")

    def players(self) -> str:
        """List the players that are currently connected."""
        return self.command("players")

    def kick_user(self, name: str, reason: str | None = None) -> str:
        """Throw a player off the server."""
        command = f"kickuser {quoted(name)}"
        if reason:
            command += f" -r {quoted(reason)}"
        return self.command(command)

    def ban_user(
        self, name: str, reason: str | None = None, with_address: bool = False
    ) -> str:
        """Ban a player by name, optionally by network address as well."""
        command = f"banuser {quoted(name)}"
        if with_address:
            command += " -ip"
        if reason:
            command += f" -r {quoted(reason)}"
        return self.command(command)

    def unban_user(self, name: str) -> str:
        """Lift the ban on a player name."""
        return self.command(f"unbanuser {quoted(name)}")

    def ban_steam_id(self, steam_id: str) -> str:
        """Ban a player by Steam ID, which works while they are offline."""
        return self.command(f"banid {validate.parse_steam_id(steam_id)}")

    def unban_steam_id(self, steam_id: str) -> str:
        """Lift the ban on a Steam ID."""
        return self.command(f"unbanid {validate.parse_steam_id(steam_id)}")

    def ban_address(self, address: str) -> str:
        """Ban a network address."""
        return self.command(f"banip {validate.parse_address(address)}")

    def unban_address(self, address: str) -> str:
        """Lift the ban on a network address."""
        return self.command(f"unbanip {validate.parse_address(address)}")

    def show_options(self) -> str:
        """Return all server options with their current values."""
        return self.command("showoptions")

    def change_option(self, name: str, value: str) -> str:
        """Change one server option while the server is running."""
        if not name.isalnum():
            raise RconError(f"{name!r} is not a valid option name.")
        return self.command(f"changeoption {name} {quoted(value)}")

    def reload_options(self) -> str:
        """Make the server read its configuration file again."""
        return self.command("reloadoptions")

    def set_access_level(self, name: str, level: str) -> str:
        """Give a player one of the permission levels of the server."""
        if level not in ACCESS_LEVELS:
            raise RconError(
                f"{level!r} is not a permission level: {', '.join(ACCESS_LEVELS)}."
            )
        return self.command(f"setaccesslevel {quoted(name)} {level}")


def rcon_for_world(data_dir: Path, worldname: str) -> ZomboidRcon:
    """Return a connection for one world, with port and password from its ini.

    The connection is not opened yet, so it can be used in a with-block.
    """
    ini_file = world_ini_file(data_dir, worldname)

    try:
        settings = configfile.read_values(ini_file.read_text(encoding="utf-8-sig"))
    except OSError as error:
        raise GameMasterError(f"Could not read {ini_file}: {error}") from error

    source = str(ini_file)
    port = validate.parse_port(
        configfile.require(settings, RCON_PORT_KEY, source), RCON_PORT_KEY
    )
    password = configfile.require(settings, RCON_PASSWORD_KEY, source)

    return ZomboidRcon(password, port)
