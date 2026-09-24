"""Public SSH keys and the authorized_keys file of a Linux user.

A key that reaches us from outside is checked here before it is written:
it has to be one line, of a known type, and its data has to be readable.
The fingerprint is worked out the same way OpenSSH does it, so that the
one shown here can be compared with 'ssh-keygen -l'.

Nothing here knows about a game or about GameMaster.
"""

import base64
import binascii
import hashlib
import os
import pwd
import struct
from pathlib import Path
from typing import NamedTuple

from gamemaster.errors import GameMasterError

SSH_DIR_NAME = ".ssh"
AUTHORIZED_KEYS_NAME = "authorized_keys"

# Only the user may enter the directory or read the file; OpenSSH refuses
# to use them otherwise
SSH_DIR_MODE = 0o700
AUTHORIZED_KEYS_MODE = 0o600

KEY_TYPES = (
    "ssh-ed25519",
    "ssh-rsa",
    "ecdsa-sha2-nistp256",
    "ecdsa-sha2-nistp384",
    "ecdsa-sha2-nistp521",
    "sk-ssh-ed25519@openssh.com",
    "sk-ecdsa-sha2-nistp256@openssh.com",
)

MAXIMUM_KEY_LENGTH = 16 * 1024


class SshKeyError(GameMasterError):
    """A public key is not usable."""


class PublicKey(NamedTuple):
    """One public key, as it stands in an authorized_keys file."""

    type: str
    data: str
    comment: str

    @property
    def line(self) -> str:
        """Return the key as one line for the authorized_keys file."""
        return " ".join(part for part in (self.type, self.data, self.comment) if part)

    @property
    def fingerprint(self) -> str:
        """Return the fingerprint, as 'ssh-keygen -l' shows it."""
        digest = hashlib.sha256(base64.b64decode(self.data)).digest()
        return "SHA256:" + base64.b64encode(digest).decode("ascii").rstrip("=")


def parse(text: str) -> PublicKey:
    """Return the public key in the text, or raise SshKeyError."""
    if len(text) > MAXIMUM_KEY_LENGTH:
        raise SshKeyError("The key is far too long to be a public key.")

    line = text.strip()
    if not line or line.startswith("#"):
        raise SshKeyError("No key given.")
    if "\n" in line or "\r" in line:
        raise SshKeyError("A public key has to be one single line.")

    parts = line.split()
    if len(parts) < 2:
        raise SshKeyError(
            "A public key looks like 'ssh-ed25519 AAAA... comment'."
        )

    key_type, data = parts[0], parts[1]
    comment = " ".join(parts[2:])

    if key_type not in KEY_TYPES:
        raise SshKeyError(
            f"{key_type!r} is not a key type this program knows: "
            f"{', '.join(KEY_TYPES)}."
        )

    try:
        blob = base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError):
        raise SshKeyError("The data of the key is not readable.") from None

    # The key repeats its own type in the first field of its data. If that
    # does not match, the line was put together wrongly.
    try:
        (length,) = struct.unpack(">I", blob[:4])
        inner_type = blob[4:4 + length].decode("ascii")
    except (struct.error, UnicodeDecodeError):
        raise SshKeyError("The data of the key is not readable.") from None

    if inner_type != key_type:
        raise SshKeyError(
            f"The key says it is {key_type!r}, but its data says "
            f"{inner_type!r}."
        )

    return PublicKey(key_type, data, comment)


def _account(username: str) -> pwd.struct_passwd:
    """Return the account of a Linux user."""
    try:
        return pwd.getpwnam(username)
    except KeyError:
        raise SshKeyError(f"The Linux user '{username}' does not exist.") from None


def authorized_keys_file(username: str) -> Path:
    """Return the path of the authorized_keys file of a user."""
    return Path(_account(username).pw_dir) / SSH_DIR_NAME / AUTHORIZED_KEYS_NAME


def read_keys(username: str) -> list[PublicKey]:
    """Return the keys in the authorized_keys file of a user.

    A line that cannot be read is left out rather than stopping the
    program: the file may have been edited by hand.
    """
    path = authorized_keys_file(username)
    if not path.is_file():
        return []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise SshKeyError(f"Could not read {path}: {error}") from error

    keys: list[PublicKey] = []
    for line in text.splitlines():
        try:
            keys.append(parse(line))
        except SshKeyError:
            continue

    return keys


def add_key(username: str, key: PublicKey) -> Path:
    """Append a key to the authorized_keys file of a user.

    The directory and the file are created if they are missing and are
    given to the user, because OpenSSH refuses keys it does not own.
    """
    account = _account(username)
    directory = Path(account.pw_dir) / SSH_DIR_NAME
    path = directory / AUTHORIZED_KEYS_NAME

    if any(existing.data == key.data for existing in read_keys(username)):
        raise SshKeyError("That key is already in the file.")

    try:
        directory.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as keys_file:
            keys_file.write(key.line + "\n")

        for item, mode in ((directory, SSH_DIR_MODE), (path, AUTHORIZED_KEYS_MODE)):
            item.chmod(mode)
            os.chown(item, account.pw_uid, account.pw_gid)
    except OSError as error:
        raise SshKeyError(f"Could not write {path}: {error}") from error

    return path
