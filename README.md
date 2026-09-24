# GameMaster

Administration tools for game servers on Linux — run by an administrator, or
by an AI agent through a narrow, explicitly granted set of commands.

The first supported game is **Project Zomboid**.

> **Status: in development.** The Debian package builds and installs, but
> nothing has yet run against a real Project Zomboid server.

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command reference](#command-reference)
- [Multiple servers and multiple worlds](#multiple-servers-and-multiple-worlds)
- [Configuration](#configuration)
- [The AI agent](#the-ai-agent)
- [How it works](#how-it-works)
- [Project layout](#project-layout)
- [Roadmap](#roadmap)
- [License](#license)

## Features

- install a Project Zomboid server with SteamCMD, creating its Linux user if
  needed, and register it
- register a server that is already installed, including its ports
- run any number of servers on one machine, one Linux user per server, with
  ports checked against every other registered server
- hold any number of worlds per server, one of them loaded at a time, and
  switch between them in a single command
- create, initialise and list worlds
- start, stop and save a server, message its players, update the server and
  its mods
- list, kick and ban players, and give them permission levels
- read and change the server options of a running world
- give an AI agent exactly these commands over SSH and sudo, and nothing else

## Requirements

- Linux with systemd
- Python 3.10 or newer
- `sudo`
- SteamCMD — only to install servers with `gamemaster install`. On Debian it
  is in the package `steamcmd`, which needs the section `non-free` and the
  architecture `i386`; see the
  [SteamCMD documentation](https://developer.valvesoftware.com/wiki/SteamCMD#Linux).
- one Linux user per game server

## Installation

The repository mirrors the file system it installs into, so the package is
built from it directly:

```
dpkg-buildpackage -us -uc -b
sudo apt install ../gamemaster_*_all.deb
```

Build on a Linux file system, not on a mounted Windows drive: the package
takes the execute bits from the files, and a Windows share does not keep
them.

Installing the package creates the agent user and the directories below
`/etc/gamemaster` and `/var/log/gamemaster`. Removing it leaves everything
alone. Purging it stops the services of the servers, removes them, and takes
away `/etc/gamemaster`, `/var/log/gamemaster` and the agent user — but never
the save games, the installed servers or their Linux users. After a purge the
game servers keep running; they are only no longer managed from here.

## Quick start

Install a server, give it a world and start it:

```
sudo gamemaster install zomboid -u zomboid          # user, install, register
sudo nano /etc/gamemaster/zomboid/zomboid.conf      # change both passwords
sudo zomboid -u zomboid world create bonn           # ini, sandbox, save dir
sudo nano ~zomboid/Zomboid/Server/bonn.ini          # settings, mods
sudo zomboid -u zomboid world init bonn             # one first start, then
                                                    # the service is written
sudo zomboid -u zomboid start
sudo zomboid -u zomboid status
```

The passwords come from the template and have to be changed before the first
world is created — they end up in the database of that world.

Without `-u` the default user from `/etc/gamemaster/gamemaster.conf`
(`PZ_DEFAULT_USER`) is taken, so on a machine with a single server the option
can be left out everywhere.

## Command reference

### `gamemaster` — set the machine up

Run by a human, as root. It creates Linux users, installs servers and manages
the keys of the agent user.

| Command | Effect |
|---|---|
| `gamemaster install zomboid [options]` | install a server with SteamCMD and register it |
| `gamemaster add zomboid [options]` | register a server that is already installed |
| `gamemaster agent [-l\|--list]` | show the keys the agent user may log in with, and add one |

Options of `install zomboid` and `add zomboid`:

| Short | Long | Meaning |
|---|---|---|
| `-u` | `--username USERNAME` | Linux user that runs the server (default: `PZ_DEFAULT_USER`) |
| `-d` | `--installdir DIRECTORY` | directory of the server (default: `PZ_SERVER_INSTALL_DIR` from the template) |
| `-P` | `--port PORT` | udp port the players connect to |
| `-U` | `--udp-port PORT` | second udp port of the server |
| `-R` | `--rcon-port PORT` | port of the remote console |
| `-b` | `--beta BRANCH` | install this beta branch (`install` only; default: `PZ_DEFAULT_BRANCH`) |
| `-h` | `--help` | show the help |

Options of `agent`:

| Short | Long | Meaning |
|---|---|---|
| `-l` | `--list` | only show the keys, do not ask for one |
| `-h` | `--help` | show the help |

A port another registered server already uses is refused. Without the
matching option the program then offers the next free one.

`install zomboid` creates the Linux user if it does not exist, with a home
directory and a group of its own; its password is asked for twice and is
never taken from the command line. SteamCMD runs as that user, never as
root, so the server belongs to the user from the start. If there is a server
in the directory already, the program stops and points to `add zomboid`.

### `zomboid` — run a server

Run as root, by a human or by the agent. Every command takes
`-u|--username USERNAME` to name the server; without it `PZ_DEFAULT_USER` is
used.

| Command | Effect |
|---|---|
| `zomboid status` | is a server running, which world, which players |
| `zomboid start` | start the service |
| `zomboid stop` | save the world and shut the server down |
| `zomboid save` | save the world, keep the server up |
| `zomboid message TEXT` | send a message to every player |
| `zomboid update` | update the server with SteamCMD (server must be stopped) |
| `zomboid update mods [-c\|--check]` | let the server fetch its mods again; `--check` only asks whether an update is waiting |
| `zomboid world list` | the worlds of this server and their state |
| `zomboid world create NAME` | create the ini file, the sandbox file and the save directory |
| `zomboid world init NAME` | first start, then write the service |
| `zomboid world switch NAME` | let the service load another world |
| `zomboid player list` | the players that are connected |
| `zomboid player kick NAME [-r\|--reason TEXT]` | throw a player off the server |
| `zomboid player ban NAME [-r\|--reason TEXT] [--ip]` | ban a player by name, `--ip` also by network address |
| `zomboid player unban NAME` | lift the ban on a name |
| `zomboid player banid STEAMID` / `unbanid STEAMID` | ban and unban a Steam ID |
| `zomboid player banip ADDRESS` / `unbanip ADDRESS` | ban and unban a network address |
| `zomboid player level NAME LEVEL` | permission level: admin, moderator, overseer, gm, observer |
| `zomboid option list` | all server options with their values |
| `zomboid option set NAME VALUE` | change one option while the server runs |
| `zomboid option reload` | read the ini file again |

Every command reports short lines on standard output and returns 0 or 1. On
1 the last line begins with `ERROR:` and says what is wrong.

## Multiple servers and multiple worlds

**Several servers on one machine: one Linux user each.** There is no limit
on how many. Each server is registered under its own user, gets its own
configuration file `/etc/gamemaster/zomboid/<user>.conf` and its own systemd
service `zomboid-<user>.service`. The three ports of a new server are checked
against every server already registered, so the same port cannot be handed
out twice. Every command is addressed to one server with `-u`:

```
sudo gamemaster install zomboid -u zomboid
sudo gamemaster install zomboid -u zomboid2 -d /opt/pzserver2 \
                                -P 16271 -U 16272 -R 27016
sudo zomboid -u zomboid2 status
```

Each user has a full installation of its own, so the servers are updated
one by one and use the disk space of one installation each.

**Several worlds per server: as many as you like, one loaded at a time.**
A server holds any number of worlds; `zomboid world list` shows them and says
which one is loaded. Only one of them runs, because there is one service per
user and the world is named in its `ExecStart` line. `zomboid world switch`
therefore stops the running world, writes the service again and starts the
new one:

```
sudo zomboid -u zomboid world list
sudo zomboid -u zomboid world switch bonn
```

This is the intended design, not a missing feature: Project Zomboid writes
everything below `~/Zomboid`, and the ports belong to the server, not to the
world. **Two worlds that are to run at the same time need two Linux users**,
that is, two servers in the sense above.

## Configuration

`/etc/gamemaster/gamemaster.conf` holds the settings that apply to the whole
machine: the name of the agent user, and per game the default server user,
the Steam application ID and the branch that is installed by default.

`/etc/gamemaster/zomboid/<user>.conf` is written by `gamemaster add zomboid`
or `gamemaster install zomboid`. It holds the passwords, the three ports, the
install directory and the Steam branch of one server. It is only read by the
GameMaster programs, which run as root, so it has permissions `0600` and
belongs to `root`.

The settings file of a world gets the RCON password, so it has permissions
`0660` and belongs to the server user and its group.

## The AI agent

`usr/share/doc/gamemaster/SOUL.md` is the profile of the agent: a template an
administrator fills in, saying what the agent may do and what it may not.

What the sudoers file enforces is the machine: the agent may run one
program, and nothing else. No packages, no users, no services, no files
outside the servers it looks after. That boundary is real and does not depend
on the agent behaving. The agent user is a member of the group of every
registered server user, so it can read that server's files and logs.

Inside the game there is no such boundary, and there cannot be one. The agent
is allowed to read the ini file of a world, because that is where the
settings and the mod list live — and that file also holds the RCON password.
Anyone who can read it can talk to the server themselves and use every
command it has, not only the ones this program offers. The choice is
therefore between an agent that can edit settings and mods, and one that is
held to a subset of the RCON commands. GameMaster takes the first: within the
game the agent is a full administrator, and only SOUL.md tells it what to
leave alone.

`gamemaster agent` shows which keys may log in as the agent user, with their
fingerprints, and adds one.

## How it works

### Creating a world

A world is created in three steps, and the middle one belongs to a person.

```
zomboid world create NAME     the ini file, the sandbox file, the save directory
                              -- edit those two: settings, mods --
zomboid world init NAME       the server runs once, then it is ready
zomboid start                 from now on it runs as a service
```

Only three things have to exist before a world can start: the ini file, the
sandbox file and the directory below `Saves/Multiplayer`. Everything else is
created by the server itself on its first start. That first start is also the
only reason it exists: the admin password is handed over on the command line
there, so that it reaches the database of the world, and the settings are
read in. Once the server answers over RCON the world is known to be sound; it
is stopped again and its systemd service is written.

### Running a server

A server runs as the systemd service `zomboid-<user>.service`. The world is
named in the `ExecStart` line, and that line is the only place where the
world of a running server is written down. `zomboid status` reads it back
from the command line of the running process, which is why it also
recognises a server that was set up by hand.

Before the server starts, the service updates it: `ExecStartPre` calls
`zomboid update`. It runs as root, because the settings of a server may only
be read by root, and a failed update does not keep the server from starting.
SteamCMD can take a while, so the service allows half an hour for its start.

`zomboid world init` is the only place in the whole program where a server is
started by hand. Everything after that goes through systemd.

`zomboid stop` does not kill the process: it saves the world over RCON, asks
the server to quit, and waits until it is gone.

### Structure of the code

The programs in `usr/sbin` are thin. They read the command line, fetch their
settings and call the library; everything that more than one of them needs
lives in the package under `usr/lib`.

The library follows one rule: the general knows nothing about the specific.
`validate.py` does not know about files, `configfile.py` does not know about
Project Zomboid, and `rcon.py` only speaks the protocol — the commands of a
particular game live with that game. A second game is added as its own module
beside `zomboid.py`.

Values that reach a program from outside — the command line, a configuration
file, later an agent — are checked in one place. Each check returns the
cleaned value or raises, so a program never works with something unchecked.

The programs report what they are doing in short lines on standard output, so
that an agent can follow along, and return 0 or 1 to say whether it worked.
The much noisier output of the game server itself goes into a log file.

## Project layout

```
etc/
  gamemaster/
    gamemaster.conf             general settings, default user, agent user
    zomboid/<user>.conf         one file per registered server
  sudoers.d/gamemaster          what the agent user is allowed to run
usr/
  sbin/
    gamemaster                  administration tool, run by a human only:
                                install and register servers, keys of the
                                agent user
    zomboid                     run a server: status, start, stop, save,
                                message, update, worlds, players, options
  share/gamemaster/zomboid/
    template.conf               template for a server configuration
    template.ini                template for a world
    template_SandboxVars.lua    template for the sandbox settings
    template.service            template for the systemd service
  share/doc/gamemaster/
    SOUL.md                     the profile of the agent, what it may
                                do and what it may not
  lib/python3/dist-packages/gamemaster/
    errors.py                   the error all programs report
    validate.py                 checks for values that come from outside
    configfile.py               reading and changing KEY=VALUE files
    context.py                  what every program needs before it starts:
                                root, settings, templates, error handling
    process.py                  the running processes of a Linux user
    service.py                  writing and controlling a systemd service
    steamcmd.py                 installing and updating with SteamCMD
    sshkey.py                   public keys and authorized_keys
    rcon.py                     the Source RCON protocol
    zomboid.py                  worlds and commands of a Zomboid server
```

## Roadmap

- manual pages for `gamemaster` and `zomboid`
- more games

## License

GPL-3.0-or-later, see [LICENSE](LICENSE).

Source: <https://git.alfaalf-media.de/alfaalf-media/gamemaster>
