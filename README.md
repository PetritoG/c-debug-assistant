# C Debugging Assistant

A small command-line tool that uses an LLM to debug C programs. It sends the failing code and its
diagnostics (compiler errors, sanitizer reports, timeouts, or wrong output) to a model, asks for an
explanation and a fix, then **verifies the fix by recompiling and running it**. If the fix still
fails, the new diagnostics go back to the model for another attempt.

## How it works

1. `tools.py` compiles a program with `gcc -Wall -Wextra -Werror` plus AddressSanitizer and
   UndefinedBehaviorSanitizer (when available), runs it with a timeout, and classifies the outcome:
   `compile_error`, `runtime_error`, `timeout`, `wrong_output`, or `pass`.
2. `agent.py` asks the model for an explanation and a complete corrected file, checks it with
   `tools.py`, and retries up to 3 times using the new diagnostics.
3. `evaluate.py` runs the agent on 10 small buggy programs in `cases/` and reports how many were
   fixed and how many on the first attempt.

## Setup

Linux or WSL (Ubuntu) is recommended, because the sanitizers are needed to catch memory errors and
leaks. Plain Windows gcc builds usually cannot run them.

```
sudo apt install gcc python3
export LLM_API_KEY=...        # any OpenAI-compatible provider
# optional:
export LLM_BASE_URL=https://api.groq.com/openai/v1
export LLM_MODEL=openai/gpt-oss-120b
```

No third-party Python packages are required.

## Usage

```
python evaluate.py --selftest          # check the harness itself, no LLM needed
python evaluate.py                     # run the agent on all cases
python evaluate.py --case off_by_one   # run one case (or a prefix, e.g. --case hard_)
python agent.py path/to/file.c         # debug your own file (prints a fix, does not overwrite)
```

Run logs are saved to `runs/` (ignored by git).

## Benchmark cases

**Basic set (10 cases):** short programs with one classic bug each: off-by-one, null dereference,
memory leak, uninitialized variable, buffer overflow, wrong printf format, use after free, integer
division, double free, and an infinite loop.

**Hard set (10 cases, names start with `hard_`):** longer programs where the bug is subtler or
spread across functions: binary search boundary, word counting state, stack capacity check, linked
list head removal, rectangular matrix transpose, integer overflow with the wrong types, negative
modulo, `strtok` on a string literal, bank transfer state handling, and a sort tie-break. Four of
them produce no crash at all, only wrong output.

Every case has an `expected.txt` with the correct output. `reference_fix.c` files exist
only to validate the harness (`--selftest`); the model never sees them.

Which stage catches a bug depends on the compiler version. With recent gcc versions several bugs
are caught at compile time by `-Werror`.

## Results

20 cases, expected output hidden from the model, run on 2026-10-04.

| Model | Attempts allowed | Fixed | Fixed on the first attempt |
|---|---|---|---|
| gpt-oss-120b | 1 | 19/20 | 19/20 |
| gpt-oss-120b | 3 | 20/20 | 19/20 |
| gpt-oss-20b | 1 | about 17/20 | about 17/20 |
| gpt-oss-20b | 3 | 20/20 | 17/20 |

- Allowing up to 3 attempts, with the verification output fed back to the model, fixed every case
  for both models.
- First-attempt failures of the smaller model varied between identical runs, so its numbers are
  approximate.
- `null_deref` failed on the first attempt in almost every run. The reason is a test-specification
  issue: the model fixed the crash but guessed the wrong message text. When the expected output was
  shown to the model (`--show-expected`) it passed on the first attempt.
- The benchmark is small (20 programs), so differences between models are indicative only.

## Limitations

- Ten small, single-file programs: a demonstration benchmark, not a statistically meaningful one.
- For wrong-output bugs the model sees the expected output, so a determined model could in
  principle hard-code it. The prompt forbids this, and the tests only check stdout.
- Memory leaks and memory errors are only detected where sanitizers work.
- Only run code you wrote or trust; the tool compiles and executes it.

## Built with AI assistance

The first version of this code was written with help from Claude, then tested and iterated on by me.
