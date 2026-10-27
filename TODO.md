Prefix: JAQ
Next: 4

### JAQ-1 · P3 · Declared Rust 1.70 does not match the lockfile

- **Area:** Build
- **Where:** `jaq-core/Cargo.toml:12`, `jaq/Cargo.toml:12`, `jaq-std/Cargo.toml:11`, `jaq-json/Cargo.toml:12`, `jaq-fmts/Cargo.toml:11`, `jaq-all/Cargo.toml:11`, `Cargo.lock:217`, `Cargo.lock:239`, `Cargo.lock:251`
- **Problem:** Every crate manifest says `rust-version` 1.69 (`jaq-core`) or 1.70 (the others). `cargo update` in this fork moved `hashbrown` to 0.17.1, `indexmap` to 2.14.2, and `getrandom` to 0.4.3. Those crates set edition 2024 and `rust-version` 1.85. `cargo tree -p jaq` shows `hashbrown` under `jaq-json` and `getrandom` under `tempfile`, so the CLI build needs them. A compiler that honors the declared floor cannot compile this lockfile. The pinned toolchain is `nightly-2026-09-15`, and `cargo check -p jaq --locked --offline` succeeded there. Rust 1.70 was not installed here, so that floor was not executed.
- **Recommendation:** Pick one floor. Either set every crate `rust-version` to at least 1.85, or pin `hashbrown`, `indexmap`, and `getrandom` back to releases that still compile on the version you claim.
- **Fix with:** upgrade
- **Effort:** S

### JAQ-2 · P3 · Workspace tests do not build the binary this tree ships

- **Area:** Tests
- **Where:** `jaq/Cargo.toml:14`, `jaq-fmts/Cargo.toml:14`, `jaq-fmts/tests/formats.rs:37`, `jaq-fmts/tests/funs.rs:6`, `.github/workflows/test.yml:36`, `.github/workflows/release.yml:52`
- **Problem:** The default `jaq` binary enables `jaq-all` feature `formats-no-cbor`, not `formats`. `cargo tree -p jaq --offline` does not contain `ciborium-ll`. `cargo tree -p jaq --features cbor --offline` does, and `cargo check -p jaq --features cbor --locked --offline` succeeded. `cargo test --workspace` unifies features with `jaq-fmts`'s default `all`, which includes `cbor`, so the tested `jaq` binary is not the release binary. `cargo test -p jaq-fmts --no-default-features --features all-no-cbor --locked --offline --no-run` failed: `read::cbor` is cfg'd out at `jaq-fmts/src/read/mod.rs:3`, and `jaq-fmts/tests/formats.rs:37` still calls it. The same command also failed `Val: Deserialize` in `jaq-fmts/tests/common/mod.rs:34` because the `serde` feature of `jaq-json` was not enabled. That serde failure was not compared with a default-feature `cargo test -p jaq-fmts`.
- **Recommendation:** Gate the CBOR tests on `feature = "cbor"`. Test `jaq` with the same features as `cargo build -p jaq`, not only under workspace feature unification. The release workflow runs `cargo test --workspace` and then `cargo build -p jaq` as a second invocation, so it has the same split.
- **Fix with:** test-audit
- **Effort:** S

### JAQ-3 · P3 · `--help` still sends users to the upstream manual

- **Area:** Docs
- **Where:** `jaq/src/help.txt:45`
- **Problem:** `jaq --help` ends with `https://gedenkt.at/jaq/manual/`. That site documents upstream jaq, including the `repl` filter and CBOR in the default binary. This tree removed `repl` and omits CBOR unless `--features cbor` is set. The in-repo manual source now says so. `help.txt` is compiled in with `include_str!` (`jaq/src/main.rs:57`), so changing it changes the binary.
- **Recommendation:** Point `--help` at the manual built from `docs/`, or add one line that CBOR and `repl` are not in the default binary. Do not leave the upstream URL as the only pointer.
- **Fix with:** docs-refresh
- **Effort:** S
