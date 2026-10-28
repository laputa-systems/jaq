.PHONY: clippy lint

clippy:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings

lint:
	@mkdir -p .work/tmp
	TMPDIR="$(CURDIR)/.work/tmp" cargo clippy --workspace --all-targets -- -D warnings
