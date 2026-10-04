"""Small client for any OpenAI-compatible chat API (stdlib only).

Environment variables:
  LLM_API_KEY    required
  LLM_BASE_URL   default: https://api.groq.com/openai/v1
  LLM_MODEL      default: openai/gpt-oss-120b  (free-tier model names change; verify)
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.groq.com/openai/v1")
MODEL = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b")


class LLMError(Exception):
    def __init__(self, code, body):
        super().__init__(f"LLM HTTP {code}: {body[:300]}")
        self.code, self.body = code, body


def chat(messages, temperature=0.0, retries=5):
    """Send messages, return the reply text. Retries on rate limits and server errors."""
    key = os.environ.get("LLM_API_KEY")
    if not key:
        raise SystemExit("Set LLM_API_KEY first (see README).")
    payload = json.dumps({"model": MODEL, "messages": messages,
                          "temperature": temperature}).encode()
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {key}",
               "User-Agent": "c-debug-assistant/0.1"}
    for attempt in range(retries):
        req = urllib.request.Request(BASE_URL + "/chat/completions",
                                     data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.load(resp)["choices"][0]["message"].get("content") or ""
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                wait = float(e.headers.get("retry-after", 2 ** attempt * 2))
                if wait > 120:  # e.g. daily quota: waiting will not help
                    raise LLMError(e.code, body)
                print(f"[llm] HTTP {e.code}, retrying in {min(wait, 60):.0f}s",
                      file=sys.stderr, flush=True)
                time.sleep(min(wait, 60))
                continue
            raise LLMError(e.code, body)
