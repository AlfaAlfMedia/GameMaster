"""Working with systemd services.

Only the general handling lives here: writing a unit file, and starting,
stopping and asking about a service. Which service belongs to which game
server is decided by that game.
"""

import shutil
import subprocess
from pathlib import Path

from gamemaster.errors import GameMasterError

UNIT_DIR = Path("/etc/systemd/system")
SYSTEMCTL = "systemctl"

# The unit file is read by systemd, which runs as root, and holds no secrets
UNIT_MODE = 0o644


class ServiceError(GameMasterError):
    """A systemd service could not be written or controlled."""


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
