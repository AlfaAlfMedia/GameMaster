---
name: valheim-world
description: Create a Valheim world or load another one
version: 1.0.0
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

   An existing world is loaded with `world switch`, a new one is made with
   `world create`. If the name the user gave is close to an existing one,
   ask which is meant before creating a second world.

2. Look at the situation:

       sudo valheim [-u <user>] status

   Tell the user which world is loaded and who is online.

3. Ask for confirmation: the server saves, stops and starts again with
   world `<name>`, and every player is thrown off. Valheim cannot send the
   players a message, so name who is online and let the user decide. Wait
   for a clear yes.

4. Switch, or create:

       sudo valheim [-u <user>] world switch <name>
       sudo valheim [-u <user>] world create <name>

   This saves, stops, changes over and starts. The start can take several
   minutes, because the server is updated first, and a new world is
   generated on its first start. Do not do these steps one by one by hand.

   A new world gets a random seed. There is no way to choose the seed from
   here; if somebody wants a particular seed, that is a job for the
   administrator.

5. Check:

       sudo valheim [-u <user>] status

   Expected: `state: running` and `world: <name>`. Report the result.
   With `state: starting` the server is still loading - wait, do not switch
   or start again.

## When something goes wrong
- If the command ends with `ERROR:`, pass the message on and use the skill
  `valheim-troubleshoot`. Do not start another world on your own.
