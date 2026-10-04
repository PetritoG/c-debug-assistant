"""Compile and run C programs for the debugging assistant.

Every program runs with a timeout. Only run code you wrote or trust.
"""
import os
import subprocess
import tempfile
from dataclasses import dataclass

CC = os.environ.get("CC", "gcc")
BASE_FLAGS = ["-std=c11", "-O1", "-g", "-Wall", "-Wextra", "-Werror"]
# -fno-sanitize-recover makes undefined behavior abort the program instead of just printing.
SAN_FLAGS = ["-fsanitize=address,undefined", "-fno-sanitize-recover=undefined",
             "-fno-omit-frame-pointer"]
COMPILE_TIMEOUT = 30
RUN_TIMEOUT = 5
MAX_DETAIL_CHARS = 3000  # keep diagnostics short enough to send to the model

_sanitizers_ok = None


@dataclass
class Result:
    status: str   # pass | compile_error | runtime_error | timeout | wrong_output
    detail: str = ""
    stdout: str = ""

    @property
    def passed(self):
        return self.status == "pass"


def _trim(text):
    text = text.strip()
    if len(text) > MAX_DETAIL_CHARS:
        return text[:MAX_DETAIL_CHARS] + "\n...[truncated]"
    return text


def _run(cmd, timeout, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, cwd=cwd)


def sanitizers_available():
    """True if the compiler can build and run a program with ASan + UBSan.

    Many Windows gcc builds (MinGW) cannot. Use WSL or Linux for full checks.
    """
    global _sanitizers_ok
    if _sanitizers_ok is None:
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "probe.c")
            exe = os.path.join(d, "probe.exe" if os.name == "nt" else "probe")
            with open(src, "w") as f:
                f.write("int main(void) { return 0; }\n")
            try:
                c = _run([CC, *SAN_FLAGS, src, "-o", exe], COMPILE_TIMEOUT)
                _sanitizers_ok = c.returncode == 0 and _run([exe], 10).returncode == 0
            except (OSError, subprocess.TimeoutExpired):
                _sanitizers_ok = False
    return _sanitizers_ok


def check_program(source_path, expected=None):
    """Compile and run source_path. If expected is given, stdout must match it."""
    flags = BASE_FLAGS + (SAN_FLAGS if sanitizers_available() else [])
    with tempfile.TemporaryDirectory() as d:
        exe = os.path.join(d, "prog.exe" if os.name == "nt" else "prog")
        try:
            c = _run([CC, *flags, source_path, "-o", exe, "-lm"], COMPILE_TIMEOUT)
        except FileNotFoundError:
            raise SystemExit(f"Compiler '{CC}' not found. Install gcc (or set CC).")
        except subprocess.TimeoutExpired:
            return Result("compile_error", "Compilation timed out.")
        if c.returncode != 0:
            return Result("compile_error", _trim(c.stderr))
        try:
            r = _run([exe], RUN_TIMEOUT, cwd=d)
        except subprocess.TimeoutExpired:
            return Result("timeout", f"The program did not finish within {RUN_TIMEOUT}s "
                                     "(possible infinite loop).")
        if r.returncode != 0:
            return Result("runtime_error",
                          f"exit code {r.returncode}\n{_trim(r.stderr)}", r.stdout)
        if expected is not None and r.stdout.strip() != expected.strip():
            return Result("wrong_output",
                          f"expected stdout:\n{expected.strip()}\n\nactual stdout:\n{r.stdout.strip()}",
                          r.stdout)
        return Result("pass", "", r.stdout)
