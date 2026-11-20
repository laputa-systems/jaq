Prefix: DSLP
Next: 8

Deslop campaign backlog ([plan](https://github.com/laputa-systems/stuff/blob/main/docs/campaigns/deslop.md), tier E). One agent works this file with the `deslop` skill: take the lowest-numbered open ticket whose area does not start with `Needs owner ·`. After DSLP-5, work the open P1 and P2 findings, then fill in `## Report` below.

## Report

Base: `ac261459a1e70af07d7495f0d14af4806e665c22`; upstream merge base: `d65e5a6cbeb8b4c352de8886188524738ded0851`.

Scorecard: Rust source lines 12,196 → 12,196; Rust test lines 2,480 → 2,520 (tracked `.rs` files, tests classified by path). Workspace tests 386 → 388; warm `make test` 7.87s → 30.74s in the recorded comparison. Escape-hatch matching lines 93 → 93. Removed: 0 lines of production code and 0 dependencies. Coverage and automated mutants: Needs environment; no caught/missed/timeout/unviable totals are available. Five selected hand-injected faults were caught; no broad survivor count was measured. Findings: 0 reproduced P1, 0 reproduced P2, 1 P3 filed, 0 fixed. Performance: one checked workload, no comparative verdict. Escaped regressions: none observed; production escape rate was not measured.

Step costs on this busy macOS arm64 host, wall time: Ground cold test output completed in 632.53s but its wrapper failed to capture the exit; warm test passed in 7.87s, lint in 492.76s. Diagnose: default CLI tests 112.30s, workspace test 5.75s, lint 25.18s. Types: candidate profile 148.00s, test 39.43s, lint 164.33s. Tests: test 30.74s, lint 41.54s, plus focused fault checks. Dead code: scan 51.76s, test 34.80s, lint 24.74s. Bench: release build 380.51s, Edit 0.08s, Change 0.48s, test 4.68s, lint 25.30s. Report: test 14.36s, lint 34.86s, plus the focused review checks. CI minutes: Needs environment; the parent owns remote CI and this pass did not run it.

Types: no stricter setting adopted; no fork-owned defect or deleted escape hatch was demonstrated. The candidate run reported one unsafe memory map; 41 wildcard enum matches, 2 single-variant wildcard matches, 6 possible truncations, 2 sign-loss casts, 43 source unwraps (34 more in tests/examples), no source expects (1 in tests/examples), 1 source redundant clone (2 more in tests/examples), and 8 pass-by-value warnings. These counts are diagnostic occurrences, excluding Cargo's duplicate summaries; warnings alone do not establish defects. The memory map is upstream; the fork's help tests use unwraps. The existing profile remains clean; the Rust escape-hatch search matched 93 lines before and after.

Tests: workspace tests increased from 386 to 388. Reported suite execution sums were 2.87s before and 2.09s after on a busy host; `make test` was 7.87s before and 30.74s after. Injected faults caught: select `USERPROFILE` instead of `HOME` (module lookup failed), enable CBOR in the default dependency graph (default rejection check failed), emit byte `00` instead of CBOR `01` (exact-output test failed), make `repl` succeed (exit-code assertion failed), and alter the help footer (footer assertion failed). All faults were restored. Needs environment: line and branch coverage and automated mutant counts were not measured because cargo-llvm-cov and cargo-mutants are unavailable; no mutation CI lane was added under the owner ruling.

Dead code: rustc `dead_code` is covered by warnings-denied workspace clippy; a separate `unreachable_pub` check reported 13 CLI and 35 library diagnostics on upstream declarations. No fork-owned removal was established, and no code or dependencies were removed. Needs environment: cargo-machete and cargo-udeps are unavailable. The upstream `jaq/tests/repl.exp` fixture has no remaining registration after this fork removed the filter; it is outside the authorized edit scope.

Bench: the upstream harness covers startup, definitions and synthetic filter workloads; it lacks completed-output checks, representative file/format journeys, memory and attribution. The new entry point checks selection in Edit (0.08s observed) and exercises the existing `upto` fixture in Change (0.48s observed, release build 380.51s); a wrong-output fault failed as intended. Host readiness checks passed around that one run, which is not a performance verdict. Full was not run and requires explicit opt-in on Linux. DSLP-7 tracks the remaining coverage and observability gaps.

Review: cumulative local changes were inspected; the benchmark failure summary and test error propagation were corrected. Method feedback: workspace feature unification hides the default binary's CBOR contract, so the test entry point now exercises it separately. Shared-file gap: the prescribed Rust coverage and mutation tools are unavailable on this host and mirror; no shared files were edited. Remaining: DSLP-7 (P3). No owner decision was identified.

## Tickets

### DSLP-7 · P3 · Add representative performance outcomes and attribution

- **Area:** performance · benchmarks
- **Where:** bench.sh, examples/benches.json
- **Problem:** The upstream harness times synthetic filters and startup but does not assert completed outputs or cover representative file and format journeys, memory, or attribution; it also depends on GNU time and its shell loops can mask failures.
- **Recommendation:** Design representative CLI and library workloads with output oracles and CPU, memory, and attribution evidence; preserve the existing public behavior.
- **Fix with:** bench-pyramid
- **Effort:** M

