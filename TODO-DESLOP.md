Prefix: DSLP
Next: 6

Deslop campaign backlog ([plan](https://github.com/laputa-systems/stuff/blob/main/docs/campaigns/deslop.md), tier E). One agent works this file with the `deslop` skill: take the lowest-numbered open ticket whose area does not start with `Needs owner ·`. After DSLP-5, work the open P1 and P2 findings, then fill in `## Report` below.

## Report

Base: `ac261459a1e70af07d7495f0d14af4806e665c22`; upstream merge base: `d65e5a6cbeb8b4c352de8886188524738ded0851`.

Types: no stricter setting adopted; no fork-owned defect or deleted escape hatch was demonstrated. The candidate run reported one unsafe memory map; 41 wildcard enum matches, 2 single-variant wildcard matches, 6 possible truncations, 2 sign-loss casts, 43 source unwraps (34 more in tests/examples), no source expects (1 in tests/examples), 1 source redundant clone (2 more in tests/examples), and 8 pass-by-value warnings. These counts are diagnostic occurrences, excluding Cargo's duplicate summaries; warnings alone do not establish defects. The memory map is upstream; the fork's help tests use unwraps. The existing profile remains clean; the Rust escape-hatch search matched 93 lines before and after.

## Tickets

### DSLP-4 · P2 · Tests: coverage, boundary gaps, mutation

- **Area:** deslop · tests
- **Where:** test suites and CI
- **Problem:** Coverage and mutation results are unmeasured; no deslop mutation lane exists.
- **Recommendation:** Run the deslop Tests step. Accept: no undispositioned survivor in critical code, the test cost budget holds, and the lane is green where the tools are mirrored.
- **Fix with:** deslop
- **Effort:** M

### DSLP-5 · P2 · Dead code: tools and debloat

- **Area:** deslop · dead code
- **Where:** whole repository (our changes)
- **Problem:** No dead-code scan has run.
- **Recommendation:** Run the deslop Dead code step. Accept: tools clean or allowlisted with reasons; walk-backs filed as Needs owner tickets.
- **Fix with:** deslop
- **Effort:** M

