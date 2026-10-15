# GameMaster

Administration tools for game servers on Linux — run by an administrator, or
by an AI agent through a narrow, explicitly granted set of commands.

Supported games: **Project Zomboid** and **Valheim**.

> **Status: in development.** Project Zomboid runs under GameMaster on a
> live server; Valheim is new in 0.2.0 and has only been tried on a test
> machine.

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command reference](#command-reference)
- [Valheim](#valheim)
- [Multiple servers and multiple worlds](#multiple-servers-and-multiple-worlds)
- [Configuration](#configuration)
- [Permissions](#permissions)
- [The AI agent](#the-ai-agent)
- [How it works](#how-it-works)
- [Project layout](#project-layout)
- [Roadmap](#roadmap)
- [License](#license)

## Features

- install a Project Zomboid or Valheim server with SteamCMD, creating its
  Linux user if needed, and register it
- register a server that is already installed, including its ports
- run any number of servers on one machine, one Linux user per server, with
  ports checked against every other registered server, of either game
- hold any number of worlds per server, one of them loaded at a time, and
  switch between them in a single command
- create, initialise and list worlds
- start, stop and save a server, message its players, update the server and
  its mods (Project Zomboid; Valheim has no remote console, see
  [Valheim](#valheim))
- list, kick and ban players, and give them permission levels
- read and change the server options of a running world (Project Zomboid)
- keep the files of a server usable for the server and the agent, whoever
  touched them last
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
- for Valheim: `libatomic1` and `libpulse0`, which its manual names as the
  libraries the server needs beyond those of SteamCMD

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
the keys of the agent user. `GAME` is `zomboid` or `valheim`.

| Command | Effect |
|---|---|
| `gamemaster install GAME [options]` | install a server with SteamCMD and register it |
| `gamemaster add GAME [options]` | register a server that is already installed |
| `gamemaster agent [-l\|--list]` | show the keys the agent user may log in with, and add one |

Options of `install` and `add`. The settings named are those of Project
Zomboid (`PZ_...`); for Valheim they begin with `VH_` instead:

| Short | Long | Meaning |
|---|---|---|
| `-u` | `--username USERNAME` | Linux user that runs the server (default: `PZ_DEFAULT_USER`) |
| `-d` | `--installdir DIRECTORY` | directory of the server (default: `PZ_SERVER_INSTALL_DIR` from the template; `add` also looks in the home of the user) |
| `-P` | `--port PORT` | udp port the players connect to; Valheim uses the next one as well |
| `-U` | `--udp-port PORT` | second udp port of the server (Zomboid only) |
| `-R` | `--rcon-port PORT` | port of the remote console (Zomboid only) |
| `-b` | `--beta BRANCH` | install this beta branch (`install` only; default: `PZ_DEFAULT_BRANCH`) |
| `-h` | `--help` | show the help |

Options of `agent`:

| Short | Long | Meaning |
|---|---|---|
| `-l` | `--list` | only show the keys, do not ask for one |
| `-h` | `--help` | show the help |

Without `-d`, `add` looks for the server - `start-server.sh` for Project
Zomboid, `valheim_server.x86_64` for Valheim - in the default directory,
then in the home directory of the user and two levels below it.
If it finds exactly one server it takes that one and says so; if it finds
several or none, it asks for `-d`.

A port another registered server already uses is refused, whichever game
it belongs to. Without the matching option the program then offers the
next free one.

`install` creates the Linux user if it does not exist, with a home
directory and a group of its own; its password is asked for twice and is
never taken from the command line. SteamCMD runs as that user, never as
root, so the server belongs to the user from the start. If there is a server
in the directory already, the program stops and points to `add`.

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
| `zomboid fix-permissions` | give every file below `~/Zomboid` back to the server user, with the permissions below |
| `zomboid service` | write the systemd service again from the configuration; applies from the next start |
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

## Valheim

### Quick start

```
sudo gamemaster install valheim -u valheim          # user, install, register
sudo nano /etc/gamemaster/valheim/valheim.conf      # name and password
sudo valheim -u valheim world create Midgard        # the server creates the
                                                    # world and starts
sudo valheim -u valheim status
```

### What is different

Valheim has no remote console, so GameMaster cannot ask the running server
anything or tell it anything. Instead:

- whether the server is up is read from its log: it is running once it has
  written `Game server connected` after its latest start
- who is online is read from the log as well, from the lines the server
  writes when a player connects, spawns and disconnects
- there is no `save`, `message` or `kick`. The server saves every half hour
  and when it gets `SIGINT`, which is how systemd stops it
- bans and rights are set in the three list files of the server, which it
  reads again when they change
- a world needs no first start of its own: the server creates a world when
  it starts with a name it does not know yet

The world, the port and the other settings are given on the command line
of the server, in the `ExecStart` line of `valheim-<user>.service`. The
name and the password of the server go into `/etc/gamemaster/valheim/<user>.env`,
which only root may read, and from there into the command line, so they
are not in the unit file, which everyone may read. While the server runs
they can still be seen in the list of processes: the server takes them in
no other way.

### `valheim` — run a server

Run as root, by a human or by the agent. Every command takes
`-u|--username USERNAME`; without it `VH_DEFAULT_USER` is used.

| Command | Effect |
|---|---|
| `valheim status` | is a server running, which world, which players |
| `valheim start` | start the service and wait until the server can be joined |
| `valheim stop` | let the server save and shut down |
| `valheim update` | update the server with SteamCMD (server must be stopped) |
| `valheim fix-permissions` | give the files of the server back to its user, with the permissions below |
| `valheim service` | write the service again from the configuration; applies from the next start |
| `valheim world list` | the worlds of this server |
| `valheim world create NAME` | point the service at a new world and start it, which creates the world |
| `valheim world switch NAME` | let the service load another world |
| `valheim player list` | the players that are connected, with their IDs |
| `valheim player lists` | the admins, the banned and the permitted players |
| `valheim player ban ID` / `unban ID` | the list of banned players |
| `valheim player admin ID` / `unadmin ID` | the list of admins |
| `valheim player permit ID` / `unpermit ID` | the list of permitted players; once anybody is on it, only they may join |

A player ID is given the way the server writes it into its log, which
`valheim player list` shows: the bare Steam ID, as `76561198000000000`, or
the platform and the ID, as `Steam_76561198000000000`, which is the form
the manual of the server names. Which of the two a server takes in its
lists has not been checked with every version.

### Configuration

`/etc/gamemaster/valheim/<user>.conf` holds the name and the password of
the server, whether it is public, whether it uses crossplay, its port, how
often it saves and keeps backups, and the install directory and Steam
branch. After a change, `valheim service` writes the service again; it
applies from the next start. Commands of your own in the service work as
for Project Zomboid, with `VH_EXEC_START_PRE_1` and so on.

### Permissions

The server keeps its worlds and lists in the default place of the game,
`~/.config/unity3d/IronGate/Valheim`:

| Where | What is there | Group | Files | Directories |
|---|---|---|---|---|
| `worlds_local/` | the worlds and the server's backups of them | read, write | `0660` | `2770` |
| `adminlist.txt`, `bannedlist.txt`, `permittedlist.txt` | the lists | read, write | `0660` | |
| everything else | what the server keeps for itself | read | `0640` | `2750` |

The directories on the way there, `~/.config` and below, are opened to the
group for passing through only (`g+x`), not for listing or writing. They
are kept that way by the same four means as for Project Zomboid.

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

### Commands of your own in the service

The configuration of a server can add commands to its systemd service, for
example to set up firewall rules before the server starts:

```
PZ_EXEC_START_PRE_1=+/etc/gamemaster/hooks/setup-snat.sh $PZ_SERVER_PORT $PZ_UDP_PORT
PZ_EXEC_START_POST_1=/usr/local/bin/notify-started
PZ_EXEC_STOP_POST_1=-+/etc/gamemaster/hooks/remove-snat.sh
```

They become `ExecStartPre`, `ExecStartPost` and `ExecStopPost` lines of the
unit. Numbers from 1 upwards allow more than one of a kind, and set their
order; `ExecStartPre` commands run after GameMaster's own. A leading `+` runs
the command as root, a leading `-` lets the server start even if the command
fails. Settings of the configuration can be passed on as `$NAME`.

A command run as root must belong to root and be writable by root alone,
and so must every directory above it; otherwise the unit is not written.
Whoever may write in one of those directories could put a program of their
own in its place and have it run as root at the next start. Scripts of
this kind belong in `/etc/gamemaster/hooks/`, which the package creates.
Purging the package removes them along with the rest of `/etc/gamemaster`.

The unit is written by `zomboid world init` and `zomboid world switch`.
After changing these settings, `zomboid service` writes it again without
touching the running server; the change applies from its next start.

## Permissions

Everything below `~/Zomboid` belongs to the server user and its group. The
agent user is a member of that group, and what it may do depends on the
part of the directory:

| Where | What is there | Group | Files | Directories |
|---|---|---|---|---|
| `Server/` | settings of the worlds, sandbox and spawn files | read, write | `0660` | `2770` |
| `Saves/` | the worlds | read, write | `0660` | `2770` |
| `mods/` | mods that do not come from Steam | read, write | `0660` | `2770` |
| `db/` | accounts and passwords of the worlds | nothing | `0600` | `0700` |
| everything else | logs, the server's backups, its own files | read | `0640` | `2750` |

`~/Zomboid` itself is `2750`, so nothing new can be put at its top by
anyone but the server. Whatever a later version of the game adds there
counts as "everything else". The home directory of the server user is
opened to its group (`g+rx`), otherwise nothing below it could be reached.

The permissions are kept that way from four sides:

- `zomboid fix-permissions` sets them on the whole directory. The service
  runs it before every start, `zomboid world init` after the first start,
  and `gamemaster add` and `install` when a server is registered. After
  files were copied or put back by hand it can be run at any time.
- the setgid bit on the directories gives everything created inside the
  group of the server, whoever creates it
- the service runs the server with `UMask=0007`, so what it creates can be
  read by its group
- the agent user gets the umask `0007` through `pam_umask`: the package
  writes `umask=0007` into its GECOS field. That covers logins over SSH. An
  agent that runs on the same machine as a service needs `UMask=0007` in
  its own unit instead; it also has to be restarted after a new server was
  registered, because a running process does not see new groups.

`fix-permissions` runs as root in a directory other users may write in, so
it never follows a link: every directory is entered and every file opened
with `O_NOFOLLOW`, and owner and permissions are changed on the open file.
Symbolic links, hard links and special files are left alone and reported,
as is a link like `Logs -> /var/log/zomboid`. If `~/Zomboid` itself is a
link, nothing is changed and the command fails.

## The AI agent

Two things tell an agent how to work with GameMaster. Both are installed
below `/usr/share/doc/gamemaster/` and meant to be copied to the agent:

- `SOUL.md` is the profile of the agent: who it is, how it reaches the
  machine, which commands and files it may use, and what it must not do. It
  is a template; the administrator fills in the parts in angle brackets.
- `skills/` holds the procedures, one folder per task, each with a
  `SKILL.md`:

  | Skill | Task |
  |---|---|
  | `zomboid-world-switch` | load another world, with a warning to the players |
  | `zomboid-new-world` | create a world, enter its settings, first start |
  | `zomboid-mods` | find mods, enter or remove them, check they loaded |
  | `zomboid-restore` | put a backup of a world back without deleting the current state |
  | `zomboid-troubleshoot` | where the logs are, what to look for, common causes |
  | `zomboid-knowledge` | power and water, network addresses, what "running" means |
  | `valheim-world` | create a world or load another one |
  | `valheim-players` | who is online, bans, admins, permitted players |
  | `valheim-troubleshoot` | where the logs are, what to look for, common causes |
  | `valheim-knowledge` | saving, worlds, network, what "running" means |

The profile is read with every message; a skill only when a task needs it.
That keeps the profile short. The skills follow the common `SKILL.md`
format (a name and a description in a YAML header, the procedure below).
For [Hermes Agent](https://hermes-agent.nousresearch.com/) the files go
into the profile of the agent:

```
~/.hermes/profiles/<profile>/SOUL.md
~/.hermes/profiles/<profile>/skills/gameserver/zomboid-*/SKILL.md
~/.hermes/profiles/<profile>/skills/gameserver/valheim-*/SKILL.md
```

Every skill then is also a command of its own in the chat, e.g.
`/zomboid-mods`. Hermes can extend skills by itself from what it learns;
look at them now and then to see that the rules of the profile still
hold.

What the sudoers file enforces is the machine: the agent may run the
programs of the games, `zomboid` and `valheim`, and nothing else. No packages, no users, no services, no files
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

Before the server starts, the service gives its files back to it and
updates it: `ExecStartPre` calls `zomboid fix-permissions`, then `zomboid
update`. Both run as root - the one changes owners, the other reads the
settings of the server, which only root may read - and neither keeps the
server from starting when it fails. SteamCMD can take a while, so the
service allows half an hour for its start.

`zomboid world init` is the only place in the whole program where a server is
started by hand. Everything after that goes through systemd.

`zomboid stop` does not kill the process: it saves the world over RCON, asks
the server to quit, and waits until it is gone.

When systemd stops the service itself - `systemctl stop`, or the machine
shutting down - it sends `SIGINT`, the signal of Ctrl+C in a terminal, on
which the server saves the world and shuts down. It has three minutes for
that before it is killed.

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
    valheim/<user>.conf         the same for Valheim
    valheim/<user>.env          name and password of a Valheim server,
                                for its service, written by GameMaster
    hooks/                      scripts of the administrator that the
                                services run as root
  sudoers.d/gamemaster          what the agent user is allowed to run
usr/
  sbin/
    gamemaster                  administration tool, run by a human only:
                                install and register servers, keys of the
                                agent user
    zomboid                     run a server: status, start, stop, save,
                                message, update, worlds, players, options
    valheim                     run a Valheim server: status, start, stop,
                                update, worlds, players and their lists
  share/gamemaster/zomboid/
    template.conf               template for a server configuration
    template.ini                template for a world
    template_SandboxVars.lua    template for the sandbox settings
    template.service            template for the systemd service
  share/gamemaster/valheim/
    template.conf               template for a server configuration
    template.service            template for the systemd service
  share/doc/gamemaster/
    SOUL.md                     the profile of the agent, what it may
                                do and what it may not
    skills/                     the procedures of the agent, one
                                SKILL.md per task
  lib/python3/dist-packages/gamemaster/
    errors.py                   the error all programs report
    validate.py                 checks for values that come from outside
    configfile.py               reading and changing KEY=VALUE files
    context.py                  what every program needs before it starts:
                                root, settings, templates, error handling
    process.py                  the running processes of a Linux user
    service.py                  writing and controlling a systemd service
    steamcmd.py                 installing and updating with SteamCMD
    permissions.py              handing files to a user without following
                                links
    sshkey.py                   public keys and authorized_keys
    rcon.py                     the Source RCON protocol
    zomboid.py                  worlds and commands of a Zomboid server
    valheim.py                  worlds, log and lists of a Valheim server
tests/                          unit tests, not part of the package
```

The tests need no root:

```
PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
```

## Roadmap

- manual pages for `gamemaster`, `zomboid` and `valheim`
- more games

## Development note

The source code of this project was generated with Claude
under human direction, review and testing.

## License

GPL-3.0-or-later, see [LICENSE](LICENSE).
