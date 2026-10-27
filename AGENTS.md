# jaq

jq implementation in this workspace. The CLI crate is `jaq`. The libraries are `jaq-core`, `jaq-std`, `jaq-json`, `jaq-fmts`, and `jaq-all`.

## Commands

- `cargo test --locked -p jaq` tests the default binary. CBOR is off.
- `cargo build --locked -p jaq --features cbor` builds the binary with CBOR.
- `cargo test --workspace --locked` unifies features, so those tests see CBOR even though `cargo build -p jaq` does not.
- `make clippy` runs clippy on the workspace with warnings denied.

`rust-toolchain.toml` pins `nightly-2026-09-15`.

## Invariants

- The default CLI has no CBOR, no `repl` filter, no Windows special case, and no mimalloc global allocator.
- `~` in a module search path expands with `HOME` only (`jaq-core/src/load/mod.rs`).
- Manual source is `docs/*.dj`. `jaq --help` prints `jaq/src/help.txt`.

## Map

- Install and what this tree ships: `README.md`
- Manual generation: `docs/README.md`
- Open work: `TODO.md`
