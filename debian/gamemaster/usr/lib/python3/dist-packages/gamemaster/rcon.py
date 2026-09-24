"""Talking to a game server over Source RCON.

Every message is a small header followed by the text of the command. A
connection is opened, the password is sent once, and after that commands
can be sent until the connection is closed.

Only the protocol lives here. The commands a particular game understands
belong to that game, for example in gamemaster.zomboid.
"""

import socket
import struct

from gamemaster.errors import GameMasterError

DEFAULT_HOST = "127.0.0.1"
DEFAULT_TIMEOUT = 5.0

# Time to wait for further parts of a long answer once the first part is there
CONTINUATION_TIMEOUT = 0.5

MAX_PACKET_SIZE = 4 * 1024 * 1024

TYPE_COMMAND = 2
TYPE_LOGIN = 3
TYPE_LOGIN_ANSWER = 2

LOGIN_ID = 0x5A17
COMMAND_ID = 0x5A18

# A quote would end an argument early, a line break would start a new command
FORBIDDEN_IN_ARGUMENT = ('"', "\n", "\r", "\x00")


class RconError(GameMasterError):
    """Talking to the server over RCON failed."""


def quoted(value: str) -> str:
    """Return the value in quotes, or raise RconError if that is not safe."""
    for character in FORBIDDEN_IN_ARGUMENT:
        if character in value:
            raise RconError(
                f"{value!r} must not contain quotes, line breaks or null bytes."
            )
    return f'"{value}"'


class Rcon:
    """An open connection to the RCON interface of one server.

    Meant to be used in a with-block, which closes the connection again:

        with Rcon(password, port) as connection:
            print(connection.command("players"))
    """

    def __init__(
        self,
        password: str,
        port: int,
        host: str = DEFAULT_HOST,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not password:
            raise RconError("No RCON password given.")
        if not 1 <= port <= 65535:
            raise RconError(f"{port} is not a valid port number.")

        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: socket.socket | None = None

    # -- opening and closing ------------------------------------------------

    def __enter__(self) -> "Rcon":
        self.open()
        return self

    def __exit__(self, *_details: object) -> None:
        self.close()

    def open(self) -> None:
        """Connect to the server and send the password."""
        try:
            self.socket = socket.create_connection(
                (self.host, self.port), timeout=self.timeout
            )
        except OSError as error:
            raise RconError(
                f"No RCON connection to {self.host}:{self.port}: {error}"
            ) from error

        self.socket.settimeout(self.timeout)
        self._login()

    def close(self) -> None:
        """Close the connection, if there is one."""
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    # -- the protocol -------------------------------------------------------

    def _login(self) -> None:
        """Send the password and check that the server accepted it."""
        self._send(LOGIN_ID, TYPE_LOGIN, self.password)

        for _ in range(3):
            answer_id, answer_type, _ = self._receive()
            if answer_type != TYPE_LOGIN_ANSWER:
                continue
            # The server answers a wrong password with the id -1
            if answer_id == -1:
                raise RconError("The RCON password was refused.")
            if answer_id != LOGIN_ID:
                raise RconError("Unexpected answer to the RCON password.")
            return

        raise RconError("The server did not confirm the RCON password.")

    def _send(self, message_id: int, message_type: int, body: str) -> None:
        """Put one message on the wire."""
        payload = struct.pack("<ii", message_id, message_type)
        payload += body.encode("utf-8") + b"\x00\x00"

        try:
            self.socket.sendall(struct.pack("<i", len(payload)) + payload)
        except OSError as error:
            raise RconError(f"Could not send to the server: {error}") from error

    def _receive_exactly(self, length: int) -> bytes:
        """Read exactly this many bytes, however they arrive."""
        parts: list[bytes] = []
        missing = length

        while missing:
            try:
                part = self.socket.recv(missing)
            except OSError as error:
                raise RconError(f"Could not read from the server: {error}") from error
            if not part:
                raise RconError("The server closed the RCON connection.")
            parts.append(part)
            missing -= len(part)

        return b"".join(parts)

    def _receive(self) -> tuple[int, int, str]:
        """Read one message and return its id, its type and its text."""
        (length,) = struct.unpack("<i", self._receive_exactly(4))
        if not 10 <= length <= MAX_PACKET_SIZE:
            raise RconError(f"The server announced an impossible length: {length}")

        payload = self._receive_exactly(length)
        message_id, message_type = struct.unpack("<ii", payload[:8])
        return message_id, message_type, payload[8:-2].decode("utf-8", "replace")

    def command(self, text: str) -> str:
        """Send one command and return the answer of the server.

        A long answer arrives in several parts. The first part is waited for
        with the normal timeout, further parts only briefly - once nothing
        follows any more, the answer is complete.
        """
        if self.socket is None:
            raise RconError("The RCON connection is not open.")

        self._send(COMMAND_ID, TYPE_COMMAND, text)

        _, _, answer = self._receive()
        parts = [answer]

        self.socket.settimeout(CONTINUATION_TIMEOUT)
        try:
            while True:
                _, _, more = self._receive()
                parts.append(more)
        except (RconError, OSError):
            pass
        finally:
            self.socket.settimeout(self.timeout)

        return "".join(parts)
