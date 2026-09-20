#!/bin/bash
# shellcheck shell=bash

ETC_DIR=/etc/gamemaster
source "$ETC_DIR/gamemaster.conf"

# print the syntax of this script
usage() {
    echo "Usage: $0 [-u|--username USER] \"World name\"" >&2
}

# parse the command line: options (-u/--username) and the world name
# may be given in any order, so everything that is not an option is
# collected in ARGS and checked after the loop
USER_NAME=""
ARGS=()

while [ $# -gt 0 ]; do
    case "$1" in
        -u|--username)
            # the value is the next argument: -u Alf / --username Alf
            if [ -z "${2:-}" ]; then
                echo "Option $1 requires an argument" >&2
                usage
                exit 1
            fi
            USER_NAME="$2"
            shift 2
            ;;
        --username=*)
            # the value is attached with an equals sign: --username=Alf
            USER_NAME="${1#*=}"
            shift
            ;;
        --)
            # end of options: all remaining arguments are taken literally
            shift
            ARGS+=("$@")
            break
            ;;
        -*)
            echo "Unknown option: $1 (world names must not start with a hyphen)" >&2
            usage
            exit 1
            ;;
        *)
            # not an option, so this is the world name
            ARGS+=("$1")
            shift
            ;;
    esac
done

# exactly one argument without option must remain: the world name
if [ ${#ARGS[@]} -ne 1 ]; then
    usage
    exit 1
fi

# store names and replace all spaces with underscores for file names
PZ_PUBLICNAME="${ARGS[0]}"
PZ_WORLD=${PZ_PUBLICNAME// /_}

# check the name against the pattern below: only A-Z, a-z, 0-9, _, - and spaces
# no hyphen or space at the first position, no space at the last position, max 32 characters
PZ_NAME_PATTERN='^[A-Za-z0-9_]([A-Za-z0-9 _-]{0,30}[A-Za-z0-9_-])?$'
if ! [[ $PZ_PUBLICNAME =~ $PZ_NAME_PATTERN ]]; then
    echo "Invalid world name: only letters, digits, space, underscore and hyphen, 1-32 characters, no hyphen or space at the beginning, no space at the end" >&2
    exit 1
fi

# without -u the default user from gamemaster.conf is used
USER_NAME="${USER_NAME:-$PZ_DEFAULT_USER}"

# the user name becomes part of a file path, so it is checked like a Linux user
# name: starts with a lowercase letter or _, then lowercase letters, digits, _ or -
# max 32 characters (same rule as in the gamemaster program)
PZ_USER_PATTERN='^[a-z_][a-z0-9_-]{0,31}$'
if ! [[ $USER_NAME =~ $PZ_USER_PATTERN ]]; then
    echo "Invalid user name: $USER_NAME" >&2
    exit 1
fi

# every user has his own configuration file, created by "gamemaster add zomboid"
PZ_CONF_FILE="$ETC_DIR/zomboid/${USER_NAME}.conf"
if [ ! -f "$PZ_CONF_FILE" ]; then
    echo "No configuration found for user $USER_NAME: $PZ_CONF_FILE" >&2
    exit 1
fi
source "$PZ_CONF_FILE"

# creating filenames with given parameters
PZ_INI_FILE="$PZ_SERVER_DATA_DIR/Server/${PZ_WORLD}.ini"
PZ_SANDBOX_FILE="$PZ_SERVER_DATA_DIR/Server/${PZ_WORLD}_SandboxVars.lua"
PZ_SAVE_DIR="$PZ_SERVER_DATA_DIR/Saves/Multiplayer/$PZ_WORLD"

# checking if the files already exist
if [ -e "$PZ_INI_FILE" ] || [ -e "$PZ_SANDBOX_FILE" ] || [ -e "$PZ_SAVE_DIR" ]; then
    echo "World already exists: $PZ_WORLD" >&2
    exit 1
fi

# copying template files
cp "$SHARE_DIR/zomboid/template.ini" $PZ_INI_FILE
cp "$SHARE_DIR/zomboid/template_SandboxVars.lua" $PZ_SANDBOX_FILE

# create the directory for savegames
mkdir -p $PZ_SAVE_DIR

# set owner and permissions
chown "$PZ_SERVER_USER:$PZ_SERVER_USER" $PZ_INI_FILE && chmod g+rw $PZ_INI_FILE
chown "$PZ_SERVER_USER:$PZ_SERVER_USER" $PZ_SANDBOX_FILE && chmod g+rw $PZ_SANDBOX_FILE
chown "$PZ_SERVER_USER:$PZ_SERVER_USER" $PZ_SAVE_DIR && chmod g+rw $PZ_SAVE_DIR

# set the display name in the ini file
sed -i "s/^PublicName=.*/PublicName=$PZ_PUBLICNAME/" "$PZ_INI_FILE"
