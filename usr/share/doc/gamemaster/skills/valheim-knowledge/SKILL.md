---
name: valheim-knowledge
description: Valheim facts on worlds, saving, network and players
version: 1.0.0
metadata:
  hermes:
    tags: [valheim, gamemaster]
    category: gameserver
---
# Background knowledge about a Valheim server

## When
Questions about saving, about worlds and their files, about the address of
the server, or about how players get on.

## Saving
- The server saves every 30 minutes and when it is stopped. There is no
  command to save in between.
- `sudo valheim stop` lets the server save first. A world is never lost by
  a regular stop or a restart of the machine.

## Worlds
- A world is a directory in `worlds_local/` with the save files in it.
  They are binary; never edit them as text.
- A world is created by the server when it starts with a name it does not
  know yet. That is what `world create` does.
- The world modifiers (combat, resources, raids, portals and so on) are set
  in the game or by the administrator, not by GameMaster.

## Network and addresses
- The server uses its port and the one after it, both udp. The default is
  2456 and 2457.
- With crossplay (`-crossplay` in `systemctl cat valheim-<user>`), players
  from every platform can join and no port has to be forwarded; they join
  by the public address, the join code in the log, or the server list.
- `sudo valheim status` shows no public address. Private addresses
  (10.x.x.x, 172.16-31.x.x, 192.168.x.x) are never the public one. If the
  public address is not known, say so; never guess.

## What "running" means
- `state: running` means the server wrote `Game server connected` after its
  latest start.
- Right after a start, the server list may not show the server for a few
  minutes. Wait and ask again, do not restart.

## Sources for further research
- https://valheim.fandom.com/wiki/Dedicated_servers
- the manual that comes with the server: `Valheim Dedicated Server
  Manual.pdf` in the install directory

Guides on the web depend on the version; check that what you read fits
before you pass it on.
