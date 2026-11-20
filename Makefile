.PHONY: clippy lint test

test:
	@mkdir -p .work/tmp
	@result=0; output=$$(TMPDIR="$(CURDIR)/.work/tmp" cargo run --quiet --locked -p jaq -- -n --to cbor 1 2>&1) || result=$$?; \
		if [ "$$result" -eq 2 ] && case "$$output" in 'Error: --to expects a data format '*) true;; *) false;; esac; \
		then :; else printf 'default CBOR rejection failed (exit %s): %s\n' "$$result" "$$output" >&2; exit 1; fi
	TMPDIR="$(CURDIR)/.work/tmp" cargo test --workspace --locked

clippy:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings

lint:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings
