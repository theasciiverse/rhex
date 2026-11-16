@AGENTS.md

# Rhex (Asciiverse packaging)

Dawid Ciężarkiewicz's Rhex (Rust, Crossterm, Ratatui, MPL-2.0), a
hex-grid roguelike of facing, light and sound, packaged for the
Asciiverse catalog (id `rhex`, kind `game`, genre `roguelike`). Not our
code: the game stays as its author made it; list every change in
PATCHES.md and keep each one offerable upstream (UPSTREAM.md).

- `upstream` is github.com/dpc/rhex (branch `master`); ours is branch
  `asciiverse`, `origin` github.com/theasciiverse/rhex (private).
- Release: tag `v<Cargo version>+<upstream commit date>-av.<n>` (first
  `v0.1.1+20261021-av.1`) and push it;
  `.github/workflows/asciiverse-release.yml` builds Linux (static musl in
  Alpine), macOS and Windows.
- No saves or settings; the session log is `rhex.log` in
  `$XDG_STATE_HOME/rhex` (`RUST_LOG=debug` for input and snapshots).
- Tests, scripted runs and recordings: scratch `HOME` and
  `XDG_STATE_HOME` in the same command, under
  `systemd-run --user --scope -p MemoryMax=4G`, `cargo -j4`.
- Needs 60x24 (the game pauses and asks for more below that) and 256
  colours; 100x30 for a comfortable layout.
- Preview: `asciiverse/record-preview.sh target/release/rhex` (random
  maps: record a few, keep the best).
- Catalog drafts: `asciiverse/rhex.toml` and `.md`; package README
  `asciiverse/README.md` (shipped as README.md in the archives).
