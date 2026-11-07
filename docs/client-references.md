# Client reference ingestion

Run these commands from the repository root. The CLI stores immutable originals by client and SHA-256 under ignored `.local/client-references/`. SQLite holds revisions, descriptors, and SIE vectors. Each logical client/asset pair has a stable source ID for Cognee. The command prepares a design request for the existing OpenCode/OpenForma integration.

Start [SIE Local](https://github.com/superlinked/sie#quick-start) on Linux or WSL with Python 3.12 in its own virtual environment. The first embedding downloads MiniLM weights.

```sh
pip install 'sie-server[local]==0.11.0'
sie-server serve --host 127.0.0.1 --port 8080 --models sentence-transformers/all-MiniLM-L6-v2
```

Install the studio reader dependencies in the Python environment used for the following commands. Set `SIE_BASE_URL` to override the default loopback base URL. Only point it at a trusted server permitted to receive client descriptors.

```sh
python -m pip install -r requirements-references.txt
python scripts/client_references.py ingest style.md --client arcade --asset finish --source "Client style guide" --terms "Commission only" --description "Brushed brass enclosure" --allow-generation
python scripts/client_references.py design --client arcade --brief "Design a brushed brass enclosure" --limit 3
```

Supply a client-approved URL using `ingest --url URL` in place of the file and `--source`. The CLI saves the fetched bytes as a versioned snapshot. Use UTF-8 for text/HTML. PDFs contribute embedded text, PNG/JPEG contribute dimensions and color mode, OBJ contributes vertex/face counts, and STEP/STL contribute file metadata. Provide a short visual or design description for binary assets, scanned PDFs, or long documents. The MiniLM model has a 256-token context. Originals remain available to the design agent.

Only use `--allow-generation` when the stated terms permit generation. Re-ingest the same asset ID to replace bytes or revise terms. Omitting the flag revokes future selection; the previous approved revision cannot reappear in new searches. The CLI assumes a trusted local operator. Client selection scopes retrieval; it does not authenticate a caller.

The design command prints a manifest path. Inspect the brief, client, source IDs, SHA-256s, revisions, permissions, descriptors, and original paths. Add `--dispatch` to the design command to send a fresh request to the configured OpenCode design agent. Follow [physical design setup](physical-designs.md) first. The adjacent `opencode.log` records the agent output; inspect it for actual OpenForma tool calls and generated artifacts.

Run the local regression test with `python -m unittest discover -s tests`. Its HTTP fixture checks the SIE request contract and exercises the database and CLI without downloading weights.
