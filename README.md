# jaq

![Build status](https://github.com/laputa-systems/jaq/actions/workflows/test.yml/badge.svg)
[![Crates.io](https://img.shields.io/crates/v/jaq-core.svg)](https://crates.io/crates/jaq-core)
[![Documentation](https://docs.rs/jaq-core/badge.svg)](https://docs.rs/jaq-core)

jaq (pronounced /ʒaːk/, like *Jacques*[^jacques]) is a clone of
the JSON data processing tool [`jq`](https://jqlang.github.io/jq/).
It has a few features not present in `jq`, such as
support for YAML, TOML, and XML.
CBOR is included only when the `jaq` binary is built with `--features cbor`.
jaq has an own [manual](https://gedenkt.at/jaq/manual/).
You can try jaq on the [playground](https://gedenkt.at/jaq/).

jaq is two things at a time:

- A command-line program, `jaq`, that can be used as drop-in replacement for `jq`.
- A library, [`jaq-core`](https://docs.rs/jaq-core/),
  that can be used to compile and run jq programs inside of Rust programs.
  Compared to the `jq` API, `jaq-core`
  can be safely used in multi-threaded environments and
  supports [arbitrary data types beyond JSON](https://docs.rs/jaq-core/latest/jaq_core/val/trait.ValT.html).

jaq focuses on three goals:

* **Correctness**:
  jaq aims to provide a more correct and predictable implementation of jq,
  while preserving compatibility with jq in most cases.
* **Performance**:
  I created jaq originally because I was bothered by
  [the long start-up time of jq 1.6](https://github.com/jqlang/jq/issues/1411),
  which amounts to about 50ms on my machine.
  This can be particularly seen when processing a large number of small files.
  Although the startup time has been vastly improved in jq 1.7,
  this tree does not repeat the upstream benchmark table.
  See [Performance](#performance).
* **Simplicity**:
  jaq aims to have a simple and small implementation, in order to
  reduce the potential for bugs and to
  facilitate contributions.

[^jacques]: I wanted to create a tool that should be discreet and obliging, like a good waiter.
  And when I think of a typical name for a (French) waiter, to my mind comes "Jacques".
  Later, I found out about the old French word *jacquet*, meaning "squirrel",
  which makes for a nice *ex post* inspiration for the name.
  And finally, the
  [Jacquard machine](https://en.wikipedia.org/wiki/Jacquard_machine)
  was an important predecessor of the modern computer,
  automating weaving with punched cards as early as 1804.



# Installation


## Binaries

This repository does not publish Windows builds.
The `release` workflow runs only when dispatched by hand.
It uploads pre-release zips named:

- `jaq-aarch64-apple-darwin.zip`
- `jaq-x86_64-unknown-linux-musl.zip`
- `jaq-aarch64-unknown-linux-musl.zip`

The tag is `release-<git sha>`.
GitHub's latest-release URL skips pre-releases, so it does not point at these tags.

[Homebrew](https://formulae.brew.sh/formula/jaq), `cargo install --locked jaq`, and the files on [01mf02/jaq releases](https://github.com/01mf02/jaq/releases) are upstream jaq, not this tree.

## From source

`rust-toolchain.toml` pins `nightly-2026-09-15`.
In this directory, `rustup` installs that compiler.

    $ cargo build --release --locked -p jaq
    $ cargo install --locked --path jaq

The binary is `target/release/jaq`.
Add `--features cbor` to either command to include CBOR.
Windows is not a supported target.



# Performance

[`bench.sh`](bench.sh) compares a jaq binary with jq and gojq.
The table that used to be here was measured on upstream jaq 3.0, which linked mimalloc.
This tree uses the system allocator and does not include that table.


# Security

jaq tries to guarantee that:

- It does not panic (except in cases of resource exhaustion, see below).
- It does not corrupt memory, i.e. it is memory-safe.
- It does not allow input data and jq filters to initiate I/O operations
  (except for reading files by jq filters before filter execution).

Any case where such a guarantee is broken is a bug and should be reported.

On the other hand,
jaq does not take countermeasures against any kind of resource exhaustion.
That means that jaq may take unlimited time, memory, or stack space.
For example, this may lead to stack overflows when:

- Reading input data: `jaq -nr 'repeat("[")' | jaq`
- Writing output data: `jaq -nc 'nth(1000000; recurse([.]))'`
- Running jq filters: `jaq -n 'def f: 1+f; f'`

jaq's core has been audited by
[Radically Open Security](https://www.radicallyopensecurity.com/)
as part of two [NLnet](https://nlnet.nl/) grants ---
thanks to both organisations for their support!
The
[first](https://github.com/01mf02/jaq/releases/download/v2.2.0/jaq.penetration.test.report.2025.1.0.pdf) and
[second](https://github.com/01mf02/jaq/releases/download/v3.0.0-gamma/NGICore.polyglot.jaq.penetration.test.report.2026.1.0.pdf)
security audit found several issues of moderate or low severity.
All issues in the security audits were addressed and
several fuzzing targets for jaq were added at `jaq-core/fuzz`.
Before that, jaq's JSON parser [hifijson](https://github.com/01mf02/hifijson/)
already disposed of a fuzzing target.
Finally, jaq disposes of a test suite of more than 500 tests.



# User Testimonials

> `jaq` is a well-built library that gave me a massive leg up compared to implementing `jq` support on my own. Extensibility through the `ValT` trait made adding `jq` support to my own types a breeze.
>
> @jobarr-amzn (<https://github.com/amazon-ion/ion-cli/pull/193#pullrequestreview-2696367084>, <https://github.com/01mf02/jaq/issues/355#issuecomment-3457076847>)

> My Rust program \[using jaq\] can execute *all queries* over *all files* **three times** while Python is busy executing *one* query across all files using the `jq` PyPI crate and a Python loop.
>
> @I-Al-Istannen (<https://github.com/01mf02/jaq/issues/323#issuecomment-3282176968>)

> jaq is very impressive! Running my [wsjq](https://github.com/thaliaarchi/wsjq) interpreter with it is significantly faster than with any other jq implementation and its emphasis on correctness is very admirable.
> \[On [wsjq benchmarks](https://github.com/01mf02/jaq/issues/294#issuecomment-3046707389), jaq is between 5 and 10 times faster than jq and between 15 and 196 times faster than gojq.\]
>
> @thaliaarchi (<https://github.com/01mf02/jaq/issues/355#issuecomment-3460028137>)

> I had been parsing data from certificate transparency logs using certstream-server. It gives a *lot* of data and piping it into jq was causing me issues. I switched to jaq and the faster startup time meant it could easily keep up on the low end VM I was using. Thank you for your work.
>
> Oliver (via e-mail)

Add your own testimonials via <https://github.com/01mf02/jaq/issues/355>.



# Acknowledgements

[This project](https://nlnet.nl/project/jaq/) was funded through the
[NGI0 Entrust](https://nlnet.nl/entrust) and
[NGI0 Commons](https://nlnet.nl/commonsfund) funds established by
[NLnet](https://nlnet.nl) with financial support from the
European Commission's [Next Generation Internet](https://ngi.eu)
programme, under the aegis of [DG Communications Networks, Content and Technology](https://commission.europa.eu/about-european-commission/departments-and-executive-agencies/communications-networks-content-and-technology_en) under
grant agreements
№ [101069594](https://cordis.europa.eu/project/id/101069594) and
№ [101135429](https://cordis.europa.eu/project/id/101135429).
Additional funding is made available by the
[Swiss State Secretariat for Education, Research and Innovation](https://www.sbfi.admin.ch/sbfi/en/home.html) (SERI).
