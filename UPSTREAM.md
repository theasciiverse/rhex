# Changes for upstream

Hi! The Asciiverse build of Rhex carries one change to the code, written
so it can be taken as it is or left out. PATCHES.md lists it with the
packaging files.

## Session logging (`src/logging.rs`, small calls in `src/terminal/`)

`logging::init()` wrote `debug.log` into the working directory with
`fern`, panicking when it could not open the file, and nothing logged to
it. The change:

- moves the log to `rhex.log` in the state folder (`$XDG_STATE_HOME/rhex`,
  else `~/.local/state/rhex`, or `%LOCALAPPDATA%\rhex` on Windows),
  truncated each session, so the game can start from any directory; if
  there is no usable folder it simply runs without a log
- uses `env_logger` with a file target, so `RUST_LOG` filters as usual
  (errors only by default), and drops `fern` and `chrono`
- logs session start and end, mode changes, the F2 input mode, new game
  and race, levels entered and the player's death at info; every raw
  crossterm event (in `Runner::run`, before `Ui::handle_event`) and a
  once-a-second snapshot of mode, size, queue, auto-move, turn, level,
  biome, depth, position, facing and HP/MP/SP at debug
- keeps tests out of real state folders: `state_dir()` is `None` under
  `cfg(test)`, and `tests/terminal.py` sets `XDG_STATE_HOME` to its work
  directory (the existing log-file assertion now looks there)

With `RUST_LOG=debug`, a player's bug report comes with the exact keys
and the state around them. `cargo test` passes, PTY tests included.
