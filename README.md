# GameMaster

Administration tools for game servers on Linux — run by an administrator, or
by an AI agent over a narrow, explicitly granted set of commands.

The first supported game is **Project Zomboid**.

> **Status: in development.** There is no package yet and no installation
> procedure. The layout of this repository already mirrors the file system,
> so that a Debian package can be built from it later.

## What it does

GameMaster manages game servers that are **already installed**. It does not
install games, and it does not create Linux users.

For Project Zomboid it can currently:

- register an existing server, including its ports (`gamemaster add zomboid`)
- create the files of a new world (`zomboid_create_world_files`)
- list the worlds of a server and their state (`zomboid_list_worlds`)
- let a server create a world once and stop it again
  (`zomboid_initialise_world`)
- talk to a running server over RCON (library)

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
    gamemaster                  administration tool, run by a human only
    zomboid_create_world_files  create the files of a new world
    zomboid_initialise_world    let the server create the world once
    zomboid_list_worlds         list worlds and their state
  share/gamemaster/zomboid/
    template.conf               template for a server configuration
    template.ini                template for a world
    template_SandboxVars.lua    template for the sandbox settings
  lib/python3/dist-packages/gamemaster/
    errors.py                   the error all programs report
    validate.py                 checks for values that come from outside
    configfile.py               reading and changing KEY=VALUE files
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

## Configuration

`/etc/gamemaster/gamemaster.conf` holds the settings that apply to the whole
machine: the default server user and the name of the agent user.

`/etc/gamemaster/zomboid/<user>.conf` is written by `gamemaster add zomboid`
and holds the passwords, the three ports and the install directory of one
server. Ports are compared against every other registered server, so the same
port cannot be handed out twice.

The world's own settings file gets the RCON password, so it is created with
permissions `0660` and belongs to the server user and its group.

## Not there yet

- Debian package (`debian/`), and with it an installation procedure
- one systemd service per world
- starting, stopping and status of a running server
- a program that exposes the RCON commands on the command line
- more games

## Requirements

- Linux with systemd
- Python 3.10 or newer
- one Linux user per game server, with the server already installed
