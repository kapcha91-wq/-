#!/bin/bash
# usage: ./make_silent.sh page.html seconds out.mp4  -> silent 1080x1920 30fps video (music is added in Instagram)
set -e
name=$(basename "$1" .html); fr="fr_${name}_silent"
rm -rf "$fr"; node render.js "$1" "$fr" "$2" 30 > /dev/null
ffmpeg -v error -y -framerate 30 -i "$fr/%05d.jpg" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high -an -movflags +faststart "$3"
rm -rf "$fr"; echo "$3"
