#!/bin/bash

echo $USER
id -u

export XDG_RUNTIME_DIR="/run/user/`id -u`"

export DISPLAY=:0
notify-send "$@"

mpv /usr/share/sounds/freedesktop/stereo/audio-volume-change.oga

