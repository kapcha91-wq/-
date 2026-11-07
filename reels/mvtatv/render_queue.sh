#!/bin/bash
# usage: ./render_queue.sh page.html:seconds:out_name ...  (two at a time)
cd "$(dirname "$0")"
run() { IFS=: read -r p d o <<< "$1"; ./make_silent.sh "$p" "$d" "out/bez_ozvuchki/$o.mp4" >> render_queue.log 2>&1 || echo "FAIL $p" >> render_queue.log; }
pids=()
for job in "$@"; do run "$job" & pids+=($!); if [ ${#pids[@]} -ge 2 ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi; done
wait; echo DONE >> render_queue.log
