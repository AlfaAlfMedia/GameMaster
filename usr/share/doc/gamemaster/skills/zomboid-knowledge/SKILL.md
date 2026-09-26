---
name: zomboid-knowledge
description: Zomboid facts on power, water and network
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster]
    category: gameserver
---
# Background knowledge about a Zomboid server

## When
Questions about power and water in the world, about the address of the
server, or when a setting and what players see in the game do not match.

## Power and water
- `<world>_SandboxVars.lua` holds the settings for the automatic shutoff:
  `ElecShut`, `WaterShut`. The value `9` means "disabled".
- That is the setting, not the state of the world. A running world keeps
  its state in the save. If the power was already cut there - by time or by
  an admin tool - it stays off, even with `ElecShut = 9` in the file.
- `ElecShut` is mostly the choice made when the world was created;
  `ElecShutModifier` sets the day of the shutoff. A known but not
  guaranteed way out: with the server stopped, set `ElecShutModifier` to a
  far away value like `9999` and restart. Offer it as an attempt, not as a
  sure fix. The same goes for water with `WaterShutModifier`.
- To check in the game: admin menu, World → Water and Electricity, and if
  available Debug → Sandbox Settings.
- Mention a mod like "Water and Power Controls" only if it is listed in
  `WorkshopItems=`.
- Save files are binary. Never edit them as text. Guides that name
  `map_sand.bin` come from older versions or from single player; in
  Build 42 multiplayer the state is spread over many files (`map_meta.bin`,
  `map_worldgen.bin`, `map_zone.bin`, `entity_data.bin`, `vehicles.db`,
  `players.db`, `zpop/`, ...). Do not call any single file "the power
  file".

## Network and addresses
- `sudo zomboid status` shows no public address.
- The logs mostly hold addresses of players, not of the server.
- Private addresses (10.x.x.x, 172.16-31.x.x, 192.168.x.x) are never the
  public address of the server.
- The address you reach the machine by over SSH may be an internal
  management address, not the public one.
- An empty `server_browser_announced_ip=` in the ini means the server
  announces no fixed address. That is not an error.
- If the public address is neither in the ini nor in the log, say so.
  Never guess.
- The ports are in the ini: `DefaultPort=`, `UDPPort=`. `RCONPort=` is for
  administration only, not for players.

## What "running" means
- `sudo zomboid status` with `state: playable` is what counts: the server
  answers over RCON.
- Right after a start, other tools may still report the server as offline
  while it is loading. Wait and ask again, do not restart.
- A reported setting such as the electricity shutoff describes the
  configuration, not the actual state of the world (see above).

## Sources for further research
- https://pzwiki.net/wiki/Server_Settings
- https://pzwiki.net/wiki/Debug_mode

Guides on the web depend on the version. Do not carry Build 41 or single
player guides over to Build 42 multiplayer without checking.
