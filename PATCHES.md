# Changes from upstream

This is the Asciiverse packaging of [Rhex](https://github.com/dpc/rhex)
by Dawid Ciężarkiewicz and contributors (MPL-2.0, `LICENSE`), a hex-grid
roguelike for the terminal in Rust on Crossterm and Ratatui. Upstream is
the `upstream` remote; this build is upstream's `master` at `dd1b6b6`
(2026-10-21), Cargo version 0.1.1, so our tags are
`v0.1.1+20261021-av.<n>`. The `asciiverse` branch carries the changes
below.

## The game

Unchanged: no rule, map generator, creature, item or line of game text is
touched. Rhex keeps no saves (a run lasts one session), reads no settings
files and makes no network connections.

## Code

- **Session logging into the state folder.** Upstream set up a `fern`
  logger that wrote `debug.log` into the current directory (and stopped
  with a panic where that directory was not writable), but nothing in the
  game logged to it. Now, with `log` and `env_logger`:
  - the log is `rhex.log` in the state folder, `$XDG_STATE_HOME/rhex`,
    else `~/.local/state/rhex`, or `%LOCALAPPDATA%\rhex` on Windows,
    started fresh each session; without a usable folder the game plays on
    unlogged (`src/logging.rs`)
  - `RUST_LOG` picks what is written, errors only by default
  - info: session start and end, mode changes, the input mode (F2), a new
    game and its race, each level entered, the player's death
    (`src/terminal/ui.rs`, `src/terminal/runner.rs`)
  - debug: every raw terminal event before it is dispatched, and a
    snapshot of the game once a second: mode, input mode, terminal size,
    queued actions, auto-move, turn, level, biome, depth, position and
    facing, HP, MP and SP (`src/terminal/ui.rs`)
  - unit tests have no state folder; the PTY tests (`tests/terminal.py`)
    point `XDG_STATE_HOME` at their own work directory
  - `fern` and `chrono` are dropped, `env_logger` added; `AutoMoveType`
    and `GoToType` derive `Debug` for the snapshot; the README says where
    the log is

UPSTREAM.md offers this change back.

## Packaging (new files)

- `.github/workflows/asciiverse-release.yml`: av archives for Linux
  (static musl, x86-64 and ARM64, built in Alpine), macOS (Intel and
  Apple silicon) and Windows (x86-64 and ARM64), plus SHA256SUMS. Each
  archive holds the `rhex` binary, `LICENSE`, this file and our
  `README.md`. Upstream's `ci.yml` (Nix) is left in place.
- `asciiverse/README.md`: the package README, shipped in the archives as
  `README.md` (upstream's README is mostly about developing the game).
- `asciiverse/record-preview.sh`, `asciiverse/drive.py`: the catalog
  preview, played by a script in a tmux pane.
- `asciiverse/rhex.toml`, `asciiverse/rhex.md`, `asciiverse/rhex.cast`:
  the catalog manifest, store page and preview, drafts for hub.
- `CLAUDE.md`, `PATCHES.md`, `UPSTREAM.md`: notes.
