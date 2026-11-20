import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "examples/benches/upto.jq"
BINARY = ROOT / "target/release/jaq"
TIERS = {"edit": ("driver",), "change": ("upto",), "full": ("upstream",)}


def selection(tier, names):
    available = TIERS[tier]
    selected = tuple(names) if names else available
    if not selected or len(set(selected)) != len(selected) or any(name not in available for name in selected):
        raise ValueError(f"unknown workload for {tier}: {', '.join(selected)}")
    return selected


def preflight(selected):
    if "upto" in selected or "upstream" in selected:
        if not BINARY.is_file() or not os.access(BINARY, os.X_OK):
            raise ValueError("upto needs target/release/jaq: run cargo build --release --locked -p jaq")
        if not FIXTURE.is_file():
            raise ValueError(f"upto needs {FIXTURE}")
        inputs = [ROOT / "Cargo.lock", ROOT / "Cargo.toml"]
        inputs += [path for crate in ROOT.glob("jaq*") if crate.is_dir() for path in crate.rglob("*.rs")]
        inputs += [crate / "Cargo.toml" for crate in ROOT.glob("jaq*") if (crate / "Cargo.toml").is_file()]
        if any(path.stat().st_mtime > BINARY.stat().st_mtime for path in inputs):
            print("bench: warning: release binary may be stale; rebuild it before measuring", file=sys.stderr)
    if "upstream" in selected and sys.platform != "linux":
        raise ValueError("upstream needs Linux and GNU /usr/bin/time")
    if "upstream" in selected and (not shutil.which("timeout") or not Path("/usr/bin/time").is_file()):
        raise ValueError("upstream needs timeout and GNU /usr/bin/time")


def check_driver():
    if selection("edit", []) != ("driver",) or selection("change", ["upto"]) != ("upto",):
        raise ValueError("valid workload selection failed")
    for tier, names in (("edit", ["upto"]), ("change", ["missing"]), ("change", ["upto", "upto"])):
        try:
            selection(tier, names)
        except ValueError:
            continue
        raise ValueError(f"invalid selection accepted: {tier} {names}")
    validate_records('{"name":"upto","time":{"jaq":[0.1]}}', {"upto"})
    for content in ('', '{"name":"upto","time":{"jaq":[]}}'):
        try:
            validate_records(content, {"upto"})
        except ValueError:
            continue
        raise ValueError("incomplete benchmark results accepted")
    print("driver selection checks passed")


def validate_records(content, expected):
    records = [json.loads(line) for line in content.splitlines()]
    names = [record["name"] for record in records]
    if set(names) != expected or len(names) != len(expected) or any(not values or not all(isinstance(value, (int, float)) for value in values) for record in records for values in record["time"].values()) or any(not record["time"] for record in records):
        raise ValueError("missing or invalid workload results")


def run_upto():
    code = FIXTURE.read_text() + " | length"
    readiness = shutil.which("perf-gate-ready")
    before = subprocess.run([readiness], capture_output=True).returncode if readiness else None
    start = time.monotonic()
    result = subprocess.run([str(BINARY), code], input=b"8192\n", capture_output=True, timeout=30)
    elapsed = time.monotonic() - start
    after = subprocess.run([readiness, "-1"], capture_output=True).returncode if readiness and before == 0 else None
    if result.returncode != 0 or result.stdout != b"8193\n":
        raise ValueError(f"upto failed: exit {result.returncode}, stdout {result.stdout!r}, stderr {result.stderr!r}")
    directory = Path(tempfile.mkdtemp(prefix="bench-", dir=ROOT / ".work/tmp"))
    report = {"workload": "upto", "seconds": elapsed, "status": "ok", "host_ready_before": before, "host_ready_after": after, "performance_verdict": "not measured"}
    (directory / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({**report, "result": str(directory / "result.json")}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=TIERS, default="edit")
    parser.add_argument("--workload", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-full", action="store_true")
    args = parser.parse_args()
    if args.list:
        print("edit: driver (selection checks)\nchange: upto (array construction)\nfull: upstream (bench.sh; Linux, manual only)")
        return
    selected = selection(args.tier, args.workload)
    if args.tier == "full" and not args.allow_full:
        raise ValueError("full requires --allow-full")
    if args.dry_run:
        commands = {"driver": "internal selection checks", "upto": f"{BINARY} '<upto.jq> | length' < input 8192", "upstream": f"bash {ROOT / 'bench.sh'} {BINARY}"}
        for name in selected:
            print(f"{name}: {commands[name]}")
        return
    preflight(selected)
    if args.check:
        print(f"preflight passed: {', '.join(selected)}")
    elif selected == ("driver",):
        check_driver()
    elif selected == ("upto",):
        run_upto()
    elif selected == ("upstream",):
        directory = Path(tempfile.mkdtemp(prefix="bench-", dir=ROOT / ".work/tmp"))
        start = time.monotonic()
        with (directory / "upstream.log").open("w") as output:
            result = subprocess.run(["bash", str(ROOT / "bench.sh"), str(BINARY)], cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
        if result.returncode == 0:
            try:
                expected = {"empty", "bf-fib", "defs"} | {json.loads(line)["name"] for line in (ROOT / "examples/benches.json").read_text().splitlines() if line.strip() and not line.startswith("#")}
                validate_records((directory / "upstream.log").read_text(), expected)
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"upstream results are incomplete: {error}; see {directory / 'upstream.log'}") from error
        report = {"workload": "upstream", "seconds": time.monotonic() - start, "exit": result.returncode, "performance_verdict": "not measured"}
        (directory / "result.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({**report, "result": str(directory / "result.json")}))
        if result.returncode:
            raise ValueError(f"upstream failed with exit {result.returncode}; see {directory / 'upstream.log'}")
    else:
        raise ValueError("no workload selected")


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.SubprocessError, ValueError, AssertionError) as error:
        print(f"bench: {error}", file=sys.stderr)
        raise SystemExit(1)
