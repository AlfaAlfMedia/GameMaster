---
name: zomboid-mods
description: Add or remove mods on a Zomboid server
version: 1.0.0
metadata:
  hermes:
    tags: [project-zomboid, gamemaster, mods]
    category: gameserver
---
# Add or remove mods

## When
Somebody wants a mod from the Steam Workshop on a Project Zomboid server, or
wants one gone.

## What you need to know
A mod needs up to three entries in the ini file of the world
(`~<user>/Zomboid/Server/<world>.ini`):

| Line | Content | Where from |
|---|---|---|
| `WorkshopItems=` | Workshop ID: digits only | Workshop page, `?id=` in the address |
| `Mods=` | Mod ID: text | Workshop page, line "Mod ID:" |
| `Map=` | map folder, map mods only | Workshop page, line "Map Folder:" |

- Several entries are separated by `;`, without spaces.
- One Workshop item can hold several Mod IDs, often variants or add-ons.
  Ask which ones are wanted instead of taking them all.
- Many mods need other mods ("Required items" on the Workshop page). Those
  need their Workshop ID and Mod ID entered as well.
- Only take mods made for the build the server runs. If the page names only
  an older build, say so.
- The server downloads the mods itself when it starts. You download
  nothing.
- Map mods go in `Map=` before the base map `Muldraugh, KY`.
- Spelling of Mod IDs: some versions of Build 42 put a `\` before every Mod
  ID (e.g. `Mods=\ModA;\ModB`). Always keep the spelling the line already
  has. The script below does that by itself.

## Research
- Wishes like "a crossbow mod" are ambiguous - there are often several
  fitting mods. Never take the first search result; ask for the exact
  Workshop link or ID, or show the candidates to choose from.
- Look up the Workshop page of the mod. Note Workshop ID, Mod ID(s), map
  folder if any, required other mods, and whether it is made for the
  server's build and for multiplayer.
- Watch for notes about old variants: some mods have several Mod IDs of
  which only one is to be enabled.
- Watch for server settings the mod asks for (e.g. `DoLuaChecksum=false`).
  Enter those too and name them in your report.
- Show the user what you found before you enter anything.

## Enter
Every command runs on the game server machine, as described in your
profile. `<user>` is the server user; leave out `-u <user>` for the default
server.

1. Which world? `sudo zomboid [-u <user>] status` shows the loaded one. The
   ini file carries its name.

2. Read the current entries:

       grep -E '^(Mods|WorkshopItems|Map)=' ~<user>/Zomboid/Server/<world>.ini

3. Change the entries. The script below changes exactly one line, saves the
   file as `<world>.ini.bak` first and prints the new line. Entries that are
   there already are not added twice. It is handed to `python3` on the game
   server machine on standard input; the arguments after `python3 -` are:
   ini file, line, `add` or `remove`, then the entries.

   Example - add a Workshop ID, over SSH:

```
ssh <game server> 'python3 - ~<user>/Zomboid/Server/<world>.ini WorkshopItems add <workshop-id>' <<'PY'
import sys
from pathlib import Path

# python3 - <ini file> <key> add|remove <entry> [<entry> ...]
ini, key, action, *entries = sys.argv[1:]
ini = Path(ini)
# newline="" keeps the line endings as they are
with open(ini, encoding="utf-8", newline="") as source:
    text = source.read()
lines = text.splitlines(keepends=True)

for number, line in enumerate(lines):
    if not line.startswith(f"{key}="):
        continue
    content = line.rstrip("\r\n")
    ending = line[len(content):]
    current = [item for item in content[len(key) + 1:].split(";") if item]

    def bare(item):
        return item.lstrip("\\")

    if action == "add":
        # Keep the spelling of the entries already there: with or without \
        prefix = "\\" if key == "Mods" and any(i.startswith("\\") for i in current) else ""
        new = [prefix + bare(e) for e in entries if bare(e) not in map(bare, current)]
        # Map mods come before the base map
        current = new + current if key == "Map" else current + new
    elif action == "remove":
        current = [i for i in current if bare(i) not in map(bare, entries)]
    else:
        sys.exit(f"ERROR: unknown action {action}")

    lines[number] = f"{key}={';'.join(current)}{ending}"
    break
else:
    sys.exit(f"ERROR: no line {key}= in {ini}")

with open(f"{ini}.bak", "w", encoding="utf-8", newline="") as backup:
    backup.write(text)
# Written in place, so the file keeps belonging to the server user
with open(ini, "w", encoding="utf-8", newline="") as target:
    target.write("".join(lines))
print(lines[number].rstrip("\r\n"))
PY
```

   The same for the other lines, each time with the same script:

   - `python3 - <ini> Mods add <mod-id> [<mod-id> ...]`
   - `python3 - <ini> Map add "<map folder>"`
   - `python3 - <ini> Mods remove <mod-id>` - and so on to remove

   When you remove a mod, take out its Workshop ID only if no other mod that
   is still entered comes from the same Workshop item.

4. Server settings the mod asks for (see Research): while the server runs,
   `sudo zomboid [-u <user>] option set <Name> <Value>`. Otherwise change
   the one line `<Name>=<Value>` in the ini in place, with `python3` as
   above.

5. Check: repeat step 2 and show the user the new lines.

## Change the order
To move a mod further forward or back: read the existing `Mods=` line, move
the one entry within it and write the line back. Never put the whole line
together again from memory - entries get lost that way. Afterwards check:
as many entries as before, the moved one exactly once. `WorkshopItems=`
stays as it is.

## Make it take effect
The server loads mods only when it starts. A restart throws every player
off - ask and warn first, as your profile says. Then:

    sudo zomboid [-u <user>] stop
    sudo zomboid [-u <user>] start
    sudo zomboid [-u <user>] status

The start takes longer with new mods, because the server downloads them.

## Check after the start
`state: playable` in `status` only means the server is running. Whether the
mods are loaded is in the log of the server (newest
`~<user>/Zomboid/Logs/*DebugLog-server.txt` or `server-console.txt`).
Search for the Workshop ID and the Mod ID and report the stages separately:

| Log line | means |
|---|---|
| `onItemDownloaded`, `Installed` with the Workshop ID | downloaded |
| `loading <ModID>` | loaded by the server |
| `required mod "<ModID>" not found` | not loaded - wrong Mod ID or missing dependency |
| `skipping non-existent map folder` | wrong `Map=` entry |
| `WARN` lines about the mod after the start | running, but with problems - report it that way |

Mind the time stamps: the log also holds earlier starts. Only lines from
the latest start count.

If something is missing: skill `zomboid-troubleshoot`.

Back to the previous state: `<world>.ini.bak` holds the ini from before the
last change. Write its content back with `cat <world>.ini.bak > <world>.ini`,
not with `mv` or `cp`.

## Update mods
After a mod was updated, players often ask because their game has another
version than the server.

    sudo zomboid [-u <user>] update mods --check

only checks. The answer is in the log of the server (skill
`zomboid-troubleshoot`).

    sudo zomboid [-u <user>] update mods

restarts the server so it fetches the new versions. Ask and warn first.
