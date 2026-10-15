"""Handing files to another user, as root, without being led astray by links.

The programs run as root, but the directories they work in belong to a
game server user, and the agent may write in some of them too. Anyone who
can write in a directory can put a symbolic link there in place of a file.
A root program that follows such a link would change a file anywhere on the
machine. So nothing here ever follows a link:

- a directory is entered from its parent with O_NOFOLLOW, one step at a time
- a file is opened with O_NOFOLLOW, and owner and permissions are changed on
  the open file, never by name, so it cannot be swapped in between
- links, hard links and special files are left alone and reported

Which permissions a path gets is decided by the game, not here.
"""

import errno
import os
import stat
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from gamemaster.errors import GameMasterError

DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
NEW_FILE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC


class PermissionsError(GameMasterError):
    """Owner or permissions could not be set."""


class Modes(NamedTuple):
    """The permissions of the files and of the directories in one place."""

    file: int
    directory: int


# The group may change what is there and add to it. The setgid bit makes
# everything created inside belong to the group of the directory, whoever
# creates it.
GROUP_WRITABLE = Modes(0o660, 0o2770)
# The group may look, not touch
GROUP_READABLE = Modes(0o640, 0o2750)
# Nobody but the owner
PRIVATE = Modes(0o600, 0o700)


class Owner(NamedTuple):
    """The user and group a file is handed to."""

    uid: int
    gid: int


class Skipped(NamedTuple):
    """A path that was left alone, and why."""

    path: str
    reason: str


class Report(NamedTuple):
    """What fix_tree did."""

    changed: int
    skipped: list[Skipped]


# ---------------------------------------------------------------------------
# Opening and creating
# ---------------------------------------------------------------------------


@contextmanager
def opened(fd: int) -> Iterator[int]:
    """Close a file descriptor when the with-block ends."""
    try:
        yield fd
    finally:
        os.close(fd)


def open_directory(path: Path) -> int:
    """Open a directory that must not be a link itself."""
    try:
        return os.open(path, DIRECTORY_FLAGS)
    except OSError as error:
        raise PermissionsError(_unusable(path, error)) from error


def make_directories(
    base_fd: int,
    names: tuple[str, ...],
    owner: Owner,
    mode_for: Callable[[tuple[str, ...]], int],
) -> int:
    """Enter or create the directories below base_fd, and return the last one.

    Every step is taken from the directory before it, so no link along the
    way is followed. A directory that is created is handed to owner with the
    mode that mode_for gives for its path below base_fd; one that exists
    already is left as it is.
    """
    fd = os.dup(base_fd)
    for depth, name in enumerate(names, start=1):
        with opened(fd) as parent:
            fd = _enter(parent, name, owner, mode_for(names[:depth]))
    return fd


def _enter(parent_fd: int, name: str, owner: Owner, mode: int) -> int:
    """Open one directory below parent_fd, creating it if it is missing."""
    try:
        os.mkdir(name, 0o700, dir_fd=parent_fd)
        created = True
    except FileExistsError:
        created = False
    except OSError as error:
        raise PermissionsError(f"Could not create {name}: {error}") from error

    try:
        fd = os.open(name, DIRECTORY_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        raise PermissionsError(_unusable(Path(name), error)) from error

    if created:
        try:
            hand_over(fd, owner, mode)
        except BaseException:
            os.close(fd)
            raise

    return fd


def make_directory(parent_fd: int, name: str, owner: Owner, mode: int) -> None:
    """Create a directory that must not exist yet, and hand it to owner."""
    try:
        os.mkdir(name, 0o700, dir_fd=parent_fd)
    except FileExistsError:
        raise PermissionsError(f"{name} already exists.") from None
    except OSError as error:
        raise PermissionsError(f"Could not create {name}: {error}") from error

    try:
        fd = os.open(name, DIRECTORY_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        raise PermissionsError(_unusable(Path(name), error)) from error

    with opened(fd):
        hand_over(fd, owner, mode)


def create_file(
    parent_fd: int, name: str, content: str, owner: Owner, mode: int
) -> None:
    """Write a file that must not exist yet, and hand it to owner.

    O_EXCL refuses a file that is there already, and a link in its place as
    well, so nothing existing is ever overwritten.
    """
    try:
        fd = os.open(name, NEW_FILE_FLAGS, 0o600, dir_fd=parent_fd)
    except FileExistsError:
        raise PermissionsError(f"{name} already exists.") from None
    except OSError as error:
        raise PermissionsError(f"Could not write {name}: {error}") from error

    with opened(fd):
        hand_over(fd, owner, mode)
        try:
            with os.fdopen(os.dup(fd), "w", encoding="utf-8") as new_file:
                new_file.write(content)
        except OSError as error:
            raise PermissionsError(f"Could not write {name}: {error}") from error


def read_text(path: Path, encoding: str = "utf-8") -> str:
    """Return the contents of a file that must not be a link."""
    try:
        fd = os.open(path, FILE_FLAGS)
    except OSError as error:
        raise PermissionsError(_unusable(path, error)) from error

    with opened(fd):
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise PermissionsError(f"{path} is not a regular file.")
        # O_NONBLOCK only served to open it safely; reading must block
        os.set_blocking(fd, True)
        try:
            with os.fdopen(os.dup(fd), encoding=encoding) as source:
                return source.read()
        except (OSError, UnicodeError) as error:
            raise PermissionsError(f"Could not read {path}: {error}") from error


def write_text(path: Path, content: str, owner: Owner, mode: int) -> None:
    """Write a file, which must not be a link, and hand it to owner.

    A file that is there already is changed in place, so it keeps being the
    same file; a missing one is created. The directory above it is entered
    without following a link either.
    """
    with opened(open_directory(path.parent)) as parent_fd:
        try:
            fd = os.open(
                path.name,
                os.O_WRONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                dir_fd=parent_fd,
            )
        except FileNotFoundError:
            create_file(parent_fd, path.name, content, owner, mode)
            return
        except OSError as error:
            raise PermissionsError(_unusable(path, error)) from error

        with opened(fd):
            status = os.fstat(fd)
            if not stat.S_ISREG(status.st_mode):
                raise PermissionsError(f"{path} is not a regular file.")
            if status.st_nlink != 1:
                raise PermissionsError(f"{path} has more than one name (hard link).")
            os.set_blocking(fd, True)
            hand_over(fd, owner, mode)
            try:
                os.ftruncate(fd, 0)
                with os.fdopen(os.dup(fd), "w", encoding="utf-8") as target:
                    target.write(content)
            except OSError as error:
                raise PermissionsError(f"Could not write {path}: {error}") from error


def _unusable(path: Path, error: OSError) -> str:
    """Say why a path could not be opened, naming a link as such."""
    if error.errno == errno.ELOOP:
        return f"{path} is a symbolic link, which is not followed."
    if error.errno == errno.ENOTDIR:
        return f"{path} is not a directory."
    return f"Could not open {path}: {error.strerror}"


# ---------------------------------------------------------------------------
# Changing owner and permissions
# ---------------------------------------------------------------------------


def hand_over(fd: int, owner: Owner, mode: int) -> bool:
    """Give an open file or directory to owner, with mode. Say if it changed."""
    status = os.fstat(fd)
    owner_differs = (status.st_uid, status.st_gid) != owner
    mode_differs = stat.S_IMODE(status.st_mode) != mode

    try:
        # Owner first, and the mode again after it: changing the owner of a
        # file clears its setuid and setgid bits
        if owner_differs:
            os.fchown(fd, owner.uid, owner.gid)
        if owner_differs or mode_differs:
            os.fchmod(fd, mode)
    except OSError as error:
        raise PermissionsError(
            f"Could not set owner or permissions: {error.strerror}"
        ) from error

    return owner_differs or mode_differs


def open_to_group(path: Path) -> bool:
    """Let the group enter and list a directory. Say if it had to be changed.

    Owner and the other permissions stay as they are.
    """
    with opened(open_directory(path)) as fd:
        mode = stat.S_IMODE(os.fstat(fd).st_mode)
        wanted = mode | 0o050
        if wanted == mode:
            return False
        try:
            os.fchmod(fd, wanted)
        except OSError as error:
            raise PermissionsError(
                f"Could not open {path} to its group: {error.strerror}"
            ) from error
        return True


def open_path_to_group(base: Path, names: tuple[str, ...]) -> None:
    """Let the group pass through the directories below base, one by one.

    For a data directory deep below the home, as ~/.config/unity3d/...: the
    group may enter every directory on the way, but neither list nor change
    it. Directories that do not exist yet are left out, as is everything
    after them. Owner and the other permissions stay as they are.
    """
    fd = open_directory(base)
    try:
        for name in names:
            try:
                next_fd = os.open(name, DIRECTORY_FLAGS, dir_fd=fd)
            except FileNotFoundError:
                return
            except OSError as error:
                raise PermissionsError(_unusable(base / name, error)) from error
            os.close(fd)
            fd = next_fd
            base = base / name

            mode = stat.S_IMODE(os.fstat(fd).st_mode)
            wanted = (mode | 0o010) & ~0o020
            if wanted != mode:
                try:
                    os.fchmod(fd, wanted)
                except OSError as error:
                    raise PermissionsError(
                        f"Could not open {base} to its group: {error.strerror}"
                    ) from error
    finally:
        os.close(fd)


def file_mode(modes: Modes, current: int) -> int:
    """Return the mode for a file, keeping it executable if it was."""
    mode = modes.file
    if current & stat.S_IXUSR:
        # x wherever r is granted: 0660 -> 0770, 0640 -> 0750
        mode |= (mode & 0o444) >> 2
    return mode


def fix_tree(
    root: Path, owner: Owner, modes_for: Callable[[tuple[str, ...]], Modes]
) -> Report:
    """Hand everything below root to owner, with the modes the caller wants.

    modes_for is asked with the path below root as a tuple of names, the
    empty tuple standing for root itself. Links are never followed; they are
    reported, just like hard links and special files, and left alone.
    """
    skipped: list[Skipped] = []

    with opened(open_directory(root)) as fd:
        changed = _fix_directory(fd, (), owner, modes_for, skipped)

    return Report(changed, skipped)


def _fix_directory(
    fd: int,
    names: tuple[str, ...],
    owner: Owner,
    modes_for: Callable[[tuple[str, ...]], Modes],
    skipped: list[Skipped],
) -> int:
    """Fix one directory and everything in it; return how much changed."""
    changed = int(hand_over(fd, owner, modes_for(names).directory))

    try:
        entries = sorted(os.listdir(fd))
    except OSError as error:
        raise PermissionsError(
            f"Could not read {'/'.join(names) or '.'}: {error.strerror}"
        ) from error

    for name in entries:
        path = names + (name,)
        try:
            changed += _fix_entry(fd, name, path, owner, modes_for, skipped)
        except FileNotFoundError:
            # Gone while we were looking: nothing left to fix
            continue

    return changed


def _fix_entry(
    parent_fd: int,
    name: str,
    path: tuple[str, ...],
    owner: Owner,
    modes_for: Callable[[tuple[str, ...]], Modes],
    skipped: list[Skipped],
) -> int:
    """Fix one entry of a directory; return how much changed."""
    shown = "/".join(path)
    status = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)

    if stat.S_ISLNK(status.st_mode):
        skipped.append(Skipped(shown, "symbolic link"))
        return 0

    if stat.S_ISDIR(status.st_mode):
        fd = _open_same(parent_fd, name, DIRECTORY_FLAGS, status, shown, skipped)
        if fd is None:
            return 0
        with opened(fd):
            return _fix_directory(fd, path, owner, modes_for, skipped)

    if not stat.S_ISREG(status.st_mode):
        skipped.append(Skipped(shown, "neither file nor directory"))
        return 0

    if status.st_nlink > 1:
        # The same file lives under another name too, possibly outside
        skipped.append(Skipped(shown, "hard link"))
        return 0

    mode = file_mode(modes_for(path), status.st_mode)
    if (status.st_uid, status.st_gid) == owner and stat.S_IMODE(status.st_mode) == mode:
        # Already right; looking was enough, nothing is changed
        return 0

    fd = _open_same(parent_fd, name, FILE_FLAGS, status, shown, skipped)
    if fd is None:
        return 0
    with opened(fd):
        return int(hand_over(fd, owner, mode))


def _open_same(
    parent_fd: int,
    name: str,
    flags: int,
    expected: os.stat_result,
    shown: str,
    skipped: list[Skipped],
) -> int | None:
    """Open an entry, but only if it is still the one that was looked at."""
    try:
        fd = os.open(name, flags, dir_fd=parent_fd)
    except FileNotFoundError:
        raise
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            skipped.append(Skipped(shown, "replaced while being fixed"))
            return None
        raise PermissionsError(f"Could not open {shown}: {error.strerror}") from error

    current = os.fstat(fd)
    if (current.st_dev, current.st_ino) != (expected.st_dev, expected.st_ino) or (
        current.st_nlink > 1 and not stat.S_ISDIR(current.st_mode)
    ):
        os.close(fd)
        skipped.append(Skipped(shown, "replaced while being fixed"))
        return None

    return fd


# ---------------------------------------------------------------------------
# Programs root may run
# ---------------------------------------------------------------------------

# How many links may be followed on the way to a program
MAXIMUM_LINKS = 40


def require_root_only(program: Path) -> Path:
    """Return the real path of a program only root can change, or raise.

    A program that runs as root must be safe from everyone else: the file
    must belong to root and be writable by root alone, and so must every
    directory on the way to it - whoever may write in a directory can put
    another file in place of the program. Links on the way are followed,
    and both the link and where it leads are checked the same way.
    """
    real = _trusted(Path(program), 0)

    status = os.stat(real)
    if not stat.S_ISREG(status.st_mode) or not status.st_mode & stat.S_IXUSR:
        raise PermissionsError(f"{program} is not an executable file.")

    return real


def _trusted(path: Path, links: int) -> Path:
    """Walk to path from /, checking every step; return where it leads."""
    if not path.is_absolute():
        raise PermissionsError(f"{path} is not an absolute path.")

    current = Path("/")
    _require_root_only_entry(current)

    for name in path.parts[1:]:
        candidate = current / name
        try:
            status = os.lstat(candidate)
        except OSError as error:
            raise PermissionsError(f"{candidate}: {error.strerror}") from error

        if stat.S_ISLNK(status.st_mode):
            # The link itself can only be changed by whoever may write in
            # current, which was checked already. Where it leads is checked
            # from the start.
            links += 1
            if links > MAXIMUM_LINKS:
                raise PermissionsError(f"{path}: too many links on the way.")
            target = Path(os.readlink(candidate))
            current = _trusted(
                Path(os.path.normpath(current / target)), links
            )
            continue

        _require_root_only_entry(candidate, status)
        current = candidate

    return current


def _require_root_only_entry(path: Path, status: os.stat_result | None = None) -> None:
    """Raise unless path belongs to root and nobody else may write to it."""
    if status is None:
        status = os.lstat(path)

    if status.st_uid != 0:
        raise PermissionsError(
            f"{path} does not belong to root, so a command run as root may "
            "not depend on it."
        )
    if status.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise PermissionsError(
            f"{path} may be changed by others than root, so a command run as "
            "root may not depend on it."
        )
