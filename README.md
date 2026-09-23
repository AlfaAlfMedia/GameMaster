# GameMaster

Administration tools for game servers on Linux — run by an administrator, or
by an AI agent over a narrow, explicitly granted set of commands.

The first supported game is **Project Zomboid**.

> **Status: in development.** The Debian package builds and installs, but
> nothing has yet run against a real Project Zomboid server.

## What it does

GameMaster manages game servers. It can install a server itself, or take
over one that is already installed.

For Project Zomboid it can currently:

- install a server with SteamCMD, creating its Linux user if needed, and
  register it (`gamemaster install zomboid`)
- register an existing server, including its ports (`gamemaster add zomboid`)
- show which keys the agent user may log in with, and add one
  (`gamemaster agent`)
- create the files of a new world (`zomboid world create`)
- let a server create a world once, stop it again and write its systemd
  service (`zomboid world init`)
- list the worlds of a server and their state (`zomboid world list`)
- let the service load another world (`zomboid world switch`)
- say whether a server is running and which world it has loaded
  (`zomboid status`)
- start and stop a server, save its world, message its players, list and
  kick or ban them, read and change the server options (`zomboid`)
- update the server and its mods (`zomboid update`)

## Idea

Every server belongs to its own Linux user. That user owns the installation,
the worlds and the save games. GameMaster keeps one configuration file per
server user below `/etc/gamemaster/` and derives everything else from it.

A separate user — by default `gamemaster` — is the one an AI agent connects
as over SSH. That user may run exactly the programs listed in
`/etc/sudoers.d/gamemaster`, and nothing else. It is a member of the group of
every registered server user, so it can read that server's files and logs
without being able to touch anything else on the machine.

The programs report what they are doing in short lines on standard output, so
that an agent can follow along, and return 0 or 1 to say whether it worked.
The much noisier output of the game server itself goes into a log file.

## Layout

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
    SOUL.md                     the profile of the agent (German), what
                                it may do and what it may not
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

## Structure

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

## Creating a world

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

## Running a server

A server runs as the systemd service `zomboid-<user>.service`. There is one
service per user, because a user has one server and that server has one
world — Project Zomboid writes everything below `~/Zomboid`.

The world is named in the `ExecStart` line of the service, and that line is
the only place where the world of a running server is written down.
`zomboid status` reads it back from the command line of the running process,
which is why it also recognises a server that was set up by hand.
`zomboid world switch` writes the service again and reloads it.

`zomboid world init` is the only place in the whole program where a server is
started by hand. Everything after that goes through systemd.

`zomboid stop` does not kill the process: it saves the world over RCON, asks
the server to quit, and waits until it is gone.

## The agent

`usr/share/doc/gamemaster/SOUL.md` describes what the agent may do, in the
form of a profile for it. It is the counterpart of the sudoers file: the
sudoers file enforces the boundary, SOUL.md explains it.

`gamemaster agent` shows which keys may log in as the agent user, with their
fingerprints, and adds one.

## Configuration

`/etc/gamemaster/gamemaster.conf` holds the settings that apply to the whole
machine: the name of the agent user, and per game the default server user,
the Steam application ID and the branch that is installed by default.

`/etc/gamemaster/zomboid/<user>.conf` is written by `gamemaster add zomboid`
or `gamemaster install zomboid` and holds the passwords, the three ports, the
install directory and the Steam branch of one server. Ports are compared
against every other registered server, so the same port cannot be handed out
twice. The passwords are taken from the template and have to be changed
before the first world is created.

## Installing a server

```
gamemaster install zomboid [-u USERNAME] [-d DIRECTORY]
                           [--port PORT] [--udp-port PORT] [--rcon-port PORT]
                           [--beta BRANCH]
```

- If the Linux user does not exist, it is created with a home directory and a
  group of its own. Its password is asked for twice; it is never taken from
  the command line.
- SteamCMD runs as that user, never as root, so the server belongs to the user
  from the start and can later be updated by it.
- Without `--beta` the stable branch is installed.
- If there is a server in the directory already, the program stops and points
  to `gamemaster add zomboid`.

SteamCMD is not installed by GameMaster. On Debian it is in the package
`steamcmd`, which needs the section `non-free` and the architecture `i386`;
see the [SteamCMD documentation](https://developer.valvesoftware.com/wiki/SteamCMD#Linux).

`<user>.conf` holds both passwords and is only read by the GameMaster
programs, which run as root, so it is created with permissions `0600` and
belongs to `root`.

The world's own settings file gets the RCON password, so it is created with
permissions `0660` and belongs to the server user and its group.

## Building the package

The repository mirrors the file system it installs into, so the package is
built from it directly:

```
dpkg-buildpackage -us -uc -b
```

Build on a Linux file system, not on a mounted Windows drive: the package
takes the execute bits from the files, and a Windows share does not keep
them.

Installing it creates the agent user and the directories below
`/etc/gamemaster` and `/var/log/gamemaster`. Removing it leaves everything
alone. Purging it stops the services of the servers, removes them, and takes
away `/etc/gamemaster`, `/var/log/gamemaster` and the agent user — but never
the save games, the installed servers or their Linux users. After a purge the
game servers keep running; they are only no longer managed from here.

## Not there yet

- manual pages for `gamemaster` and `zomboid`
- more games

## Requirements

- Linux with systemd
- Python 3.10 or newer
- `sudo`, for the agent user
- SteamCMD, to install servers with `gamemaster install`
- one Linux user per game server
