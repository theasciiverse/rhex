#!/bin/sh
# Records the 100x30 catalog preview, asciiverse/rhex.cast
# (hub/RECORDING.md): the introduction, then a dwarf exploring the Dark
# Forest, fighting what comes close and taking the path onward into the
# Dungeon, played by asciiverse/drive.py, and quitting at the end.
# asciinema records a tmux pane (own socket, no status line, no user
# config) that drive.py reads and plays into. The maps are random, so
# record a few and keep the best. Needs asciinema 3 and tmux.
#   asciiverse/record-preview.sh target/release/rhex [seconds]
set -eu
binary=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
length=${2:-50}
here=$(cd "$(dirname "$0")" && pwd)
out=$here/rhex.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir "$home/bin" && cp "$binary" "$home/bin/rhex"
cd "$home"  # nothing in the recording names a local path
export HOME="$home" XDG_STATE_HOME="$home/state" \
  PATH="$home/bin:$PATH" USER=player LOGNAME=player \
  TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 rhex \; set -g status off
python3 -I "$here/drive.py" avrec rec "$length" &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "Rhex" \
  --command "tmux -L avrec attach -t rec" "$out"
wait "$drive"
