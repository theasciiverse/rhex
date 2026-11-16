//! Session logging with `log` and `env_logger`.
//!
//! The terminal belongs to the game, so the log goes to a file, never to
//! stderr: `rhex.log` in the state folder, started fresh every session.
//! `RUST_LOG` picks what is written, as env_logger reads it everywhere else:
//! without it only errors, `RUST_LOG=info` adds mode changes, levels entered
//! and deaths, and `RUST_LOG=debug` adds every raw terminal event and a
//! snapshot of the game once a second.

use std::fs::{self, File};
use std::path::PathBuf;

/// File name of the session log inside the state folder.
const LOG_FILE: &str = "rhex.log";

/// The folder for rhex's own files: `$XDG_STATE_HOME/rhex`, else
/// `~/.local/state/rhex` on Unix and `%LOCALAPPDATA%\rhex` on Windows.
/// Unit tests have none, so they never write into a real state folder.
pub fn state_dir() -> Option<PathBuf> {
    if cfg!(test) {
        return None;
    }
    let nonempty = |name: &str| std::env::var_os(name).filter(|value| !value.is_empty());
    let base = nonempty("XDG_STATE_HOME").map(PathBuf::from).or_else(|| {
        if cfg!(windows) {
            nonempty("LOCALAPPDATA").map(PathBuf::from)
        } else {
            nonempty("HOME").map(|home| PathBuf::from(home).join(".local").join("state"))
        }
    })?;
    Some(base.join("rhex"))
}

/// Start the session log. The game plays on without one when the state
/// folder cannot be found or written.
pub fn init() {
    let Some(dir) = state_dir() else {
        return;
    };
    let file = match fs::create_dir_all(&dir).and_then(|()| File::create(dir.join(LOG_FILE))) {
        Ok(file) => file,
        Err(_) => return,
    };
    let _ = env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("error"))
        .target(env_logger::Target::Pipe(Box::new(file)))
        .format_timestamp_millis()
        .try_init();
}
