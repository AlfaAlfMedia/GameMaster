"""Working with systemd services.

Only the general handling lives here: writing a unit file, and starting,
stopping and asking about a service. Which service belongs to which game
server is decided by that game.
"""

import re
import shutil
import subprocess
from pathlib import Path
from typing import NamedTuple

from gamemaster import permissions, validate
from gamemaster.errors import GameMasterError

UNIT_DIR = Path("/etc/systemd/system")
SYSTEMCTL = "systemctl"

# The unit file is read by systemd, which runs as root, and holds no secrets
UNIT_MODE = 0o644


class ServiceError(GameMasterError):
    """A systemd service could not be written or controlled."""


# ---------------------------------------------------------------------------
# Commands in a unit file
# ---------------------------------------------------------------------------

# Of the prefixes systemd knows for an Exec line, these two are accepted:
IGNORE_FAILURE = "-"  # a failure of the command is not a failure of the service
AS_ROOT = "+"  # the command runs as root, not as the user of the service

COMMAND_PATTERN = re.compile(
    r"(?P<prefix>[-+]{0,2})(?P<program>/\S*)(?:[ \t]+(?P<arguments>.*))?"
)


class Command(NamedTuple):
    """One command of an Exec line: prefix, program and its arguments."""

    prefix: str
    program: Path
    arguments: str

    @property
    def as_root(self) -> bool:
        """Say whether systemd runs this command as root."""
        return AS_ROOT in self.prefix

    @property
    def line(self) -> str:
        """Return the command as it stands after 'ExecStartPre=' and alike."""
        text = f"{self.prefix}{self.program}"
        return f"{text} {self.arguments}" if self.arguments else text


def parse_command(text: str) -> Command:
    """Return a command for an Exec line of a unit file.

    It must start with the absolute path of the program, optionally after
    the prefixes '-' and '+'. Anything that could end the line or start a
    new setting in the unit file is refused.
    """
    match = COMMAND_PATTERN.fullmatch(text.strip())
    if match is None:
        raise ServiceError(
            f"{text!r} is not a command: give the absolute path of the program, "
            f"optionally after '{IGNORE_FAILURE}' and '{AS_ROOT}'."
        )

    prefix = match["prefix"]
    if len(set(prefix)) != len(prefix):
        raise ServiceError(f"{text!r}: each prefix may be given only once.")

    arguments = (match["arguments"] or "").strip()
    if any(ord(character) < 32 or ord(character) == 127 for character in arguments):
        raise ServiceError(f"{text!r} contains a control character.")

    return Command(
        prefix, Path(validate.parse_absolute_path(match["program"])), arguments
    )


# Commands the administrator adds to the service in the configuration of a
# server, numbered from 1: <PREFIX>_EXEC_START_PRE_1, ..._2 and so on.
# setting without the prefix of the game -> line in the unit
HOOK_SETTINGS = {
    "EXEC_START_PRE": "ExecStartPre",
    "EXEC_START_POST": "ExecStartPost",
    "EXEC_STOP_POST": "ExecStopPost",
}


def hook_lines(values: dict[str, str], prefix: str, source: str) -> list[str]:
    """Return the lines the administrator added to a service, checked.

    prefix is the one of the game, as PZ for PZ_EXEC_START_PRE_1. A command
    that runs as root must be out of reach of everyone but root, otherwise
    the server user - or anyone who takes it over - could put its own
    program in its place and have it run as root at the next start.
    """
    lines: list[str] = []

    for setting, directive in HOOK_SETTINGS.items():
        numbered: list[tuple[int, str, str]] = []
        for key, value in values.items():
            match = re.fullmatch(rf"{prefix}_{setting}_([0-9]+)", key)
            if match and value.strip():
                numbered.append((int(match[1]), key, value))

        for _number, key, value in sorted(numbered):
            try:
                command = parse_command(value)
                if command.as_root:
                    permissions.require_root_only(command.program)
            except GameMasterError as error:
                raise GameMasterError(f"{key} in {source}: {error}") from error
            lines.append(f"{directive}={command.line}")

    return lines


def unit_file(name: str) -> Path:
    """Return the path of the unit file of a service."""
    return UNIT_DIR / f"{name}.service"


def exists(name: str) -> bool:
    """Say whether the unit file of a service is there."""
    return unit_file(name).is_file()


def _systemctl(*arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run systemctl and return what it reported."""
    program = shutil.which(SYSTEMCTL)
    if program is None:
        raise ServiceError("systemctl was not found. This system has no systemd.")

    try:
        result = subprocess.run(
            [program, *arguments], capture_output=True, text=True
        )
    except OSError as error:
        raise ServiceError(f"Could not run systemctl: {error}") from error

    if check and result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise ServiceError(
            f"systemctl {' '.join(arguments)} failed: {message or result.returncode}"
        )

    return result


def is_active(name: str) -> bool:
    """Say whether systemd considers the service to be running."""
    result = _systemctl("is-active", "--quiet", f"{name}.service", check=False)
    return result.returncode == 0


def write_unit(name: str, content: str) -> Path:
    """Write the unit file of a service, replacing an older one."""
    path = unit_file(name)

    try:
        path.write_text(content, encoding="utf-8")
        path.chmod(UNIT_MODE)
    except OSError as error:
        raise ServiceError(f"Could not write {path}: {error}") from error

    return path


def daemon_reload() -> None:
    """Make systemd read the unit files again."""
    _systemctl("daemon-reload")


def enable(name: str) -> None:
    """Make the service start when the machine boots."""
    _systemctl("enable", f"{name}.service")


def start(name: str) -> None:
    """Start the service now."""
    _systemctl("start", f"{name}.service")


def stop(name: str) -> None:
    """Stop the service now."""
    _systemctl("stop", f"{name}.service")
