Prefix: DSLP
Next: 8

Deslop campaign backlog ([plan](https://github.com/laputa-systems/stuff/blob/main/docs/campaigns/deslop.md), tier E). One agent works this file with the `deslop` skill: take the lowest-numbered open ticket whose area does not start with `Needs owner ·`. After DSLP-5, work the open P1 and P2 findings, then fill in `## Report` below.

## Report

Base: `ac261459a1e70af07d7495f0d14af4806e665c22`; upstream merge base: `d65e5a6cbeb8b4c352de8886188524738ded0851`.

Types: no stricter setting adopted; no fork-owned defect or deleted escape hatch was demonstrated. The candidate run reported one unsafe memory map; 41 wildcard enum matches, 2 single-variant wildcard matches, 6 possible truncations, 2 sign-loss casts, 43 source unwraps (34 more in tests/examples), no source expects (1 in tests/examples), 1 source redundant clone (2 more in tests/examples), and 8 pass-by-value warnings. These counts are diagnostic occurrences, excluding Cargo's duplicate summaries; warnings alone do not establish defects. The memory map is upstream; the fork's help tests use unwraps. The existing profile remains clean; the Rust escape-hatch search matched 93 lines before and after.

Tests: workspace tests increased from 386 to 388. Reported suite execution sums were 2.87s before and 2.09s after on a busy host; `make test` was 7.87s before and 30.74s after. Injected faults caught: select `USERPROFILE` instead of `HOME` (module lookup failed), enable CBOR in the default dependency graph (default rejection check failed), emit byte `00` instead of CBOR `01` (exact-output test failed), make `repl` succeed (exit-code assertion failed), and alter the help footer (footer assertion failed). All faults were restored. Needs environment: line and branch coverage and automated mutant counts were not measured because cargo-llvm-cov and cargo-mutants are unavailable; no mutation CI lane was added under the owner ruling.

Dead code: rustc `dead_code` is covered by warnings-denied workspace clippy; a separate `unreachable_pub` check reported 13 CLI and 35 library diagnostics on upstream declarations. No fork-owned removal was established, and no code or dependencies were removed. Needs environment: cargo-machete and cargo-udeps are unavailable. The upstream `jaq/tests/repl.exp` fixture has no remaining registration after this fork removed the filter; it is outside the authorized edit scope.

Bench: the upstream harness covers startup, definitions and synthetic filter workloads; it lacks completed-output checks, representative file/format journeys, memory and attribution. The new entry point checks selection in Edit (0.08s observed) and exercises the existing `upto` fixture in Change (0.48s observed, release build 380.51s); a wrong-output fault failed as intended. Host readiness checks passed around that one run, which is not a performance verdict. Full was not run and requires explicit opt-in on Linux. DSLP-7 tracks the remaining coverage and observability gaps.

## Tickets

### DSLP-7 · P3 · Add representative performance outcomes and attribution

- **Area:** performance · benchmarks
- **Where:** bench.sh, examples/benches.json
- **Problem:** The upstream harness times synthetic filters and startup but does not assert completed outputs or cover representative file and format journeys, memory, or attribution; it also depends on GNU time and its shell loops can mask failures.
- **Recommendation:** Design representative CLI and library workloads with output oracles and CPU, memory, and attribution evidence; preserve the existing public behavior.
- **Fix with:** bench-pyramid
- **Effort:** M

