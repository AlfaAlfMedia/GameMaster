---
name: zomboid-restore
description: Put a backup of a Zomboid world back
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster, backup]
    category: gameserver
---
# Put a backup of a world back

## When
Somebody wants a world set back to an earlier state, e.g. after a bug, lost
data or a quarrel on the server.

## Principles
- The current state is **never deleted**, only renamed. That way there is
  always a way back.
- Only with explicit consent, with the world and the backup named.
- Everything played after the backup is gone afterwards. Say so plainly.

## Where backups come from
- The server makes its own, below `~<user>/Zomboid/backups/` (at every
  start and every version change, controlled by `BackupsCount`,
  `BackupsOnStart`, `BackupsOnVersionChange`, `BackupsPeriod` in the ini
  file). You may read them.
- If the backup is somewhere else, ask the user for the path. It has to be
  readable for you.

## Steps
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user; leave out `-u <user>` for the default
server.

1. Find the backups and show them to the user with their dates:

       ls -lR ~<user>/Zomboid/backups | head -50

2. Look at the chosen backup before doing anything. For a zip file:

       python3 -m zipfile -l <backup.zip> | head -40

   Look for the folder of the world, usually `Saves/Multiplayer/<world>/`
   or `<world>/`. Some archives have no entry for the folder itself, only
   for the files in it - that is a complete state as well. A backup without
   any files of the world is no use. If you cannot find the folder
   unambiguously, stop and ask.

   Note the number of files of the world in the archive.

   If the backup also holds `db/<world>.db` (accounts and passwords), you
   cannot put that part back - you have no access to `db/`. Tell the user
   an administrator has to do it, if it is needed.

3. Ask for confirmation: world, backup with its date, what will be lost,
   that the server is stopped for it. Wait for a clear yes.

4. If the server is running this world: warn the players, then stop it.

       sudo zomboid [-u <user>] message "The server is stopped to restore a backup."
       sudo zomboid [-u <user>] stop

5. Unpack the backup into a folder of its own below /tmp:

       mkdir /tmp/restore-<world>
       python3 -m zipfile -e <backup.zip> /tmp/restore-<world>

6. Put the current state aside, do not delete it:

       mv ~<user>/Zomboid/Saves/Multiplayer/<world> \
          ~<user>/Zomboid/Saves/Multiplayer/<world>.before-restore-<date>

7. Copy the folder of the world from the backup into its place:

       cp -r /tmp/restore-<world>/<path-to-world> ~<user>/Zomboid/Saves/Multiplayer/<world>

   Check that the number of files matches:

       find ~<user>/Zomboid/Saves/Multiplayer/<world> -type f | wc -l

8. Give the files back to the server user. Without this step the world
   starts with errors like "WorldDictionary error", because the server
   cannot write its files:

       sudo zomboid [-u <user>] fix-permissions

9. Clean up and start:

       rm -r /tmp/restore-<world>
       sudo zomboid [-u <user>] start
       sudo zomboid [-u <user>] status

10. The restore has worked only when `status` shows `state: playable` and
    the log of the start has the line `*** SERVER STARTED ****`. Report
    each stage on its own: backup chosen, old state put aside, files put
    back, world loaded - and where the old state is
    (`<world>.before-restore-<date>`). You do not delete the old state;
    that is for a human to decide.

## When something goes wrong
- The server does not start: skill `zomboid-troubleshoot`.
- Back to the state before the restore: stop the server, rename the
  restored folder to `<world>.restore-failed`, rename
  `<world>.before-restore-<date>` back to `<world>`, run
  `sudo zomboid fix-permissions`, start.
