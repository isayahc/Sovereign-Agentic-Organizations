"""Project-local configuration and launcher for the official Cognee MCP server."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen
from urllib.parse import urlsplit

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


def configure() -> None:
    # Defaults < root .env < process environment < local Cognee overrides.
    values = dict(dotenv_values(ROOT / "config/cognee.env.example"))
    values.update(dotenv_values(ROOT / ".env"))
    values.update(os.environ)
    values.update(dotenv_values(ROOT / ".local/cognee.env"))
    os.environ.update({key: value for key, value in values.items() if value is not None})
    storage = ROOT / ".local/cognee"
    for name, directory in {
        "SYSTEM_ROOT_DIRECTORY": storage / "system",
        "DATA_ROOT_DIRECTORY": storage / "data",
    }.items():
        directory.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(directory)


def check_models() -> int:
    """Check model availability without loading a model or running inference."""
    missing = []
    for prefix in ("LLM", "EMBEDDING"):
        if os.environ.get(f"{prefix}_PROVIDER") != "ollama":
            print(f"{prefix}: non-Ollama profile; verify its provider separately.")
            missing.append(prefix)
            continue
        endpoint = urlsplit(os.environ[f"{prefix}_ENDPOINT"])
        url = f"{endpoint.scheme}://{endpoint.netloc}/api/tags"
        try:
            with urlopen(url, timeout=5) as response:
                models = {item["name"] for item in json.load(response)["models"]}
        except Exception as exc:
            print(f"{prefix}: Ollama availability check failed ({type(exc).__name__}).")
            missing.append(prefix)
            continue
        model = os.environ[f"{prefix}_MODEL"]
        present = model in models or f"{model}:latest" in models
        print(f"{prefix}: {model} - {'available' if present else 'missing'}")
        if not present:
            missing.append(prefix)
    return int(bool(missing))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    configure()
    if args.check:
        return check_models()
    executable = Path(sys.executable).parent / (
        "cognee-mcp.exe" if os.name == "nt" else "cognee-mcp"
    )
    if not executable.exists():
        print("Install requirements-cognee.txt in this Python environment first.", file=sys.stderr)
        return 1
    return subprocess.call([
        str(executable), "--transport", "http", "--host", "127.0.0.1",
        "--port", "8001", "--tool-mode", "all",
    ], cwd=ROOT / ".local/cognee")


if __name__ == "__main__":
    raise SystemExit(main())
