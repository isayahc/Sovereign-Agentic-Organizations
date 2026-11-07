# Private inference with Tinfoil

The project's Python inference entry point uses `TinfoilAI`, the official Tinfoil SDK, with its default attestation verification and pinned/encrypted transport. It does not use a direct OpenAI-compatible URL that bypasses client-side verification.

## Setup

Use the Python environment from the design setup, or create it with `uv venv --python 3.12 --seed .local/venv`:

```powershell
uv pip install --python .local/venv/Scripts/python.exe -r requirements.txt
```

Store the credential only in the ignored root `.env` file:

```dotenv
TINFOIL_API_KEY=your-key-here
```

The module loads this file explicitly, without overwriting an existing environment variable. SDK 0.15.0 does not automatically read `TINFOIL_API_KEY`, so the wrapper assigns it to the SDK's underlying client after verified transport construction. No key is passed to the constructor or embedded in source. The wrapper also closes the client and disables automatic API retries.

## Make a verified inference call

```powershell
.local/venv/Scripts/python.exe inference.py
```

This sends one non-sensitive chat prompt to `gpt-oss-120b`, with automatic API retries disabled, and prints the response ID, model, text, and token usage. It exits nonzero on failure and does not print provider error bodies or credentials. A successful completion through the default SDK transport demonstrates a real inference request with SDK verification enabled; the generated text itself is not attestation evidence.

Reuse the client from application code:

```python
from inference import create_client

with create_client() as client:
    response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[{"role": "user", "content": "Summarize this design brief..."}],
    )
```

`complete(prompt)` is also available for short replies. The SDK exposes the usual OpenAI-compatible methods for custom request parameters.

This integration covers calls through this Python client. OpenCode's own model connection and the external OpenForma checkout retain their existing configuration.

References: [Python SDK](https://docs.tinfoil.sh/sdk/python-sdk), [models](https://docs.tinfoil.sh/models/chat), [verification](https://docs.tinfoil.sh/verification/verification-in-tinfoil).
