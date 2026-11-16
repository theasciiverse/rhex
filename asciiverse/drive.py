"""Plays Rhex for the catalog preview (asciiverse/record-preview.sh).

Reads the tmux pane and presses keys at a watchable pace: past the
introduction, picks a dwarf, then explores (o) the Dark Forest. When a
creature comes near, the dwarf closes in, turns (l) until it stands in
front and attacks by moving into it (k); hurt by something it is not
facing, it looks round. Once the level is explored it walks to
the onward exit (G, >) and goes through (>). Quits (Esc, y) after about
LENGTH seconds.
    python3 -I drive.py <tmux socket> <session> [length] [debug]
"""
import re
import subprocess
import sys
import time

SOCK, SESS = sys.argv[1], sys.argv[2]
LENGTH = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0
DEBUG = len(sys.argv) > 4
T0 = time.time()
MAP_W = 70  # the sidebar starts at column 70
CREATURES = ("rat", "goblin", "troll", "wolf", "cave beetle", "skeleton", "pony")


def tmux(*args):
    return subprocess.run(["tmux", "-L", SOCK, *args], capture_output=True,
                          text=True).stdout


def screen():
    return tmux("capture-pane", "-p", "-t", SESS).split("\n")


def key(k, wait=0.3):
    if DEBUG:
        print(round(time.time() - T0, 1), k, file=sys.stderr)
    tmux("send-keys", "-t", SESS, k)
    time.sleep(wait)


def panel(rows, label):
    for r in rows:
        m = re.search(label + r":\s*(.*?)(\s{2,}|$)", r)
        if m:
            return m.group(1).strip().lower()
    return ""


def foe_near(rows):
    """Distance in rows and columns from @ to the nearest creature letter."""
    hero, foes = None, []
    for y, r in enumerate(rows):
        for x, c in enumerate(r[:MAP_W]):
            if c == "@":
                hero = (x, y)
            elif c in "rgTwbsp":
                foes.append((x, y))
    if DEBUG and foes:
        print("foes", foes, "hero", hero, file=sys.stderr)
    if not hero or not foes:
        return None
    return min(max(abs(f[0] - hero[0]) // 2, abs(f[1] - hero[1])) for f in foes)


def hit_points(rows):
    for r in rows:
        m = re.search(r"HP:\s*(\d+)/", r)
        if m:
            return int(m.group(1))
    return None


def log_text(rows):
    return "\n".join(rows)


time.sleep(1.0)
key("x", 1.0)          # past the introduction
key("c", 1.2)          # a dwarf: strong, armoured and long-winded
stuck = turns = cooldown = hurt = 0
last_hp = None
while time.time() - T0 < LENGTH:
    rows = screen()
    front = panel(rows, "In front")
    near = foe_near(rows)
    if any(c in front for c in CREATURES):
        key("k", 0.35)
        continue
    hp = hit_points(rows)
    if hp is not None and last_hp is not None and hp < last_hp:
        hurt = 4        # struck by something it is not facing: look round
    last_hp = hp if hp is not None else last_hp
    if hurt:
        hurt -= 1
        key("l", 0.25)
        continue
    near_foe = near is not None and near <= 1
    if near_foe and turns < 6:
        key("l", 0.25)  # face whatever is next to the dwarf
        turns += 1
        continue
    turns = 0
    text = log_text(rows)
    exit_seen = any(">" in r[:MAP_W] for r in rows)
    if cooldown == 0 and (exit_seen or "Nothing else to explore" in text or stuck > 3):
        failed = text.count("Can't get there")
        key("G", 0.3)
        key(">", 2.5)
        if log_text(screen()).count("Can't get there") > failed:
            cooldown = 4    # no known way yet: explore some more
        else:
            key(">", 1.5)
        stuck = 0
        continue
    cooldown = max(0, cooldown - 1)
    before = text
    key("o", 1.5)
    if log_text(screen()) == before:
        stuck += 1
key("Escape", 0.8)
key("y", 0.6)
