"""What every GameMaster program needs before it can do its work.

Reading the general configuration, checking that the program runs as root,
reporting a line to whoever called us, and turning an error into a message
and an exit code. Nothing here knows about a particular game.
"""

import argparse
import os
import re
import sys
from collections.abc import Callable
from pathlib import Path

from gamemaster import configfile
from gamemaster.errors import GameMasterError

ETC_DIR = Path("/etc/gamemaster")
GAMEMASTER_CONF_FILE = ETC_DIR / "gamemaster.conf"


def report(message: str) -> None:
    """Print one line about what is happening, for whoever called us."""
    print(message, flush=True)


def require_root() -> None:
    """End with an error if the program is not run as root."""
    if os.geteuid() != 0:
        raise GameMasterError(
            "This command must be run as root (for example with sudo)."
        )


def read_settings(path: Path) -> dict[str, str]:
    """Return the settings of a configuration file."""
    try:
        return configfile.read_values(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise GameMasterError(f"Could not read {path}: {error}") from error


def read_template(path: Path) -> str:
    """Return the contents of a template file."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise GameMasterError(
            f"Could not read the template {path}: {error}"
        ) from error


def gamemaster_settings() -> dict[str, str]:
    """Return the settings that apply to the whole machine."""
    return read_settings(GAMEMASTER_CONF_FILE)


class ArgumentParser(argparse.ArgumentParser):
    """A command line that answers a wrong command with the commands there are.

    All GameMaster programs use it, so a command a program does not know -
    because the game cannot do it, or because of a typing error - is met
    the same way everywhere: the help of the level the mistake is on, then
    the ERROR line every failure ends with, and the exit code 1.
    """

    def error(self, message: str) -> None:
        self.print_help()
        # The help goes to standard output, the ERROR line to standard
        # error; the help must be out first, so the ERROR line is the last
        sys.stdout.flush()
        choice = re.search(r"invalid choice: '([^']*)'", message)
        if choice:
            message = (
                f"'{choice[1]}' is not a command of {self.prog}. "
                f"The commands are listed above."
            )
        else:
            message = f"{message[:1].upper()}{message[1:]}. See above."
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)


def run(action: Callable[[], None]) -> int:
    """Carry out the program and return its exit code (0 = everything ok)."""
    try:
        action()
    except GameMasterError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        return 1
    return 0
