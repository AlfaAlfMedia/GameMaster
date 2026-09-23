"""Installing and updating a game server with SteamCMD.

SteamCMD is never run as root: Valve advises against it, and the files
have to belong to the user that runs the server afterwards. Which
application is installed is decided by the game, not here.
"""

import os
import pwd
import shutil
import subprocess

from gamemaster.errors import GameMasterError

STEAMCMD = "steamcmd"

# Where the Debian package puts the program if it is not on the PATH
EXTRA_PATH = "/usr/games"

# The name Steam uses for the stable branch
STABLE_BRANCH = "public"

# The Debian wrapper copies SteamCMD into the home of whoever calls it and
# works out where from $HOME and $XDG_DATA_HOME. Those XDG variables may
# still be set to the places of root, so they are taken out: otherwise the
# copy would end up in root's directories instead of the server user's.
XDG_PREFIX = "XDG_"

MISSING_MESSAGE = (
    "SteamCMD was not found. On Debian it is in the package 'steamcmd' from "
    "the section non-free, which also needs the architecture i386: "
    "https://developer.valvesoftware.com/wiki/SteamCMD#Linux"
)


class SteamCmdError(GameMasterError):
    """SteamCMD is missing or did not do its work."""


def find() -> str:
    """Return the path of SteamCMD, or raise if it is not installed."""
    search_path = os.pathsep.join(
        part for part in (os.environ.get("PATH", ""), EXTRA_PATH) if part
    )
    program = shutil.which(STEAMCMD, path=search_path)
    if program is None:
        raise SteamCmdError(MISSING_MESSAGE)
    return program


def _environment(account: pwd.struct_passwd, username: str) -> dict[str, str]:
    """Return the environment SteamCMD is started with."""
    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith(XDG_PREFIX)
    }
    environment["HOME"] = account.pw_dir
    environment["USER"] = username
    environment["LOGNAME"] = username
    return environment


def _run(
    command: list[str], account: pwd.struct_passwd, username: str
) -> subprocess.CompletedProcess:
    """Run SteamCMD as the server user."""
    try:
        return subprocess.run(
            command,
            cwd=account.pw_dir,
            user=username,
            group=account.pw_gid,
            # Without this list SteamCMD would keep the groups of root
            extra_groups=os.getgrouplist(username, account.pw_gid),
            env=_environment(account, username),
        )
    except (OSError, LookupError) as error:
        raise SteamCmdError(f"Could not start SteamCMD: {error}") from error


def update(app_id: str, username: str, install_dir: str, branch: str) -> None:
    """Install or update an application, running as the server user."""
    program = find()

    try:
        account = pwd.getpwnam(username)
    except KeyError:
        raise SteamCmdError(f"The Linux user '{username}' does not exist.") from None

    # SteamCMD brings itself up to date the first time a user runs it, and an
    # app_update in that same run fails with "Missing configuration". So it is
    # started once and told to do nothing; after that the real run works.
    _run([program, "+quit"], account, username)

    command = [
        program,
        "+force_install_dir", install_dir,
        "+login", "anonymous",
        "+app_update", app_id,
    ]
    if branch != STABLE_BRANCH:
        command += ["-beta", branch]
    command += ["validate", "+quit"]

    result = _run(command, account, username)

    if result.returncode != 0:
        raise SteamCmdError(f"SteamCMD ended with exit code {result.returncode}.")
