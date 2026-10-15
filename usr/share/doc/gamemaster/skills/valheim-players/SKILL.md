---
name: valheim-players
description: Who is on a Valheim server, bans, admins, permitted players
version: 1.0.0
metadata:
  hermes:
    tags: [valheim, gamemaster]
    category: gameserver
---
# Players on a Valheim server

## When
Somebody asks who is online, or wants a player banned, made an admin, or
let onto a server that only permitted players may join.

## What there is, and what there is not
Valheim has no remote console. GameMaster therefore knows the players from
the log of the server, and sets bans and rights through three list files
the server reads again when they change:

| List | Effect |
|---|---|
| banned | these players cannot join |
| admin | these players may use the admin commands in the game (F5) |
| permitted | once anybody is on it, **only** those on it may join |

There is no command to kick a player or to send a message. An admin in the
game can kick with the console there.

## Player IDs
The lists hold IDs, not names. To find one:

    sudo valheim [-u <user>] player list

shows the players that are online with their ID in brackets, the way the
server writes it into its log: the bare Steam ID, as `76561198000000000`,
or with the platform before it, as `Steam_76561198000000000`. Use it
exactly as shown. For a player who is offline, ask the user for the ID; a
player sees it in the game with F2. Never guess an ID from a name.

If a ban or admin rights with the bare number do not take effect, the
server may want the form with the platform: take the entry off again and
add `Steam_<number>` instead. Tell the user which form worked.

## Steps
Every command runs on the game server machine, as described in your
profile.

- Who is online:

      sudo valheim [-u <user>] player list

  The list comes from the log. A player who just joined appears once the
  character has spawned.

- Show the lists:

      sudo valheim [-u <user>] player lists

- Ban, lift a ban:

      sudo valheim [-u <user>] player ban <id>
      sudo valheim [-u <user>] player unban <id>

  Afterwards run `player list` to see whether a banned player who was
  online has been disconnected, and say so. If not, the ban applies when
  they join next.

- Admin rights:

      sudo valheim [-u <user>] player admin <id>
      sudo valheim [-u <user>] player unadmin <id>

- Permitted players:

      sudo valheim [-u <user>] player permit <id>
      sudo valheim [-u <user>] player unpermit <id>

  Before putting the **first** player on the permitted list, say clearly
  that from then on everybody else is kept out, and wait for a clear yes.

Change the lists only with these commands, not with an editor.

## Rules
- Banning and admin rights are decisions of the user. Carry them out only
  when asked, and name the player and the ID back before you do.
- Player IDs belong to the players. Pass them on only to the person who
  looks after the server, never into a web search.
