Prefix: JAQ
Next: 4

### JAQ-3 · P3 · `--help` still sends users to the upstream manual

- **Area:** Docs
- **Where:** `jaq/src/help.txt:45`
- **Problem:** `jaq --help` ends with `https://gedenkt.at/jaq/manual/`. That site documents upstream jaq, including the `repl` filter and CBOR in the default binary. This tree removed `repl` and omits CBOR unless `--features cbor` is set. The in-repo manual source now says so. `help.txt` is compiled in with `include_str!` (`jaq/src/main.rs:57`), so changing it changes the binary.
- **Recommendation:** Point `--help` at the manual built from `docs/`, or add one line that CBOR and `repl` are not in the default binary. Do not leave the upstream URL as the only pointer.
- **Fix with:** docs-refresh
- **Effort:** S
