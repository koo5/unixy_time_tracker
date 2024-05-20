#!/usr/bin/env fish
set DIR /data/sync/jj/backup/hours/(date --iso)
mkdir -p $DIR
sudo -u postgres pg_dump -d hours > $DIR/dump
