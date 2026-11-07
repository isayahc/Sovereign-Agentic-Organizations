# Cognee memory skeleton

OpenCode connects to the official **Cognee MCP 0.5.8** server at `http://127.0.0.1:8001/mcp`. One local HTTP server owns the embedded stores so multiple OpenCode sessions can share it without spawning competing database writers.

## Setup

```powershell
./scripts/setup-memory.ps1
./scripts/start-memory.ps1 -Check
./scripts/start-memory.ps1
```

Keep the server terminal open; use `opencode mcp list` in another terminal to check the connection. OpenCode watches `opencode.json`; `/reload` can force reconnection after the server starts. Stop the memory server with Ctrl+C.

The starter profile uses local Ollama for both graph extraction and embeddings:

- Chat: `qwen2.5:14b` (already present on the initial development machine).
- Embeddings: `nomic-embed-text:latest`, 768 dimensions.
- Storage: Cognee's embedded defaults under ignored `.local/cognee/`.
- Runtime: isolated `.local/cognee-venv/`, separate from OpenForma and Tinfoil dependencies.

Install any missing models before ingestion:

```powershell
ollama pull qwen2.5:14b
ollama pull nomic-embed-text:latest
```

The 14B model may spill into system RAM on the development laptop and run slowly. The starter does not run inference on launch. `-Check` only lists installed models; it does not prove extraction or retrieval quality. The first ingestion may also download tokenizer assets.

## Configuration

Defaults are in `config/cognee.env.example`. Optional overrides belong in ignored `.local/cognee.env`. Precedence is defaults, root `.env`, process environment, then local Cognee overrides. The launcher fixes data/system directories to this repository's `.local/cognee` so they are stable regardless of the calling directory. Keep secrets out of committed configuration.

The current Tinfoil Python client is independent of Cognee. A future Tinfoil-backed profile needs an attestation-verifying adapter or local Tinfoil proxy for the LLM and an explicitly configured embedding provider. Pointing Cognee directly at Tinfoil's public OpenAI-compatible URL does not reuse `inference.py` or its connection-time verification. MCP sampling is another future path, contingent on verified host support.

## OpenCode workflow

```text
/remember The selected track is Sovereign Agentic Organizations; Idea 2 is personalized evolving game assets.
/recall What track and idea did we choose?
```

The commands use the official `remember` and `recall` tools. `forget` and `cognify_status` are exposed as well; discover their actual schemas before calling them. For a long ingestion, use `background=true` and check `cognify_status` before claiming completion.

### Memory contract

| Dataset | Contents |
| --- | --- |
| `sao_project` | Track, technology choices, implementation decisions, verified setup results, and outstanding work. |
| `sao_client_<id>` | A particular client's style preferences, briefs, and feedback; use only when an explicit client ID is provided. |

Always specify `dataset_name` for writes and `datasets` for reads. Dataset names organize memory; they are **not tenant authorization boundaries**. This skeleton is a single trusted local-user workspace. Production client isolation requires separate authenticated backend users/processes or a tested permission layer.

Each memory summary should include:

- Kind: decision, preference, brief, feedback, or verification.
- Subject and explicit client/job/asset ID when relevant.
- Fact or preference, including units and constraints when present.
- Source: repository path, issue URL, or user statement; date.
- Status: planned, verified, or superseded; identify the prior decision when updating it.

Store concise durable facts. Read source files before seeding memory; never ingest the whole repository, `.env`, keys, or runtime folders. Retrieve relevant context before making a new decision; use current source code and explicit user corrections to resolve stale memories. Use `self_improvement=false` initially for predictable ingestion; this still builds permanent graph memory.

## Acceptance path

1. Install the server and verify OpenCode can discover its real memory tools.
2. Run `-Check`; install/configure missing chat and embedding models.
3. Store one non-sensitive project decision in `sao_project`.
4. Recall it with references from a second OpenCode session.
5. Restart the memory server and recall it again to demonstrate persistence.

Tool discovery alone is not a completed remember/recall test. Record failures and missing providers rather than presenting an unbuilt graph as working memory. Cognee, its transitive dependencies, and model assets need additional deployment hardening/locking before production use.

References: [MCP setup](https://docs.cognee.ai/cognee-mcp/mcp-local-setup), [memory tools](https://docs.cognee.ai/cognee-mcp/mcp-tools), [LLM providers](https://docs.cognee.ai/setup-configuration/llm-providers), [embeddings](https://docs.cognee.ai/setup-configuration/embedding-providers).
