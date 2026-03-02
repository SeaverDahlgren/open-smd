#!/usr/bin/env python3
"""
Minimal terminal chatbot with conversational context.

Requirements:
- Python 3.8+
- GEMINI_API_KEY environment variable set
"""

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Dict, List

SYSTEM_PROMPT = "You are a concise, helpful assistant in a terminal chatbot."
DEFAULT_MODEL = "gemini-2.5-flash"

def call_gemini(
    api_key: str, model: str, messages: List[Dict[str, str]], system_prompt: str
) -> str:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    # Convert chat history into Gemini message format.
    contents = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        parsed = json.loads(raw)

    candidates = parsed.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"No candidates returned: {parsed}")

    parts = candidates[0].get("content", {}).get("parts", [])
    text_chunks = [p.get("text", "") for p in parts if isinstance(p, dict)]
    answer = "".join(text_chunks).strip()
    if not answer:
        raise RuntimeError(f"Empty text response: {parsed}")
    return answer


def main() -> int:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return 1

    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    messages = []

    print(f"Terminal chatbot running with model: {model}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return 0

        if not user_input:
            continue

        # Add the latest user turn; prior turns remain in `messages` for context.
        messages.append({"role": "user", "content": user_input})

        try:
            assistant_text = call_gemini(
                api_key=api_key,
                model=model,
                messages=messages,
                system_prompt=SYSTEM_PROMPT,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"Assistant> Gemini API error ({exc.code}): {body}")
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"Assistant> Error calling model: {exc}")
            continue

        print(f"Assistant> {assistant_text}\n")
        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    sys.exit(main())
