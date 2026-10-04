"""Propose a fix, verify it by compiling and running it, retry with the new diagnostics.

Usage: python agent.py path/to/file.c
"""
import os
import re
import sys
import tempfile

from llm import chat
from tools import check_program

SYSTEM = """You are a careful C debugging assistant. You receive a C program that fails \
(compile error, crash, sanitizer report, timeout, or wrong output) together with the diagnostics.
Find the root cause and return a corrected, complete program.

Rules:
- Make the smallest change that fixes the bug. Keep the program's purpose and output format.
- Never hard-code expected output. Never remove warnings, checks or sanitizers.
- Return the complete file, not a diff.

Reply in exactly this format:
EXPLANATION:
<2-4 sentences: what the bug is and why it happens>
FIXED_CODE:
```c
<complete corrected program>
```"""

_REPLY = re.compile(r"EXPLANATION:\s*(.*?)\s*FIXED_CODE:\s*```(?:c)?\s*\n(.*?)```", re.S)


def parse_reply(text):
    """Return (explanation, code), or None if the reply does not follow the format."""
    m = _REPLY.search(text or "")
    if not m or not m.group(2).strip():
        return None
    return m.group(1).strip(), m.group(2).rstrip() + "\n"


def _problem(code, first, expected=None):
    text = (f"Failing program:\n```c\n{code}```\n\n"
            f"Problem type: {first.status}\n{first.detail}")
    if expected is not None and first.status != "wrong_output":
        # wrong_output diagnostics already contain the expected text
        text += f"\n\nThe program should print exactly:\n{expected.strip()}"
    return text


def debug(source_path, first_result, expected=None, max_attempts=3, show_expected=False):
    """Try to fix a failing program. Returns a dict describing what happened.

    show_expected: also tell the model the correct output from the first message.
    """
    code = open(source_path, encoding="utf-8").read()
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": _problem(code, first_result,
                                         expected if show_expected else None)}]
    last = {"fixed": False, "attempts": 0, "explanation": "", "code": "", "last_status": "",
            "history": []}  # one entry per attempt, so no reasoning is lost
    for attempt in range(1, max_attempts + 1):
        reply = chat(messages)
        parsed = parse_reply(reply)
        last["attempts"] = attempt
        if parsed is None:
            last["history"].append({"attempt": attempt, "status": "bad_format"})
            messages += [{"role": "assistant", "content": reply},
                         {"role": "user", "content": "Wrong format. Use exactly the "
                          "EXPLANATION: / FIXED_CODE: format with one ```c block."}]
            last["last_status"] = "bad_format"
            continue
        explanation, fixed = parsed
        with tempfile.TemporaryDirectory() as d:
            candidate = os.path.join(d, "candidate.c")
            with open(candidate, "w", encoding="utf-8") as f:
                f.write(fixed)
            result = check_program(candidate, expected)
        last.update(explanation=explanation, code=fixed, last_status=result.status)
        last["history"].append({"attempt": attempt, "status": result.status,
                                "explanation": explanation})
        if result.passed:
            last["fixed"] = True
            return last
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": "That fix still fails.\n"
                      f"Problem type: {result.status}\n{result.detail}\n"
                      "Explain the real cause and return the complete corrected program."}]
    return last


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agent.py path/to/file.c")
    path = sys.argv[1]
    first = check_program(path)
    if first.passed:
        raise SystemExit("The program already compiles and runs cleanly.")
    print(f"Original problem: {first.status}\n{first.detail}\n")
    out = debug(path, first)
    if out["fixed"]:
        print(f"Fixed after {out['attempts']} attempt(s).\n\n{out['explanation']}\n\n{out['code']}")
    else:
        print(f"Could not fix it in {out['attempts']} attempts (last status: {out['last_status']}).")
