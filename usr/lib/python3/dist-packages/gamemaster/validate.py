"""Checks for values that reach the programs from outside.

Each function returns the checked and normalised value, or raises
ValidationError.
"""

import re
from ipaddress import ip_address

from gamemaster.errors import GameMasterError

USERNAME_PATTERN = re.compile(r"[a-z_][a-z0-9_-]{0,31}")
USERNAME_RULE = (
    "lowercase letters, digits, underscore and hyphen, starting with a "
    "letter or underscore, at most 32 characters"
)

WORLDNAME_PATTERN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_-]{0,31}")
WORLDNAME_RULE = (
    "letters, digits, underscore and hyphen, not starting with a hyphen, "
    "at most 32 characters"
)

# The path ends up in a configuration file that is read back later, so
# quotes, spaces and shell metacharacters are kept out.
INSTALL_DIR_PATTERN = re.compile(r"/[A-Za-z0-9._/-]+")
INSTALL_DIR_RULE = (
    "an absolute path built from letters, digits, dot, underscore, hyphen "
    "and slash"
)

# Ports below 1024 may only be opened by root, and the game servers run as
# their own user
MINIMUM_PORT = 1024
MAXIMUM_PORT = 65535


class ValidationError(GameMasterError):
    """A value from outside does not follow the rules."""


def _checked(value: str, pattern: re.Pattern[str], rule: str) -> str:
    """Return value if it matches pattern, otherwise raise ValidationError."""
    if not pattern.fullmatch(value):
        raise ValidationError(f"{value!r} is not allowed: use {rule}.")
    return value


def parse_username(text: str) -> str:
    """Return the Linux user name."""
    return _checked(text, USERNAME_PATTERN, USERNAME_RULE)


def parse_worldname(text: str) -> str:
    """Return the world name, with spaces replaced by underscores."""
    return _checked(
        text.strip().replace(" ", "_"), WORLDNAME_PATTERN, WORLDNAME_RULE
    )


def parse_port(text: str, name: str = "port") -> int:
    """Return the port as a number a game server may use."""
    try:
        port = int(text)
    except ValueError:
        raise ValidationError(f"{name} {text!r} is not a number.") from None
    if not MINIMUM_PORT <= port <= MAXIMUM_PORT:
        raise ValidationError(
            f"{name} {port} is not between {MINIMUM_PORT} and {MAXIMUM_PORT}."
        )
    return port


def parse_steam_id(text: str) -> str:
    """Return the Steam ID, which consists of digits only."""
    if not text.isdigit():
        raise ValidationError(f"{text!r} is not a Steam ID (digits only).")
    return text


def parse_address(text: str) -> str:
    """Return the network address in its normal form."""
    try:
        return str(ip_address(text))
    except ValueError:
        raise ValidationError(f"{text!r} is not a network address.") from None


def parse_install_dir(text: str) -> str:
    """Return the install directory without trailing slashes."""
    directory = _checked(text.rstrip("/"), INSTALL_DIR_PATTERN, INSTALL_DIR_RULE)
    if ".." in directory:
        raise ValidationError(f"{text!r} is not allowed: '..' is not permitted.")
    return directory
