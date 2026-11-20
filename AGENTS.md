# jaq

jq implementation in this workspace. The CLI crate is `jaq`. The libraries are `jaq-core`, `jaq-std`, `jaq-json`, `jaq-fmts`, and `jaq-all`.

## Commands

- `cargo test --locked -p jaq` tests the default binary. CBOR is off.
- `cargo build --locked -p jaq --features cbor` builds the binary with CBOR.
- `cargo test --workspace --locked` unifies features, so those tests see CBOR even though `cargo build -p jaq` does not.
- `make clippy` runs clippy on the workspace with warnings denied.

`rust-toolchain.toml` pins `nightly-2026-11-09`.

## Invariants

- The default CLI has no CBOR, no `repl` filter, no Windows special case, and no mimalloc global allocator.
- `~` in a module search path expands with `HOME` only (`jaq-core/src/load/mod.rs`).
- Manual source is `docs/*.dj`. `jaq --help` prints `jaq/src/help.txt`.

## Map

- Install and what this tree ships: `README.md`
- Manual generation: `docs/README.md`
- Open work: `TODO.md`

## Verification

- `make test` checks the default CLI and runs the workspace tests (388 passed; 30.74s on a busy host).
- `make lint` runs workspace clippy with warnings denied (cold 492.76s on a busy host).
- Edit: `cargo test --locked -p jaq --test distribution` checks module lookup (0.26s test time).
- Change: `cargo test --locked -p jaq --features cbor --test distribution` checks CBOR output (0.27s test time).
- CLI help and version: `jaq/tests/help.rs`; filter output: `jaq/tests/golden.rs`.
- Removed `repl` filter: `jaq/tests/distribution.rs`.
- Default CBOR rejection: `make test` builds the default CLI before workspace features are unified.
- CLI exit codes and remaining flags: no comprehensive boundary suite.
- Library filter evaluation and paths: `jaq-core/tests/`; JSON: `jaq-json/tests/`.
- CBOR, TOML and XML: `jaq-fmts/tests/formats.rs`; other formats: `jaq-fmts/tests/funs.rs`.
- Module search path expansion: `jaq/tests/distribution.rs`.
- Library consumers include `jaq`, `jaq-play`, and the other workspace crates.
- Performance workload: `bench.sh` and `examples/benches.json`; no regression gate.
