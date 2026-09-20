"""Changing configuration files that hold one KEY=VALUE pair per line."""

import re


class ConfigFileError(Exception):
    """A configuration file does not hold what was expected."""


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
