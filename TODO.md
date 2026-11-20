Prefix: JAQ
Next: 5
### JAQ-4 · P3 · Add representative performance outcomes and attribution

- **Area:** performance · benchmarks
- **Where:** bench.sh, examples/benches.json
- **Problem:** The upstream harness times synthetic filters and startup but does not assert completed outputs or cover representative file and format journeys, memory, or attribution; it also depends on GNU time and its shell loops can mask failures.
- **Recommendation:** Design representative CLI and library workloads with output oracles and CPU, memory, and attribution evidence; preserve the existing public behavior.
- **Fix with:** bench-pyramid
- **Effort:** M
