---
name: zomboid-world-switch
description: Load another world on a Zomboid server
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster]
    category: gameserver
---
# Switch the world

## When
Somebody wants a Project Zomboid server to load another world.

## Steps
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user; leave out `-u <user>` for the default
server.

1. List the worlds:

       sudo zomboid [-u <user>] world list

   Only a world under "playable" can be switched to. A world under
   "created, not initialised yet" has to be initialised first (skill
   `zomboid-new-world`, from step 4). If the world does not exist at all,
   say so and ask whether a new one should be created.

2. Look at the situation:

       sudo zomboid [-u <user>] status

   Tell the user which world is loaded and who is online.

3. Ask for confirmation: the server is stopped and started again with world
   `<name>`, and every player is thrown off. Wait for a clear yes.

4. If players are online, warn them and give them about a minute:

       sudo zomboid [-u <user>] message "The server switches worlds and restarts in one minute."

5. Switch:

       sudo zomboid [-u <user>] world switch <name>

   This saves, stops, changes over and starts. The start can take several
   minutes, because the server is updated first. Do not do these steps one
   by one by hand.

6. Check:

       sudo zomboid [-u <user>] status

   Expected: `state: playable` and `world: <name>`. Report the result.
   With `state: starting` the server is still loading - wait, do not switch
   or start again.

## When something goes wrong
- If `world switch` ends with `ERROR:`, pass the message on and use the
  skill `zomboid-troubleshoot`. Do not start another world on your own.
