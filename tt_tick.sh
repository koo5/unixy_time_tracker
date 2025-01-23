#!/bin/fish

set DIR (dirname (readlink -m (status --current-filename))); cd "$DIR"

./tt is_on && ./tt tick && ./notify.sh -t 3000 "tt tick" (date) 2>&1 | logger -t tt

