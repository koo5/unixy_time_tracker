# unixy_time_tracker
inspired by upwork's time tracker app. python. postgresql. cron. mplayer. xprintidle. 

alternatives: https://github.com/meetmangukiya/bth-py

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
do_connect: could not connect to socket
connect: No such file or directory
Failed to open LIRC support. You will not be able to use your remote control.

Playing /usr/share/sounds/KDE-Im-Contact-In.ogg.
libavformat version 57.83.100 (external)
libavformat file format detected.
[lavf] stream 0: audio (vorbis), -aid 0
Load subtitles in /usr/share/sounds/
==========================================================================
Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
libavcodec version 57.107.100 (external)
AUDIO: 48000 Hz, 2 ch, floatle, 192.0 kbit/6.25% (ratio: 24000->384000)
Selected audio codec: [ffvorbis] afm: ffmpeg (FFmpeg Vorbis)
==========================================================================
AO: [pulse] 48000Hz 2ch floatle (4 bytes per sample)
Video: no video
Starting playback...
A:   0.6 (00.6) of 0.8 (00.7)  0.4% 


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
do_connect: could not connect to socket
connect: No such file or directory
Failed to open LIRC support. You will not be able to use your remote control.

Playing /usr/share/sounds/KDE-Im-Contact-In.ogg.
libavformat version 57.83.100 (external)
libavformat file format detected.
[lavf] stream 0: audio (vorbis), -aid 0
Load subtitles in /usr/share/sounds/
==========================================================================
Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
libavcodec version 57.107.100 (external)
AUDIO: 48000 Hz, 2 ch, floatle, 192.0 kbit/6.25% (ratio: 24000->384000)
Selected audio codec: [ffvorbis] afm: ffmpeg (FFmpeg Vorbis)
==========================================================================
AO: [pulse] 48000Hz 2ch floatle (4 bytes per sample)
Video: no video
Starting playback...
A:   0.6 (00.6) of 0.8 (00.7)  0.3% 


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
do_connect: could not connect to socket
connect: No such file or directory
Failed to open LIRC support. You will not be able to use your remote control.

Playing /usr/share/sounds/KDE-Im-Contact-In.ogg.
libavformat version 57.83.100 (external)
libavformat file format detected.
[lavf] stream 0: audio (vorbis), -aid 0
Load subtitles in /usr/share/sounds/
==========================================================================
Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
libavcodec version 57.107.100 (external)
AUDIO: 48000 Hz, 2 ch, floatle, 192.0 kbit/6.25% (ratio: 24000->384000)
Selected audio codec: [ffvorbis] afm: ffmpeg (FFmpeg Vorbis)
==========================================================================
AO: [pulse] 48000Hz 2ch floatle (4 bytes per sample)
Video: no video
Starting playback...
A:   0.7 (00.6) of 0.8 (00.7)  0.3% 


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
koom@dev ~/unixy_time_tracker (master)> 
```
