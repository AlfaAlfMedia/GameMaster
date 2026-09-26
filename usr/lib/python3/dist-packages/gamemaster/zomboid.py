"""Knowledge about a Project Zomboid server: its worlds and its commands."""

import os
import pwd
import re
import shutil
from contextlib import ExitStack
from pathlib import Path
from typing import NamedTuple

from gamemaster import (
    configfile, context, permissions, process, service, steamcmd, validate,
)
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

    # Before the first world is created there is nothing here at all, and
    # that is not an error: the server has no worlds yet.
    if not server_dir.is_dir():
        return [], []

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

    def check_mods_need_update(self) -> str:
        """Ask the server whether any of its mods has an update waiting.

        The server writes the answer into its log file, so what comes back
        here only says that the check was started.
        """
        return self.command("checkModsNeedUpdate")

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

    # Read as root from a directory the agent may write in, so a link in
    # place of the file is not followed
    settings = configfile.read_values(
        permissions.read_text(ini_file, encoding="utf-8-sig")
    )

    source = str(ini_file)
    port = validate.parse_port(
        configfile.require(settings, RCON_PORT_KEY, source), RCON_PORT_KEY
    )
    password = configfile.require(settings, RCON_PASSWORD_KEY, source)

    return ZomboidRcon(password, port)


# ---------------------------------------------------------------------------
# The server of one user
# ---------------------------------------------------------------------------

ZOMBOID_ETC_DIR = context.ETC_DIR / "zomboid"

DEFAULT_USER_KEY = "PZ_DEFAULT_USER"

SERVER_USER_KEY = "PZ_SERVER_USER"
INSTALL_DIR_KEY = "PZ_SERVER_INSTALL_DIR"
ADMIN_PASSWORD_KEY = "PZ_SERVER_ADMIN_PASSWORD"
BRANCH_KEY = "PZ_SERVER_BRANCH"
APP_ID_KEY = "PZ_APP_ID"


class Server(NamedTuple):
    """Everything a program needs to know about one registered server."""

    username: str
    server_user: str
    data_dir: Path
    install_dir: Path
    admin_password: str
    branch: str
    conf_file: Path


def config_file(username: str) -> Path:
    """Return the path of the configuration file of one registered server."""
    return ZOMBOID_ETC_DIR / f"{username}.conf"


def username_of(given: str | None) -> str:
    """Return the user from the command line, or PZ_DEFAULT_USER."""
    if given is not None:
        return validate.parse_username(given)

    default = context.gamemaster_settings().get(DEFAULT_USER_KEY)
    if not default:
        raise GameMasterError(
            f"No user given and {DEFAULT_USER_KEY} is not set in "
            f"{context.GAMEMASTER_CONF_FILE}. Use -u/--username to name a user."
        )
    return validate.parse_username(default)


# Project Zomboid keeps everything in this directory below the home of the
# user it runs as; there is no setting for it
DATA_SUBDIR = "Zomboid"


def data_dir_of(server_user: str) -> Path:
    """Return the directory the server of this Linux user keeps its data in."""
    try:
        home = pwd.getpwnam(server_user).pw_dir
    except KeyError:
        raise GameMasterError(
            f"The Linux user '{server_user}' does not exist."
        ) from None
    return Path(home) / DATA_SUBDIR


def load(given_username: str | None) -> Server:
    """Return the registered server of a user, with all values checked."""
    username = username_of(given_username)
    conf_file = config_file(username)

    if not conf_file.is_file():
        raise GameMasterError(
            f"No configuration found for user '{username}': {conf_file}. "
            f"Run 'gamemaster add zomboid -u {username}' first."
        )

    values = context.read_settings(conf_file)
    source = str(conf_file)
    server_user = validate.parse_username(
        configfile.require(values, SERVER_USER_KEY, source)
    )

    return Server(
        username=username,
        server_user=server_user,
        data_dir=data_dir_of(server_user),
        install_dir=Path(
            validate.parse_install_dir(
                configfile.require(values, INSTALL_DIR_KEY, source)
            )
        ),
        admin_password=configfile.require(values, ADMIN_PASSWORD_KEY, source),
        branch=validate.parse_branch(
            configfile.require(values, BRANCH_KEY, source)
        ),
        conf_file=conf_file,
    )


# ---------------------------------------------------------------------------
# A running server
# ---------------------------------------------------------------------------

# The argument that tells the server which world to load. It is the only
# place where the world of a running server is written down.
WORLD_ARGUMENT = "-servername"

# The server itself, and the script that starts it
SERVER_PROGRAM = "ProjectZomboid64"
START_SCRIPT = "start-server.sh"

NOT_RUNNING = "not running"
STARTING = "starting"
PLAYABLE = "playable"


class RunningServer(NamedTuple):
    """A server process that was found, and the world it was told to load."""

    pid: int
    worldname: str
    # True for the server itself, False for the script that started it
    is_server: bool


def find_running_server(server_user: str) -> RunningServer | None:
    """Return the running server of a user, or None if there is none.

    The world is taken from the command line of the process, because that
    is where the server was told which world to load. It is found the same
    way for a server GameMaster started itself and for one that was set up
    by hand.

    The server itself counts more than the script that starts it: the
    script can still be alive while the server is already gone.
    """
    wrapper: RunningServer | None = None

    for pid, arguments in process.processes_of(server_user):
        worldname = process.value_after(arguments, WORLD_ARGUMENT)
        if worldname is None:
            continue

        names = process.program_names(arguments)

        if any(name.startswith(SERVER_PROGRAM) for name in names):
            return RunningServer(pid, worldname, True)
        if START_SCRIPT in names:
            wrapper = RunningServer(pid, worldname, False)

    return wrapper


def server_state(server: Server) -> tuple[str, RunningServer | None]:
    """Return how far along the server of this user is.

    Three answers are possible: it is not running at all, it is on its way
    up but does not answer yet, or it is playable.
    """
    running = find_running_server(server.server_user)

    if running is None:
        return NOT_RUNNING, None
    if not running.is_server:
        return STARTING, running

    try:
        with rcon_for_world(server.data_dir, running.worldname) as connection:
            connection.players()
    except GameMasterError:
        return STARTING, running

    return PLAYABLE, running


def require_running(server: Server) -> RunningServer:
    """Return the running server, or raise if none is playable."""
    state, running = server_state(server)

    if state == NOT_RUNNING:
        raise GameMasterError(
            f"No Project Zomboid server is running for user "
            f"'{server.server_user}'."
        )
    if state == STARTING:
        raise GameMasterError(
            f"The server of user '{server.server_user}' is still starting "
            f"(world '{running.worldname}') and does not answer yet."
        )

    return running


def require_stopped(server: Server, action: str) -> None:
    """Raise if a server is running, naming what would have been done."""
    state, running = server_state(server)

    if state != NOT_RUNNING:
        raise GameMasterError(
            f"The server of user '{server.server_user}' is running with world "
            f"'{running.worldname}' (process {running.pid}). "
            f"Stop it before you {action}."
        )


# ---------------------------------------------------------------------------
# Creating a world
# ---------------------------------------------------------------------------

SHARE_DIR = Path("/usr/share/gamemaster/zomboid")
INI_TEMPLATE = SHARE_DIR / "template.ini"
SANDBOX_TEMPLATE = SHARE_DIR / "template_SandboxVars.lua"
SERVICE_TEMPLATE = SHARE_DIR / "template.service"

LOG_DIR = Path("/var/log/gamemaster/zomboid")

# The setting in the ini file that holds the name shown in the server browser
PUBLIC_NAME_KEY = "PublicName"

# Settings carried over from the configuration of the user into the ini file
# of the world: ini setting -> setting in the user's conf file
INI_FROM_CONF = {
    "RCONPassword": "PZ_SERVER_RCON_PASSWORD",
    "RCONPort": "PZ_RCON_PORT",
    "DefaultPort": "PZ_SERVER_PORT",
    "UDPPort": "PZ_UDP_PORT",
}

PORT_KEYS = ("RCONPort", "DefaultPort", "UDPPort")


def world_paths(data_dir: Path, worldname: str) -> tuple[Path, Path, Path]:
    """Return the three parts of a world: ini file, sandbox file, save dir."""
    server_dir = data_dir / SERVER_SUBDIR
    return (
        server_dir / f"{worldname}.ini",
        server_dir / f"{worldname}_SandboxVars.lua",
        data_dir / MULTIPLAYER_SUBDIR / worldname,
    )


# ---------------------------------------------------------------------------
# Owner and permissions of the data directory
# ---------------------------------------------------------------------------

# Everything below ~/Zomboid belongs to the server user and its group. The
# agent is a member of that group, and what it may do depends on the part of
# the directory:
#
#   Server/   the settings of the worlds          the agent may change them
#   Saves/    the worlds themselves               the agent may change them,
#                                                 e.g. to put a backup back
#   mods/     mods that do not come from Steam    the agent may add them
#   db/       accounts and passwords of a world   only the server
#   the rest  logs, backups, what the server      the agent may read it
#             keeps for itself
#
# Anything new that a later version of the game adds falls under "the rest".
GROUP_WRITABLE_SUBDIRS = ("Server", "Saves", "mods")
PRIVATE_SUBDIRS = (DATABASE_SUBDIR,)


def data_modes(names: tuple[str, ...]) -> permissions.Modes:
    """Return the permissions of a path below the data directory."""
    if names:
        if names[0] in PRIVATE_SUBDIRS:
            return permissions.PRIVATE
        if names[0] in GROUP_WRITABLE_SUBDIRS:
            return permissions.GROUP_WRITABLE
    return permissions.GROUP_READABLE


def owner_of(server: Server) -> permissions.Owner:
    """Return the user and group the files of this server belong to."""
    try:
        account = pwd.getpwnam(server.server_user)
    except KeyError:
        raise GameMasterError(
            f"The Linux user '{server.server_user}' does not exist."
        ) from None
    return permissions.Owner(account.pw_uid, account.pw_gid)


def fix_permissions(server: Server) -> permissions.Report | None:
    """Give the data directory back to the server user, with the right modes.

    Whoever touched the files last - the agent, root putting back a backup,
    an editor that wrote a new file - afterwards they belong to the server
    user and its group again. Returns None if there is no data directory yet.
    """
    home = server.data_dir.parent

    # The agent reaches the data directory through the home directory
    permissions.open_to_group(home)

    # Before the first world there is nothing to fix. A link in place of
    # the directory counts as there, and fix_tree refuses it.
    if not os.path.lexists(server.data_dir):
        return None

    return permissions.fix_tree(server.data_dir, owner_of(server), data_modes)


def build_ini(template: str, worldname: str, server: Server) -> str:
    """Return the ini file of a new world, filled in from the template."""
    values = context.read_settings(server.conf_file)
    source = str(server.conf_file)

    content = configfile.set_value(template, PUBLIC_NAME_KEY, worldname)

    for ini_key, conf_key in INI_FROM_CONF.items():
        value = configfile.require(values, conf_key, source)
        if ini_key in PORT_KEYS:
            value = str(validate.parse_port(value, conf_key))
        content = configfile.set_value(content, ini_key, value)

    return content


def create_world_files(server: Server, worldname: str) -> tuple[Path, Path, Path]:
    """Create the ini file, the sandbox file and the save directory.

    Those three are all a world needs before its first start. Everything
    else is created by the server itself when the world is initialised.
    Missing directories on the way are created as well: the server builds
    them on its first start, but the files of the first world have to be
    written before that ever happens.
    """
    ini_file, sandbox_file, save_dir = world_paths(server.data_dir, worldname)

    ini_content = build_ini(context.read_template(INI_TEMPLATE), worldname, server)
    sandbox_content = context.read_template(SANDBOX_TEMPLATE)

    owner = owner_of(server)
    server_names = (SERVER_SUBDIR,)
    save_names = tuple(Path(MULTIPLAYER_SUBDIR).parts)

    def directory_mode(names: tuple[str, ...]) -> int:
        return data_modes(names).directory

    with ExitStack() as stack:
        def enter(parent_fd: int, names: tuple[str, ...], mode_for) -> int:
            fd = permissions.make_directories(parent_fd, names, owner, mode_for)
            return stack.enter_context(permissions.opened(fd))

        home_fd = stack.enter_context(
            permissions.opened(permissions.open_directory(server.data_dir.parent))
        )
        # The data directory itself is the empty path of the policy
        data_fd = enter(home_fd, (server.data_dir.name,),
                        lambda _names: directory_mode(()))
        server_fd = enter(data_fd, server_names, directory_mode)
        saves_fd = enter(data_fd, save_names, directory_mode)

        for parent_fd, path in (
            (server_fd, ini_file),
            (server_fd, sandbox_file),
            (saves_fd, save_dir),
        ):
            try:
                os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            raise GameMasterError(f"The world '{worldname}' already exists: {path}")

        file_mode = data_modes(server_names).file
        permissions.create_file(server_fd, ini_file.name, ini_content, owner, file_mode)
        permissions.create_file(
            server_fd, sandbox_file.name, sandbox_content, owner, file_mode
        )
        permissions.make_directory(
            saves_fd, save_dir.name, owner, directory_mode(save_names)
        )

    return ini_file, sandbox_file, save_dir


# ---------------------------------------------------------------------------
# The systemd service of a server
# ---------------------------------------------------------------------------

# One service per user, because a user has exactly one server and that
# server has exactly one world: everything is written below ~/Zomboid.
SERVICE_PREFIX = "zomboid"


def unit_name(username: str) -> str:
    """Return the name of the systemd service of one server user."""
    return f"{SERVICE_PREFIX}-{username}"


def log_directory(server: Server) -> Path:
    """Return the directory the output of this server goes into."""
    return LOG_DIR / server.username


def prepare_log_directory(server: Server) -> Path:
    """Create the log directory of this server and hand it to its user."""
    directory = log_directory(server)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        shutil.chown(directory, group=server.server_user)
        directory.chmod(0o750)
    except (OSError, LookupError) as error:
        raise GameMasterError(
            f"Could not prepare {directory}: {error}"
        ) from error
    return directory


# Commands the administrator adds to the service in the configuration of a
# server, numbered from 1: PZ_EXEC_START_PRE_1, PZ_EXEC_START_PRE_2, ...
# setting -> line in the unit
HOOK_SETTINGS = {
    "PZ_EXEC_START_PRE": "ExecStartPre",
    "PZ_EXEC_START_POST": "ExecStartPost",
    "PZ_EXEC_STOP_POST": "ExecStopPost",
}

HOOKS_MARKER = "@HOOKS@"


def unit_hooks(server: Server) -> list[str]:
    """Return the lines the administrator added to the service, checked.

    A command that runs as root must be out of reach of everyone but root,
    otherwise the server user - or anyone who takes it over - could put its
    own program in its place and have it run as root at the next start.
    """
    values = context.read_settings(server.conf_file)
    lines: list[str] = []

    for setting, directive in HOOK_SETTINGS.items():
        numbered: list[tuple[int, str, str]] = []
        for key, value in values.items():
            match = re.fullmatch(rf"{setting}_([0-9]+)", key)
            if match and value.strip():
                numbered.append((int(match[1]), key, value))

        for _number, key, value in sorted(numbered):
            try:
                command = service.parse_command(value)
                if command.as_root:
                    permissions.require_root_only(command.program)
            except GameMasterError as error:
                raise GameMasterError(
                    f"{key} in {server.conf_file}: {error}"
                ) from error
            lines.append(f"{directive}={command.line}")

    return lines


def build_unit(server: Server, worldname: str) -> str:
    """Return the unit file of this server, filled in from the template."""
    log_file = log_directory(server) / f"{worldname}.log"
    hooks = unit_hooks(server)

    content = context.read_template(SERVICE_TEMPLATE)
    for marker, value in (
        # The service runs as the server user, but 'zomboid -u' wants the
        # name the server is registered under. They are usually the same
        # and do not have to be.
        ("@USER@", server.server_user),
        ("@CONF_USER@", server.username),
        ("@WORLD@", worldname),
        ("@INSTALL_DIR@", str(server.install_dir)),
        ("@LOG_FILE@", str(log_file)),
    ):
        content = content.replace(marker, value)

    # The marker has a line of its own, which goes away when there is
    # nothing to put there
    content = content.replace(
        f"{HOOKS_MARKER}\n", "".join(f"{line}\n" for line in hooks)
    )

    return content


def install_unit(server: Server, worldname: str) -> Path:
    """Write the unit file of this server and make systemd read it."""
    prepare_log_directory(server)
    path = service.write_unit(unit_name(server.username), build_unit(server, worldname))
    service.daemon_reload()
    return path


def unit_world(server: Server) -> str | None:
    """Return the world the unit file is set to, or None if there is none."""
    path = service.unit_file(unit_name(server.username))
    if not path.is_file():
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GameMasterError(f"Could not read {path}: {error}") from error

    for line in content.splitlines():
        if line.startswith("ExecStart="):
            return process.value_after(line.split(), WORLD_ARGUMENT)

    return None


def update_server(server: Server, app_id: str) -> None:
    """Update the installed server with SteamCMD."""
    steamcmd.update(
        app_id=validate.parse_app_id(app_id),
        username=server.server_user,
        install_dir=str(server.install_dir),
        branch=server.branch,
    )
