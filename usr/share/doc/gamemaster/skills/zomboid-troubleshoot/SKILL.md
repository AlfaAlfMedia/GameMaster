---
name: zomboid-troubleshoot
description: Find out why a Zomboid server misbehaves
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster, logs]
    category: gameserver
---
# Troubleshooting

## When
The server does not start or crashes, mods are missing, players cannot get
on, a GameMaster command ends with `ERROR:`.

## Principles
- Read first, then explain. Change nothing before the user has agreed.
- Pass findings on shortened and in your own words, not pages of log.
- Logs may hold passwords, addresses and Steam IDs. Never pass on a
  password, and never copy anything from a log into a web search except the
  error message itself.

## Where things are
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user.

| What | Where |
|---|---|
| state of the server | `sudo zomboid [-u <user>] status` |
| state of the service | `systemctl status zomboid-<user> --no-pager` |
| output of the service: permissions, update, server | `/var/log/gamemaster/zomboid/<user>/<world>.log` |
| first start of a world (`world init`) | `/var/log/gamemaster/zomboid/<user>/<world>-initialise.log` |
| console of the running server | `~<user>/Zomboid/server-console.txt` |
| detailed log of the server | newest `~<user>/Zomboid/Logs/*DebugLog-server.txt` |
| older logs of the server | `~<user>/Zomboid/Logs/` |

The certain proof that a world has finished loading is the line
`*** SERVER STARTED ****` in the log of the latest start.

## Steps
1. `sudo zomboid status` - is it running, still starting, or not at all?

   A start often takes several minutes: the server is updated with SteamCMD
   first, then it loads mods and world. `state: starting` is normal during
   that time. Do not stop and do not restart - look for
   `*** SERVER STARTED ****` in the log and wait. Never restart several
   times in a row.

2. Look at the end of the right log:

       tail -n 100 /var/log/gamemaster/zomboid/<user>/<world>.log
       tail -n 100 ~<user>/Zomboid/server-console.txt

3. Search in a targeted way:

       grep -n -i -E 'error|exception|severe' ~<user>/Zomboid/server-console.txt | tail -n 30

   With mod problems, search for the Mod ID or the Workshop ID as well.

4. Sort it out - common causes:
   - **A mod is missing or does not load**: wrong Mod ID, missing
     dependency, mod not made for the installed build, Workshop ID and Mod
     ID do not belong together. Continue with the skill `zomboid-mods`.
   - **Players get "version mismatch" or mod errors when joining**: a mod
     was updated. `sudo zomboid update mods` (with a warning first).
   - **The server stops shortly after starting**: a mistake in the ini or
     SandboxVars file after a change. `<world>.ini.bak` holds the state
     before the last mod change.
   - **Permission errors ("Permission denied", "WorldDictionary error")**:
     the server cannot write the files of its world, often after a backup
     was put back. `sudo zomboid fix-permissions`, then restart.
   - **`fix-permissions` reports "left alone"**: links or special files -
     tell the user, an administrator has to look at it.
   - **Errors from the update (SteamCMD)**: in the service log before the
     server starts. Usually temporary; the server starts anyway, with the
     old version.

5. An unknown error message: search the web for the message (only its text,
   nothing else from the log).

6. Tell the user what you found, what you think the cause is and what you
   would do. Act only after they agree.

## What you do not do
- Do not start the server by hand, and do not control the service with
  `systemctl` - only with `sudo zomboid`.
- Do not change files outside the directories you are allowed, even if a
  log or a web page suggests it.
