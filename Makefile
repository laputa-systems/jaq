.PHONY: bench bench-check bench-list bench-dry-run clippy lint test

TIER ?= edit
BENCH_ARGS = --tier "$(TIER)" $(if $(WORKLOAD),--workload "$(WORKLOAD)") $(if $(ALLOW_FULL),--allow-full)

bench:
	@mkdir -p .work/tmp
	python3 examples/bench_driver.py $(BENCH_ARGS)

bench-check:
	python3 examples/bench_driver.py $(BENCH_ARGS) --check

bench-list:
	python3 examples/bench_driver.py --list

bench-dry-run:
	python3 examples/bench_driver.py $(BENCH_ARGS) --dry-run

test:
	@mkdir -p .work/tmp
	@result=0; output=$$(TMPDIR="$(CURDIR)/.work/tmp" cargo run --quiet --locked -p jaq -- -n --to cbor 1 2>&1) || result=$$?; \
		if [ "$$result" -eq 2 ] && case "$$output" in *'Error: --to expects a data format '*) true;; *) false;; esac; \
		then :; else printf 'default CBOR rejection failed (exit %s): %s\n' "$$result" "$$output" >&2; exit 1; fi
	TMPDIR="$(CURDIR)/.work/tmp" cargo test --workspace --locked

clippy:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings

lint:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings

.PHONY: clean
clean:
	@if test -L ./target || { test -e ./target && ! test -d ./target; }; then \
	  printf '%s\n' 'make clean: ./target must be a local build directory' >&2; exit 1; \
	fi
	rm -rf -- ./target
