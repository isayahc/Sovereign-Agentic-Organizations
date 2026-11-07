"""Exercise the actual CLI and SQLite store with a controlled SIE HTTP endpoint."""

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "client_references.py"


class Encoder(BaseHTTPRequestHandler):
    """Serve a deterministic embedding in SIE's OpenAI-compatible response shape."""

    def do_POST(self) -> None:
        """Check the model contract and encode the submitted text."""
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path != "/v1/embeddings" or payload["model"] != "sentence-transformers/all-MiniLM-L6-v2":
            self.send_error(400)
            return
        text = payload["input"].lower()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"data": [{"embedding": [1, text.count("brass"), text.count("wood")]}]}).encode())

    def log_message(self, format: str, *args: object) -> None:
        """Keep fixture HTTP access logs out of test output."""


class ReferenceTests(unittest.TestCase):
    """Check client isolation, versioning, usage changes, and the generation handoff."""

    def test_workflow(self) -> None:
        """Run concurrent ingestion, update a reference, then query and revoke it."""
        with tempfile.TemporaryDirectory() as folder, ThreadingHTTPServer(("127.0.0.1", 0), Encoder) as server:
            threading.Thread(target=server.serve_forever, daemon=True).start()
            self.addCleanup(server.shutdown)
            root = Path(folder)
            env = dict(os.environ, SIE_BASE_URL=f"http://127.0.0.1:{server.server_port}")

            def run(*args: str) -> dict:
                """Run a fresh process to verify restart persistence and CLI output."""
                output = subprocess.check_output([sys.executable, str(SCRIPT), "--store", str(root / "index"),
                                                  *args], env=env, text=True)
                return json.loads(output)

            file = root / "style.md"
            file.write_text("wood finish", encoding="utf-8")
            common = ["ingest", str(file), "--asset", "finish", "--source", "client brief", "--terms", "commission"]
            a = [*common, "--client", "a", "--allow-generation"]
            with ThreadPoolExecutor(max_workers=2) as pool:
                first, duplicate = pool.map(lambda _: run(*a), range(2))
            self.assertEqual(sorted([first["changed"], duplicate["changed"]]), [False, True])
            other = run(*common, "--client", "b", "--allow-generation")
            self.assertNotEqual(first["source_id"], other["source_id"])
            file.write_text("brass finish", encoding="utf-8")
            revision = run(*a)
            self.assertEqual((revision["source_id"], revision["revision"]), (first["source_id"], 2))
            design = ["design", "--client", "a", "--brief", "brass prop"]
            manifest = Path(run(*design)["manifest"])
            refs = json.loads(manifest.read_text())["references"]
            self.assertEqual([(x["client"], x["revision"]) for x in refs], [("a", 2)])
            self.assertEqual(Path(refs[0]["original"]).read_bytes(), b"brass finish")
            run(*common, "--client", "a")
            with self.assertRaises(subprocess.CalledProcessError):
                run(*design)
