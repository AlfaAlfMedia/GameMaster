---
name: valheim-troubleshoot
description: Find out why a Valheim server misbehaves
version: 1.0.0
metadata:
  hermes:
    tags: [valheim, gamemaster, logs]
    category: gameserver
---
# Troubleshooting

## When
The server does not start or crashes, players cannot get on, a world is
missing, a GameMaster command ends with `ERROR:`.

## Principles
- Read first, then explain. Change nothing before the user has agreed.
- Pass findings on shortened and in your own words, not pages of log.
- Logs hold addresses and player IDs. Never copy anything from a log into
  a web search except the error message itself.

## Where things are
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user.

| What | Where |
|---|---|
| state of the server | `sudo valheim [-u <user>] status` |
| state of the service | `systemctl status valheim-<user> --no-pager` |
| output of the service: permissions, update, server | `/var/log/gamemaster/valheim/<user>/<world>.log` |
| worlds and lists | `~<user>/.config/unity3d/IronGate/Valheim/` |

Every start of the server adds to the same log file. A new start begins
with the line `[UnityMemory] Configuration Parameters`; what came before
belongs to earlier starts. The server can be joined once the line
`Game server connected` follows.

## Steps
1. `status`: is it `not running`, `starting` or `running`?
2. Read the end of the log of the world from `status` (or `service world`):

       tail -n 200 /var/log/gamemaster/valheim/<user>/<world>.log

3. Look for the usual causes:
   - the update before the start failed: lines of SteamCMD with `Error`
     or `Failed`. The server then starts with the old version, which
     players with a newer game cannot join
   - `DllNotFoundException` for `libParty.so`, or other lines about
     PlayFab: crossplay cannot work on this machine. Without crossplay
     the server still runs
   - the server stops right after `Load world`: the world files may be
     damaged. Do not delete anything; say so and offer to look at the
     backups (see below)
   - players cannot connect, but the server is `running`: ports or
     firewall. That is a job for the administrator; say which port is set
     (the `-port` value in `systemctl cat valheim-<user>`; the server uses
     it and the next one)
4. Report what you found and what you suggest. Wait for a yes before you
   change anything.

## Backups of a world
The server keeps automatic backups beside the world in `worlds_local/`;
their names contain `_backup_`. Putting one back is done with the server
stopped, and only after the user agreed. Copy the current world to `/tmp`
first, never overwrite it without a copy, and run
`sudo valheim fix-permissions` afterwards.
