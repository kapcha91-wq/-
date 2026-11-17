#!/bin/sh
# Rebuild assets/audio/{music,engine}.mp3 from synth.py. Run from the project root.
set -e
python3 audio-src/synth.py assets/audio
ffmpeg -hide_banner -loglevel error -y -i assets/audio/music.wav -af "highpass=f=28,lowpass=f=14000,loudnorm=I=-14:TP=-1.0" -c:a libmp3lame -b:a 192k assets/audio/music.mp3
ffmpeg -hide_banner -loglevel error -y -i assets/audio/engine.wav -af "highpass=f=35,equalizer=f=120:t=q:w=1:g=4,lowpass=f=6000,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5,volume='if(lt(t,2.4),1,if(lt(t,6.5),0.55,if(lt(t,8.6),1,max(0.4,1-(t-8.6)*0.6))))':eval=frame" -c:a libmp3lame -b:a 192k assets/audio/engine.mp3
rm assets/audio/music.wav assets/audio/engine.wav
