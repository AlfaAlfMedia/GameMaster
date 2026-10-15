"""Knowledge about a Valheim server: its worlds, its log and its lists.

Valheim has no remote console. A running server is therefore known from
its process and from its log, and the people it lets in are set in three
text files - the admins, the banned and the permitted players - which the
server reads again when they change.
"""

import os
import pwd
import re
import shutil
from pathlib import Path
from typing import NamedTuple

from gamemaster import (
    configfile, context, permissions, process, service, steamcmd, validate,
)
from gamemaster.errors import GameMasterError

# ---------------------------------------------------------------------------
# The server of one user
# ---------------------------------------------------------------------------

VALHEIM_ETC_DIR = context.ETC_DIR / "valheim"

DEFAULT_USER_KEY = "VH_DEFAULT_USER"
APP_ID_KEY = "VH_APP_ID"

SERVER_USER_KEY = "VH_SERVER_USER"
INSTALL_DIR_KEY = "VH_SERVER_INSTALL_DIR"
BRANCH_KEY = "VH_SERVER_BRANCH"
NAME_KEY = "VH_SERVER_NAME"
PASSWORD_KEY = "VH_SERVER_PASSWORD"
PORT_KEY = "VH_SERVER_PORT"
PUBLIC_KEY = "VH_SERVER_PUBLIC"
CROSSPLAY_KEY = "VH_CROSSPLAY"

# Settings that are handed to the server only when they are set, with the
# option they become. Left empty, the server keeps its own default.
OPTIONAL_SETTINGS = {
    "VH_SAVE_INTERVAL": "-saveinterval",
    "VH_BACKUPS": "-backups",
    "VH_BACKUP_SHORT": "-backupshort",
    "VH_BACKUP_LONG": "-backuplong",
}

# The server says so itself: a password shorter than this, or one that is
# part of the name of the server, is not accepted
MINIMUM_PASSWORD_LENGTH = 5

# Valheim keeps its worlds and lists here below the home of the user it
# runs as, unless it is given -savedir, which GameMaster does not do
DATA_SUBDIR = Path(".config/unity3d/IronGate/Valheim")


class Server(NamedTuple):
    """Everything a program needs to know about one registered server."""

    username: str
    server_user: str
    data_dir: Path
    install_dir: Path
    branch: str
    conf_file: Path


def config_file(username: str) -> Path:
    """Return the path of the configuration file of one registered server."""
    return VALHEIM_ETC_DIR / f"{username}.conf"


def username_of(given: str | None) -> str:
    """Return the user from the command line, or VH_DEFAULT_USER."""
    if given is not None:
        return validate.parse_username(given)

    default = context.gamemaster_settings().get(DEFAULT_USER_KEY)
    if not default:
        raise GameMasterError(
            f"No user given and {DEFAULT_USER_KEY} is not set in "
            f"{context.GAMEMASTER_CONF_FILE}. Use -u/--username to name a user."
        )
    return validate.parse_username(default)


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
            f"Run 'gamemaster add valheim -u {username}' first."
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
        branch=validate.parse_branch(
            configfile.require(values, BRANCH_KEY, source)
        ),
        conf_file=conf_file,
    )


# ---------------------------------------------------------------------------
# Worlds
# ---------------------------------------------------------------------------

WORLDS_SUBDIR = "worlds_local"

# A world is a directory of its own with the files of the current save in
# it, _main.<save number>.fwl2 among them. Older versions of the game kept
# a world as two files, <world>.fwl and <world>.db, which a server that was
# set up long ago may still have.
WORLD_FILE_PATTERN = "_main.*.fwl2"
OLD_WORLD_SUFFIX = ".fwl"

# The automatic backups of the server stand beside the worlds and are not
# worlds of their own
BACKUP_MARK = "_backup_"


def find_worlds(data_dir: Path) -> list[str]:
    """Return the names of the worlds the server has created."""
    worlds_dir = data_dir / WORLDS_SUBDIR

    # Before the first start there is nothing here, which is not an error
    if not worlds_dir.is_dir():
        return []

    found: set[str] = set()

    for entry in worlds_dir.iterdir():
        if entry.is_symlink():
            continue
        if entry.is_dir() and any(entry.glob(WORLD_FILE_PATTERN)):
            name = entry.name
        elif entry.is_file() and entry.suffix == OLD_WORLD_SUFFIX:
            name = entry.stem
        else:
            continue

        if BACKUP_MARK in name:
            continue
        try:
            found.add(validate.parse_worldname(name))
        except GameMasterError:
            # A world created by hand under a name GameMaster cannot pass
            # on is left out rather than breaking the list
            continue

    return sorted(found, key=str.lower)


# ---------------------------------------------------------------------------
# A running server
# ---------------------------------------------------------------------------

# The argument that tells the server which world to load. It is the only
# place where the world of a running server is written down.
WORLD_ARGUMENT = "-world"

SERVER_PROGRAM = "valheim_server.x86_64"

NOT_RUNNING = "not running"
STARTING = "starting"
RUNNING = "running"


class RunningServer(NamedTuple):
    """A server process that was found, and the world it was told to load."""

    pid: int
    worldname: str


def find_running_server(server_user: str) -> RunningServer | None:
    """Return the running server of a user, or None if there is none.

    The world is taken from the command line of the process, so a server
    that was set up by hand is found as well as one GameMaster started.
    """
    for pid, arguments in process.processes_of(server_user):
        if SERVER_PROGRAM not in process.program_names(arguments[:1]):
            continue
        worldname = process.value_after(arguments, WORLD_ARGUMENT)
        if worldname is not None:
            return RunningServer(pid, worldname)
    return None


# ---------------------------------------------------------------------------
# The log
# ---------------------------------------------------------------------------

LOG_DIR = Path("/var/log/gamemaster/valheim")

# Every start of the server adds to the same log file. The engine begins
# each start with one of these lines, so the last of them opens the
# current run.
SESSION_MARKERS = ("[UnityMemory] Configuration Parameters", "Mono path[0]")

# The server writes this when it can be joined
READY_LINE = "Game server connected"

# Only the end of a log is read; a server that runs for weeks writes a lot
LOG_TAIL_BYTES = 8 * 1024 * 1024


def log_directory(server: Server) -> Path:
    """Return the directory the output of this server goes into."""
    return LOG_DIR / server.username


def log_file(server: Server, worldname: str) -> Path:
    """Return the log file of one world of this server."""
    return log_directory(server) / f"{worldname}.log"


def prepare_log_directory(server: Server) -> Path:
    """Create the log directory of this server and hand it to its group."""
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


def current_run(text: str) -> list[str]:
    """Return the lines of the last start of the server in a log."""
    lines = text.splitlines()
    start = 0
    for number, line in enumerate(lines):
        if line.startswith(SESSION_MARKERS):
            start = number
    return lines[start:]


def read_current_run(path: Path) -> list[str]:
    """Return the lines of the last start of the server from its log file."""
    try:
        with open(path, "rb") as source:
            source.seek(0, os.SEEK_END)
            size = source.tell()
            source.seek(max(0, size - LOG_TAIL_BYTES))
            data = source.read()
    except FileNotFoundError:
        return []
    except OSError as error:
        raise GameMasterError(f"Could not read {path}: {error}") from error

    return current_run(data.decode("utf-8", "replace"))


def is_ready(lines: list[str]) -> bool:
    """Say whether the server has said it can be joined."""
    return any(READY_LINE in line for line in lines)


# What the server writes when somebody comes and goes. A connection is
# known by the ID of its peer; the name of the character follows once the
# player has spawned. The order of the lines is what ties the two together.
CONNECTION_PATTERN = re.compile(
    r"Got (?:handshake from client|connection SteamID) (?P<peer>\S+)"
)
PLATFORM_PATTERN = re.compile(
    r"PlayFab socket with remote ID (?P<peer>\S+) received local Platform ID "
    r"(?P<platform>\S+)"
)
CHARACTER_PATTERN = re.compile(
    r"Got character ZDOID from (?P<name>.+?) : (?P<zdo>-?[0-9]+):(?P<number>[0-9]+)"
)
CLOSING_PATTERN = re.compile(r"Closing socket (?P<peer>\S+)")


class Player(NamedTuple):
    """A player that is connected, as far as the log tells."""

    name: str
    peer: str


def players_from_log(lines: list[str]) -> list[Player]:
    """Return the players that are connected according to the log.

    Valheim offers no other way to ask: the log of the current run is read
    from its start, and whoever connected and has not been disconnected
    since counts as being there.
    """
    connected: dict[str, str] = {}
    waiting: list[str] = []

    for line in lines:
        if match := CONNECTION_PATTERN.search(line):
            peer = match["peer"]
            if peer not in connected and peer not in waiting:
                waiting.append(peer)
        elif match := PLATFORM_PATTERN.search(line):
            # Crossplay: the remote ID stands for the platform ID that
            # follows, which is what the lists of the server use
            peer = match["platform"]
            if peer not in connected and peer not in waiting:
                waiting.append(peer)
        elif match := CHARACTER_PATTERN.search(line):
            # The number after the colon is 0 when a character dies; the
            # player is still connected
            if match["number"] == "0":
                continue
            name = match["name"].strip()
            if name in connected.values():
                continue
            peer = waiting.pop(0) if waiting else ""
            connected[peer or name] = name
        elif match := CLOSING_PATTERN.search(line):
            peer = match["peer"]
            connected.pop(peer, None)
            if peer in waiting:
                waiting.remove(peer)

    return [
        Player(name, "" if peer == name else peer)
        for peer, name in connected.items()
    ]


def server_state(server: Server) -> tuple[str, RunningServer | None, list[str]]:
    """Return how far along the server of this user is, with its log lines.

    Three answers are possible: it is not running at all, it is on its way
    up but cannot be joined yet, or it is running.
    """
    running = find_running_server(server.server_user)
    if running is None:
        return NOT_RUNNING, None, []

    lines = read_current_run(log_file(server, running.worldname))
    return (RUNNING if is_ready(lines) else STARTING), running, lines


def require_stopped(server: Server, action: str) -> None:
    """Raise if a server is running, naming what would have been done."""
    running = find_running_server(server.server_user)
    if running is not None:
        raise GameMasterError(
            f"The server of user '{server.server_user}' is running with world "
            f"'{running.worldname}' (process {running.pid}). "
            f"Stop it before you {action}."
        )


# ---------------------------------------------------------------------------
# Admins, banned and permitted players
# ---------------------------------------------------------------------------

# list -> file in the data directory. The server creates the files on its
# first start, each with a comment line at the top.
LISTS = {
    "admin": "adminlist.txt",
    "banned": "bannedlist.txt",
    "permitted": "permittedlist.txt",
}

LIST_HEADERS = {
    "admin": "// List admin players ID  ONE per line",
    "banned": "// List banned players ID  ONE per line",
    "permitted": "// List permitted players ID ONE per line",
}

COMMENT = "//"

# The ID of a player as the server writes it into its log and its lists:
# the platform and the user ID on it, as Steam_76561198000000000. Lists
# written by older versions hold the bare Steam ID.
PLAYER_ID_PATTERN = re.compile(r"(?:[A-Za-z]+_)?[A-Za-z0-9]{1,64}")


def parse_player_id(text: str) -> str:
    """Return the ID of a player for one of the lists."""
    if not PLAYER_ID_PATTERN.fullmatch(text):
        raise GameMasterError(
            f"{text!r} is not a player ID: use the platform and the ID on it, "
            f"as Steam_76561198000000000."
        )
    return text


def list_path(server: Server, name: str) -> Path:
    """Return the file of one of the lists of the server."""
    return server.data_dir / LISTS[name]


def read_list(server: Server, name: str) -> list[str]:
    """Return the player IDs on one of the lists."""
    path = list_path(server, name)
    if not os.path.lexists(path):
        return []

    # Read as root from a directory the agent may write in, so a link in
    # place of the file is not followed
    text = permissions.read_text(path)
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith(COMMENT)
    ]


def write_list(server: Server, name: str, entries: list[str]) -> Path:
    """Write one of the lists, keeping the comment lines at its top."""
    path = list_path(server, name)

    comments: list[str] = []
    if os.path.lexists(path):
        comments = [
            line for line in permissions.read_text(path).splitlines()
            if line.strip().startswith(COMMENT)
        ]
    if not comments:
        comments = [LIST_HEADERS[name]]

    if not server.data_dir.is_dir():
        raise GameMasterError(
            f"{server.data_dir} does not exist yet. Start the server once, "
            f"which creates it."
        )

    content = "".join(f"{line}\n" for line in comments + entries)
    permissions.write_text(path, content, owner_of(server), data_modes((path.name,)).file)
    return path


def add_to_list(server: Server, name: str, player_id: str) -> bool:
    """Put a player on a list. Say whether it had to be added."""
    player_id = parse_player_id(player_id)
    entries = read_list(server, name)
    if player_id in entries:
        return False
    write_list(server, name, entries + [player_id])
    return True


def remove_from_list(server: Server, name: str, player_id: str) -> bool:
    """Take a player off a list. Say whether it was on it."""
    player_id = parse_player_id(player_id)
    entries = read_list(server, name)
    if player_id not in entries:
        return False
    write_list(server, name, [entry for entry in entries if entry != player_id])
    return True


# ---------------------------------------------------------------------------
# Owner and permissions of the data directory
# ---------------------------------------------------------------------------

# Everything below ~/.config/unity3d/IronGate/Valheim belongs to the server
# user and its group. The agent is a member of that group, and what it may
# do depends on the part of the directory:
#
#   worlds_local/   the worlds                     the agent may change them,
#                                                  e.g. to put a backup back
#   the lists       admins, banned, permitted      the agent may change them
#   the rest        what the server keeps for      the agent may read it
#                   itself
#
# Anything new that a later version of the game adds falls under "the rest".
GROUP_WRITABLE_NAMES = (WORLDS_SUBDIR, *LISTS.values())


def data_modes(names: tuple[str, ...]) -> permissions.Modes:
    """Return the permissions of a path below the data directory."""
    if names and names[0] in GROUP_WRITABLE_NAMES:
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

    Returns None if there is no data directory yet: the server creates it
    on its first start, and the service sorts it before the next one.
    """
    home = server.data_dir.parents[len(DATA_SUBDIR.parts) - 1]

    # The agent reaches the data directory through the home directory and
    # the directories below it, which it may pass but not look into
    permissions.open_to_group(home)
    permissions.open_path_to_group(home, DATA_SUBDIR.parts[:-1])

    # A link in place of the directory counts as there, and fix_tree
    # refuses it
    if not os.path.lexists(server.data_dir):
        return None

    return permissions.fix_tree(server.data_dir, owner_of(server), data_modes)


# ---------------------------------------------------------------------------
# The systemd service of a server
# ---------------------------------------------------------------------------

SHARE_DIR = Path("/usr/share/gamemaster/valheim")
SERVICE_TEMPLATE = SHARE_DIR / "template.service"

# One service per user, because the worlds of a user share one data
# directory and the server can load only one of them at a time
SERVICE_PREFIX = "valheim"

HOOKS_MARKER = "@HOOKS@"


def unit_name(username: str) -> str:
    """Return the name of the systemd service of one server user."""
    return f"{SERVICE_PREFIX}-{username}"


def environment_file(server: Server) -> Path:
    """Return the file the service takes the name and password from.

    They go there rather than into the unit, which everyone may read. The
    server only takes them on its command line, though, so while it runs
    they can be seen in the list of processes all the same.
    """
    return VALHEIM_ETC_DIR / f"{server.username}.env"


def _flag(values: dict[str, str], key: str, source: str) -> bool:
    """Return a setting that is 1 or 0."""
    value = values.get(key, "0").strip() or "0"
    if value not in ("0", "1"):
        raise GameMasterError(f"{key} in {source} must be 0 or 1, not {value!r}.")
    return value == "1"


def _text(values: dict[str, str], key: str, source: str) -> str:
    """Return a setting that is passed on to the server as it is."""
    value = configfile.require(values, key, source)
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise GameMasterError(f"{key} in {source} contains a control character.")
    return value


class Settings(NamedTuple):
    """What the service hands to the server, checked."""

    name: str
    password: str
    port: int
    public: bool
    crossplay: bool
    options: list[str]


def read_service_settings(server: Server) -> Settings:
    """Return the settings of the server from its configuration, checked."""
    values = context.read_settings(server.conf_file)
    source = str(server.conf_file)

    name = _text(values, NAME_KEY, source)
    password = _text(values, PASSWORD_KEY, source)

    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise GameMasterError(
            f"{PASSWORD_KEY} in {source} must have at least "
            f"{MINIMUM_PASSWORD_LENGTH} characters; the server refuses a "
            f"shorter one."
        )
    if password in name:
        raise GameMasterError(
            f"{PASSWORD_KEY} in {source} must not be part of {NAME_KEY}; "
            f"the server refuses that."
        )

    options: list[str] = []
    for key, option in OPTIONAL_SETTINGS.items():
        value = values.get(key, "").strip()
        if not value:
            continue
        if not value.isdigit():
            raise GameMasterError(f"{key} in {source} must be a number, not {value!r}.")
        options += [option, value]

    return Settings(
        name=name,
        password=password,
        port=validate.parse_port(
            configfile.require(values, PORT_KEY, source), PORT_KEY
        ),
        public=_flag(values, PUBLIC_KEY, source),
        crossplay=_flag(values, CROSSPLAY_KEY, source),
        options=options,
    )


def unit_hooks(server: Server) -> list[str]:
    """Return the lines the administrator added to the service, checked."""
    return service.hook_lines(
        context.read_settings(server.conf_file), "VH", str(server.conf_file)
    )


def _quoted(value: str) -> str:
    """Return a value for an environment file of systemd, in double quotes."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")
    return f'"{escaped}"'


def build_environment(settings: Settings) -> str:
    """Return the environment file of the service."""
    return (
        "# Written by GameMaster from the configuration of the server; it is\n"
        "# replaced whenever the service is written. Do not edit it by hand.\n"
        f"VH_NAME={_quoted(settings.name)}\n"
        f"VH_PASSWORD={_quoted(settings.password)}\n"
    )


def build_unit(server: Server, worldname: str, settings: Settings) -> str:
    """Return the unit file of this server, filled in from the template."""
    hooks = unit_hooks(server)

    options = list(settings.options)
    if settings.crossplay:
        options.append("-crossplay")

    content = context.read_template(SERVICE_TEMPLATE)
    for marker, value in (
        # The service runs as the server user, but 'valheim -u' wants the
        # name the server is registered under. They are usually the same
        # and do not have to be.
        ("@USER@", server.server_user),
        ("@CONF_USER@", server.username),
        ("@WORLD@", worldname),
        ("@INSTALL_DIR@", str(server.install_dir)),
        ("@LOG_FILE@", str(log_file(server, worldname))),
        ("@ENV_FILE@", str(environment_file(server))),
        ("@PORT@", str(settings.port)),
        ("@PUBLIC@", "1" if settings.public else "0"),
        ("@OPTIONS@", "".join(f" {option}" for option in options)),
    ):
        content = content.replace(marker, value)

    # The marker has a line of its own, which goes away when there is
    # nothing to put there
    content = content.replace(
        f"{HOOKS_MARKER}\n", "".join(f"{line}\n" for line in hooks)
    )

    return content


def write_environment(server: Server, settings: Settings) -> Path:
    """Write the environment file of the service, for root's eyes only."""
    path = environment_file(server)
    try:
        # Created with 0600 straight away, so the password is never
        # readable for others, not even for a moment
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as target:
            os.fchmod(target.fileno(), 0o600)
            target.write(build_environment(settings))
    except OSError as error:
        raise GameMasterError(f"Could not write {path}: {error}") from error
    return path


def install_unit(server: Server, worldname: str) -> Path:
    """Write the unit file of this server and make systemd read it."""
    settings = read_service_settings(server)
    content = build_unit(server, worldname, settings)

    prepare_log_directory(server)
    write_environment(server, settings)
    path = service.write_unit(unit_name(server.username), content)
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

    return unit_world_from_text(content)


def unit_world_from_text(content: str) -> str | None:
    """Return the world a unit file loads, or None if it names none."""
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
