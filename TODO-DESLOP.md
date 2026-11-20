Prefix: DSLP
Next: 7

Deslop campaign backlog ([plan](https://github.com/laputa-systems/stuff/blob/main/docs/campaigns/deslop.md), tier E). One agent works this file with the `deslop` skill: take the lowest-numbered open ticket whose area does not start with `Needs owner ·`. After DSLP-5, work the open P1 and P2 findings, then fill in `## Report` below.

## Report

Base: `ac261459a1e70af07d7495f0d14af4806e665c22`; upstream merge base: `d65e5a6cbeb8b4c352de8886188524738ded0851`.

Types: no stricter setting adopted; no fork-owned defect or deleted escape hatch was demonstrated. The candidate run reported one unsafe memory map; 41 wildcard enum matches, 2 single-variant wildcard matches, 6 possible truncations, 2 sign-loss casts, 43 source unwraps (34 more in tests/examples), no source expects (1 in tests/examples), 1 source redundant clone (2 more in tests/examples), and 8 pass-by-value warnings. These counts are diagnostic occurrences, excluding Cargo's duplicate summaries; warnings alone do not establish defects. The memory map is upstream; the fork's help tests use unwraps. The existing profile remains clean; the Rust escape-hatch search matched 93 lines before and after.

Tests: workspace tests increased from 386 to 388. Reported suite execution sums were 2.87s before and 2.09s after on a busy host; `make test` was 7.87s before and 30.74s after. Injected faults caught: select `USERPROFILE` instead of `HOME` (module lookup failed), enable CBOR in the default dependency graph (default rejection check failed), emit byte `00` instead of CBOR `01` (exact-output test failed), make `repl` succeed (exit-code assertion failed), and alter the help footer (footer assertion failed). All faults were restored. Needs environment: line and branch coverage and automated mutant counts were not measured because cargo-llvm-cov and cargo-mutants are unavailable; no mutation CI lane was added under the owner ruling.

Dead code: rustc `dead_code` is covered by warnings-denied workspace clippy; a separate `unreachable_pub` check reported 13 CLI and 35 library diagnostics on upstream declarations. No fork-owned removal was established, and no code or dependencies were removed. Needs environment: cargo-machete and cargo-udeps are unavailable. The upstream `jaq/tests/repl.exp` fixture has no remaining registration after this fork removed the filter; it is outside the authorized edit scope.

## Tickets

### DSLP-6 · P2 · Bench: audit and selective entry point

- **Area:** deslop · bench
- **Where:** bench.sh, examples/benches.json, Makefile
- **Problem:** The existing upstream benchmark harness has not been audited or given a selective entry point in this fork.
- **Recommendation:** Run the deslop Bench step, preserving upstream code and proving Edit and one Change workload.
- **Fix with:** deslop
- **Effort:** M

