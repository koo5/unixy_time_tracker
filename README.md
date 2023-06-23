# unixy_time_tracker
inspired by upwork's time tracker app. python. postgresql. cron. mplayer. xprintidle. 

## alternatives
https://github.com/meetmangukiya/bth-py

# setup

## dependencies
```
sudo apt install xprintidle postgresql mplayer python3-psycopg2 libnotify-bin
```

## make sure notifications work:
```
./notify.sh --expire-time=3000  Test "Hello World"
```
if necessary, try running:
```
xfce4-notifyd-config
/usr/lib/x86_64-linux-gnu/xfce4/notifyd/xfce4-notifyd
```

## install cron job

```
crontab cron/unixy_time_tracker
```

## add this directory to your PATH (fish)
```
set -U fish_user_paths $fish_user_paths ~/unixy_time_tracker/
```

## setup postgres
```
sudo --login --user=postgres psql -c "create user hours;"
sudo --login --user=postgres psql -c "alter user hours with password 'hours';"
sudo --login --user=postgres psql -c "create database 'hours';"
sudo --login --user=postgres pg_restore -c -C -s -v -d hours < hours_db
sudo --login --user=postgres psql -c "grant all privileges on database hours to hours;"
```


## set up keyboard shortcuts:
```
"ctrl + alt + [" to "~/unixy_time_tracker/tt on"
"ctrl + alt + ]" to "~/unixy_time_tracker/tt off"
```



# sample interaction
```
koom@dev ~/unixy_time_tracker (master) [1]> tt on "boring task 1"
db updated.
0:00:35.435037 xbrl
7:49:22.200187 pyco3
4:20:07.766982 semantics
1:36:57.089243 modules
db updated.
on
MPlayer 1.3.0 (Debian), built with gcc-7 (C) 2000-2016 MPlayer Team
[mplayer output ommited..]
Exiting... (End of file)

koom@dev ~/unixy_time_tracker (master)> tt on "boring task 2"
db updated.
0:00:35.435037 xbrl
7:49:22.200187 pyco3
4:20:07.766982 semantics
1:36:57.089243 modules
0:00:15.851025 boring task 1
0:00:00.017912 boring task 2
db updated.
on
MPlayer 1.3.0 (Debian), built with gcc-7 (C) 2000-2016 MPlayer Team
[mplayer output ommited..]
Exiting... (End of file)

koom@dev ~/unixy_time_tracker (master)> tt on "boring task 1"
db updated.
0:00:35.435037 xbrl
7:49:22.200187 pyco3
4:20:07.766982 semantics
1:36:57.089243 modules
0:00:15.851025 boring task 1
0:00:10.980661 boring task 2
0:00:00.048821 boring task 1
db updated.
on
MPlayer 1.3.0 (Debian), built with gcc-7 (C) 2000-2016 MPlayer Team
[mplayer output ommited..]
Exiting... (End of file)

koom@dev ~/unixy_time_tracker (master) [1]> tt info
0:00:35.435037 xbrl
7:49:22.200187 pyco3
4:20:07.766982 semantics
1:36:57.089243 modules
0:00:48.215652 boring task 1
0:00:10.980661 boring task 2
running.

koom@dev ~/unixy_time_tracker (master)> tt csv
#hours;task
xbrl;0.0
pyco3;7.8
semantics;4.3
modules;1.6
boring task 1;0.0
boring task 2;0.0

```


# useful queries
```
﻿delete from hours where ts < '2020-06-01 00:00:14.05933+01';
```

