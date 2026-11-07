"""Private inference through Tinfoil's attestation-verifying Python SDK."""

import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from tinfoil import TinfoilAI

DEFAULT_MODEL = "gpt-oss-120b"


@contextmanager
def create_client():
    """Load project-local credentials and keep SDK verification enabled."""
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    if not os.environ.get("TINFOIL_API_KEY", "").strip():
        raise RuntimeError("Set TINFOIL_API_KEY in the project .env file.")
    client = TinfoilAI(timeout=120.0)
    # SDK 0.15.0 does not yet load TINFOIL_API_KEY itself. Configure its
    # underlying OpenAI client after the verified transport is constructed.
    client.client.api_key = os.environ["TINFOIL_API_KEY"]
    client.client.max_retries = 0
    try:
        yield client
    finally:
        client.client.close()


def complete(prompt: str):
    """Return an OpenAI-compatible completion using the verified transport."""
    with create_client() as client:
        return client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            reasoning_effort="low",
            max_tokens=256,
        )


def main() -> int:
    """Make one real request with a non-sensitive connectivity-test prompt."""
    try:
        response = complete("Reply with exactly: Tinfoil integration works.")
        text = response.choices[0].message.content if response.choices else None
        if not text or not text.strip():
            raise RuntimeError("The completion did not contain a text response.")
    except Exception as exc:
        # Avoid logging request headers, credentials, or provider error bodies.
        print(f"Tinfoil smoke test failed ({type(exc).__name__}).", file=sys.stderr)
        return 1
    print(json.dumps({
        "id": response.id,
        "model": response.model,
        "response": text,
        "usage": response.usage.model_dump() if response.usage else None,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
