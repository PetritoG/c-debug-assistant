"""Run the benchmark of buggy C programs.

  python evaluate.py --selftest     check the harness itself (no LLM needed)
  python evaluate.py                run the agent on every case
  python evaluate.py --case NAME    run cases whose name starts with NAME (e.g. hard_)
  python evaluate.py --show-expected   also give the model the correct output up front
"""
import argparse
import json
import pathlib
import time

from agent import debug
from tools import check_program, sanitizers_available

CASES_DIR = pathlib.Path(__file__).parent / "cases"
RUNS_DIR = pathlib.Path(__file__).parent / "runs"


def load_cases(only=None):
    cases = []
    for d in sorted(CASES_DIR.iterdir()):
        if d.is_dir() and (only is None or d.name.startswith(only)):
            cases.append((d.name, d, (d / "expected.txt").read_text()))
    if not cases:
        raise SystemExit(f"No case found{' starting with ' + only if only else ''}.")
    return cases


def selftest():
    """Every buggy program must fail its check; every reference fix must pass."""
    print(f"sanitizers available: {sanitizers_available()}")
    bad = 0
    for name, d, expected in load_cases():
        buggy = check_program(str(d / "buggy.c"), expected)
        ref = check_program(str(d / "reference_fix.c"), expected)
        ok = (not buggy.passed) and ref.passed
        bad += not ok
        note = "" if ok else f"  <-- buggy: {buggy.status}, reference: {ref.status}"
        print(f"{'OK  ' if ok else 'FAIL'} {name:22} buggy -> {buggy.status}{note}")
    if bad:
        print(f"\n{bad} case(s) behave unexpectedly. Leaks and memory errors are only "
              "detected with sanitizers (Linux/WSL).")
    return 1 if bad else 0


def run(only=None, attempts=3, show_expected=False):
    RUNS_DIR.mkdir(exist_ok=True)
    out_path = RUNS_DIR / f"{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    fixed = first_try = total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for name, d, expected in load_cases(only):
            src = str(d / "buggy.c")
            before = check_program(src, expected)
            if before.passed:
                print(f"SKIP {name}: the buggy program already passes (run --selftest)")
                continue
            total += 1
            res = debug(src, before, expected, attempts, show_expected)
            fixed += res["fixed"]
            first_try += res["fixed"] and res["attempts"] == 1
            print(f"{'FIXED' if res['fixed'] else 'FAIL '} {name:22} "
                  f"({before.status}) attempts={res['attempts']}")
            f.write(json.dumps({"case": name, "problem": before.status,
                                "show_expected": show_expected, **res}) + "\n")
            f.flush()
    mode = "expected output shown" if show_expected else "expected output hidden"
    print(f"\nfixed {fixed}/{total} ({first_try} on the first attempt), {mode}. Log: {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--case")
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--show-expected", action="store_true",
                    help="tell the model the correct output from the first message")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    run(args.case, args.attempts, args.show_expected)
