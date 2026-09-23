"""Finding the running processes of a Linux user.

Only the general mechanism lives here: which processes belong to a user,
and with which arguments they were started. What those arguments mean
belongs to the game that uses them.

The list of processes is read from /proc. A process can end while it is
being looked at, so anything that cannot be read is left out instead of
raising.
"""

import pwd
from pathlib import Path

from gamemaster.errors import GameMasterError

PROC_DIR = Path("/proc")


class ProcessError(GameMasterError):
    """The processes of a user could not be determined."""


def user_id(username: str) -> int:
    """Return the numeric id of a Linux user."""
    try:
        return pwd.getpwnam(username).pw_uid
    except KeyError:
        raise ProcessError(f"The Linux user '{username}' does not exist.") from None


def _arguments(entry: Path) -> list[str]:
    """Return the command line of one process, or an empty list."""
    try:
        raw = (entry / "cmdline").read_bytes()
    except OSError:
        # The process has ended, or its command line may not be read
        return []
    return [part.decode("utf-8", "replace") for part in raw.split(b"\x00") if part]


def _owner(entry: Path) -> int | None:
    """Return the id of the user a process belongs to, or None."""
    try:
        return entry.stat().st_uid
    except OSError:
        return None


def processes_of(username: str) -> list[tuple[int, list[str]]]:
    """Return the process number and command line of every process of a user."""
    wanted = user_id(username)
    found: list[tuple[int, list[str]]] = []

    try:
        entries = list(PROC_DIR.iterdir())
    except OSError as error:
        raise ProcessError(f"Could not read {PROC_DIR}: {error}") from error

    for entry in entries:
        if not entry.name.isdigit():
            continue
        if _owner(entry) != wanted:
            continue
        arguments = _arguments(entry)
        if arguments:
            found.append((int(entry.name), arguments))

    return found


def value_after(arguments: list[str], option: str) -> str | None:
    """Return what follows an option, as 'X' in ['-servername', 'X']."""
    for position, argument in enumerate(arguments[:-1]):
        if argument == option:
            return arguments[position + 1]
    return None


def program_names(arguments: list[str]) -> list[str]:
    """Return the file names in a command line, without their directories."""
    return [Path(argument).name for argument in arguments]
