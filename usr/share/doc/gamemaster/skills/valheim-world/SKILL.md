---
name: valheim-world
description: Create a Valheim world or load another one
version: 1.1.0
metadata:
  hermes:
    tags: [valheim, gamemaster]
    category: gameserver
---
# Create or switch a world

## When
Somebody wants a Valheim server to load another world, or to start a new
one.

## Steps
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user; leave out `-u <user>` for the default
server.

1. List the worlds:

       sudo valheim [-u <user>] world list

   A world under "playable" has been played and can be switched to. A
   world under "created, not started yet" has rules but Valheim has not
   made it yet. If the name the user gave is close to an existing one, ask
   which is meant before creating a second world.

2. Look at the situation:

       sudo valheim [-u <user>] status

   Tell the user which world is loaded and who is online.

3. Ask for confirmation: the server saves, stops and starts again with
   world `<name>`, and every player is thrown off. Valheim cannot send the
   players a message, so name who is online and let the user decide. Wait
   for a clear yes.

4. **A world that is "playable":** switch to it.

       sudo valheim [-u <user>] world switch <name>

   This saves, stops, changes over and starts. Do not do these steps one
   by one by hand.

   **A new world:** the same steps as for Project Zomboid.

       sudo valheim [-u <user>] world create <name>

   This writes the rules of the world to
   `~<user>/.config/unity3d/IronGate/Valheim/gamemaster/<name>.conf`. Ask
   the user which rules they want - difficulty (`VH_PRESET`), combat,
   death penalty, resources, raids, portals, no build cost, no map - and
   set them in that file; every rule is explained there, with the values
   it takes. Leave a rule empty for the default of Valheim. Then:

       sudo valheim [-u <user>] stop
       sudo valheim [-u <user>] world init <name>
       sudo valheim [-u <user>] start

   `world init` refuses while a server runs; that is why it is stopped
   first. Valheim makes the new world during that start. A new world gets
   a random seed; there is no way to choose it from here.

   The start can take several minutes, because the server is updated
   first.

5. Check:

       sudo valheim [-u <user>] status

   Expected: `state: running` and `world: <name>`. Report the result.
   With `state: starting` the server is still loading - wait, do not switch
   or start again.

## Changing the rules of a world
Change its file in `~<user>/.config/unity3d/IronGate/Valheim/gamemaster/`,
then, after the user agreed, `sudo valheim service` and a restart with
`stop` and `start`. The new rules apply from that start. A world that has
no such file keeps the rules it was made with; do not create one for it
without asking.

## When something goes wrong
- If the command ends with `ERROR:`, pass the message on and use the skill
  `valheim-troubleshoot`. Do not start another world on your own.
