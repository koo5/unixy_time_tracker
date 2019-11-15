# unixy_time_tracker
inspired by upwork's time tracker app. python. postgresql. cron. mplayer. xprintidle. csv export. you've got to have this

# setup
```
sudo apt install xprintidle postgresql mplayer
```

# make sure notifications work:
```notify-send --expire-time=3000  Test "Hello World"```
```
if necessary, try:
xfce4-notifyd-config
/usr/lib/x86_64-linux-gnu/xfce4/notifyd/xfce4-notifyd
```

change "user" and:```
cat cron_entries >> /etc/crontab
```

add this directory to your PATH

setup postgres: todo

set up keyboard shortcuts, if desired:
"ctrl + alt + [" to "tt on"
"ctrl + alt + ]" to "tt off"


