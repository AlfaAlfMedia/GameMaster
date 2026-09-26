---
name: zomboid-new-world
description: Create and initialise a new Zomboid world
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster]
    category: gameserver
---
# Create a new world

## When
Somebody wants a new world on a Project Zomboid server.

## Clarify first
- The name of the world: letters, digits, `_` and `-`, at most 32
  characters. Spaces become `_`.
- The wanted server settings: e.g. name in the server browser, password,
  maximum number of players, PvP, mods.
- The wanted sandbox settings: e.g. number of zombies, their speed, loot,
  length of a day.

Ask for what is missing. Whatever the user leaves open stays at the default
of the template - say so.

## Steps
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user; leave out `-u <user>` for the default
server. The files of the server are below `~<user>/Zomboid/`.

1. Check that the world does not exist yet:

       sudo zomboid [-u <user>] world list

2. Create its files:

       sudo zomboid [-u <user>] world create <name>

   This creates:
   - `~<user>/Zomboid/Server/<name>.ini` - server settings
   - `~<user>/Zomboid/Server/<name>_SandboxVars.lua` - rules of the game
   - `~<user>/Zomboid/Saves/Multiplayer/<name>/` - the save

   Ports and RCON password are filled in already. Do not change them.

3. Enter the settings:
   - Read both files first.
   - Change only the lines that matter. Write the file back in place, e.g.
     with `python3`, so it keeps belonging to the server user.
   - ini file: one setting per line, `Name=Value`, e.g. `PublicName=`,
     `Password=`, `MaxPlayers=`, `PVP=`, `Public=`.
   - SandboxVars file: Lua, e.g. `Zombies = 4,`. The comment above each line
     names the allowed values - keep to them, and leave commas and braces
     where they are.
   - Mods: skill `zomboid-mods`, section "Enter", but without the restart.
   - Show the user a short list of what you changed. Never include
     passwords.

4. Only if the server is running another world: it has to be stopped for
   the first start. That throws players off - ask and warn first, as your
   profile says, then:

       sudo zomboid [-u <user>] stop

5. First start:

       sudo zomboid [-u <user>] world init <name>

   The server starts once, takes over the admin password and the settings,
   creates the remaining files and is stopped again. That takes a few
   minutes, longer with mods. Afterwards the service is set to this world.

6. Start it, if the user wants to:

       sudo zomboid [-u <user>] start
       sudo zomboid [-u <user>] status

   If another world was running before, the service loads the new one from
   now on. Back to the old world with the skill `zomboid-world-switch`.

## When something goes wrong
- `world init` ends with `ERROR:` and "See the log file": the log is named
  in the output (`log file: ...`). Use the skill `zomboid-troubleshoot`.
- After fixing the files, run `sudo zomboid world init <name>` again - as
  long as `world list` shows the world as "not initialised yet".
