"""Reading and changing configuration files with one KEY=VALUE pair per line."""

import re

from gamemaster.errors import GameMasterError

# A reference to another setting, written as $NAME or ${NAME}
REFERENCE_PATTERN = re.compile(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?")


class ConfigFileError(GameMasterError):
    """A configuration file does not hold what was expected."""


def read_values(text: str) -> dict[str, str]:
    """Return the settings of a configuration file as a dictionary.

    Empty lines and lines starting with '#' are skipped, quotes around a
    value are dropped, and a later line overrides an earlier one. A value
    may refer to a setting defined above it as $NAME or ${NAME}.
    """
    values: dict[str, str] = {}

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # partition splits at the FIRST '=', so a value may contain one
        key, separator, value = line.partition("=")
        if not separator:
            continue

        value = value.strip().strip('"').strip("'")
        values[key.strip()] = _expand(value, values)

    return values


def require(values: dict[str, str], key: str, source: str) -> str:
    """Return the setting, or raise ConfigFileError if it is missing or empty."""
    value = values.get(key)
    if not value:
        raise ConfigFileError(f"{key} is not set in {source}.")
    return value


def set_value(text: str, key: str, value: str) -> str:
    """Return text with every line for key set to value."""
    if "\n" in value or "\r" in value:
        raise ConfigFileError(
            f"The value for {key!r} must not contain a line break."
        )

    # re.escape keeps characters such as '.' in the key from being read as
    # part of the pattern
    pattern = re.compile(rf"[ \t]*{re.escape(key)}=.*")

    lines = text.splitlines(keepends=True)
    found = False

    for number, line in enumerate(lines):
        content = line.rstrip("\r\n")
        line_break = line[len(content):]
        if pattern.fullmatch(content):
            lines[number] = f"{key}={value}{line_break}"
            found = True

    if not found:
        raise ConfigFileError(f"No line for {key!r} found.")

    return "".join(lines)


def _expand(value: str, values: dict[str, str]) -> str:
    """Replace references to settings that were read earlier."""
    return REFERENCE_PATTERN.sub(lambda match: values.get(match.group(1), ""), value)
