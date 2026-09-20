#!/bin/bash

ETC_DIR=/etc/gamemaster
source "$ETC_DIR/gamemaster.conf"
source "$ETC_DIR/zomboid/zomboid.conf"

runuser -u zomboid -- ${PZ_SERVER_INSTALL_DIR}/start-server.sh -servername "$1" -adminpassword "$PZ_SERVER_ADMIN_PASSWORD"