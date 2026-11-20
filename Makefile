.PHONY: clippy lint test

test:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo test --workspace --locked

clippy:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings

lint:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings
