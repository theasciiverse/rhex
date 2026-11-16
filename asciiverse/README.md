# Rhex

**Something in the Dark Forest heard that. Which way are you facing?**

You start among the brown trunks and green thickets of the Dark Forest,
with a creek winding through it, a still pond and a few small clearings
where light breaks through the canopy. Everywhere else is dark. You hear
a rat before you see it. You see a wolf only when it is already turning
toward you, a yellow **!** flashing over its head: it knows you are there.

Rhex is a roguelike on a grid of hexagons, and you have a front and a
back. Turning is a move of its own, you see what lies ahead of you, and
anything that reaches your back hits twice as hard and twice as surely.
So does your blade, if you get behind it. Every step, door, swing and
rattle of a buckler makes noise that travels through the trees, damped
by thickets and stopped by trunks, and the creatures of the forest and
the Dungeon below come to find out what made it.

Take the path onward and the forest gives way to the Dungeon: stone
rooms lit by wall-side torches, closed doors, chests that open loudly and
are sometimes empty, cave beetles in their armour and skeletons with
short swords and bucklers. Then forest again, deeper, and Dungeon again.
Every level you leave is still there when you climb back, with its
creatures, its open chests and whatever you dropped.

- **Human, elf or dwarf**: the elf sees farthest in the dark, the dwarf
  hits hardest and runs longest
- **Light is a choice**: a hand lantern in your left hand shows the way
  and shows you to everything else
- **Sound is a lure and a giveaway**: a whistle may bring them over; a
  club is easy to swing and loud to use
- **Charge** two hexes at a foe, if you have the stamina

Rhex is unfinished, as its author says, and very much playable. There
is no saving: a run lasts as long as you do.

## Playing

Run `rhex` in a terminal of at least 60x24 with 256 colours and a
Unicode font; 100x30 gives a comfortable layout. Press a key at the
introduction, then pick a race (`a` human, `b` elf, `c` dwarf).

- **h** / **l** or **Left** / **Right**: turn
- **k** / **j** or **Up** / **Down**: step forward or back; walk into a
  creature to attack it, into a door to open it, into a thicket to cut it
- **H** / **L**: strafe front-left or front-right without turning
- **c**: charge; **.**: wait; **o**: explore; **G** then **>** or **<**:
  walk to a passage
- **>** or **<**: take the passage you stand on
- **,**: pick up, open the chest or door in front of you
- **I**: inventory, then an item's letter for what you can do with it;
  **E** equip or use, **D** drop
- **x**: examine; **F2**: Vi keys (then **q** quits too); **?**: help;
  **Esc**: quit

## The session log

Rhex writes `rhex.log` in its state folder (`$XDG_STATE_HOME/rhex`, else
`~/.local/state/rhex`, or `%LOCALAPPDATA%\rhex` on Windows), new each
session. `RUST_LOG=info rhex` records mode changes, levels and deaths;
`RUST_LOG=debug rhex` adds every key and a snapshot of the game each
second, which makes a bug report easy to follow.

## Credits

- Rhex: Dawid Ciężarkiewicz (dpc), https://github.com/dpc/rhex, with
  Demur Rumed, Christopher Serr and other contributors (MPL-2.0, see
  LICENSE)
- Built on hex2d by the same author, Crossterm and Ratatui
- This package: Asciiverse, for the av launcher and the catalog at
  https://asciiverse.sh. What we changed is in PATCHES.md.

## Building

`cargo build --release --locked` with a current stable Rust builds the
game; the release workflow (`.github/workflows/asciiverse-release.yml`)
builds static Linux binaries in Alpine, and macOS and Windows on their
own runners. The upstream README in the repository covers the Nix
development setup and the test suite.
