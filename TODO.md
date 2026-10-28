Prefix: JAQ
Next: 4

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
