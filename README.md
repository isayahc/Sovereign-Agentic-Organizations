# Sovereign Agentic Game Asset Studio

An agent-run studio that creates personalized, evolving game assets, learns each client's style, and works toward selling custom assets and reusable asset packs.

**Track:** Sovereign Agentic Organizations

**Selected concept:** [Idea 2](docs/idea.md)

**Status:** Initial local OpenCode/OpenForma design integration; the studio workflow is planned.

## Vision

Build a small creative company operated by collaborating agents: understand a client, design an asset, refine it through feedback, package it for use, and prepare it for sale. Clients retain control of their creative context, and the organization improves through shared memory.

For the initial MVP, **living assets** means versioned assets that evolve with client preferences and feedback. Runtime adaptation inside a game is a future extension.

## Goals

- Generate custom gaming assets from a client's brief and references.
- Learn and recall each client's visual style across requests.
- Coordinate specialized agents around a shared production workflow.
- Deliver usable assets with previews, version history, and integration instructions.
- Prepare saleable assets and test demand through a real customer commission or asset-pack sale.
- Prefer local or self-hosted execution where supported, with explicit documentation of external dependencies.

## Selected technology

| Technology | Intended role |
| --- | --- |
| **Cognee** | Required memory layer: connect briefs, style preferences, references, assets, and feedback in shared agent memory. Keep client-specific context scoped to its owner. |
| **[OpenForma MCP](https://github.com/Mapped-Assembly/OpenForma)** | Current design integration, replacing the earlier generic Forma-OSS reference. Agents use its MCP interface to author and refine supported designs and obtain exportable artifacts. |
| **Superlinked** | Planned support for the five task areas below, with model/runtime selection and supported interfaces confirmed during integration discovery. |

OpenForma currently describes a hardware/CAD design platform with supported native CAD exports including OBJ. The first asset experiment will be a mechanical or hard-surface game prop. Game-ready topology, materials, scale, and engine import require a separate validation and conversion step. Supported motion previews do not by themselves establish game-ready animation support.

### Superlinked task areas

These are the capabilities we intend to implement; exact Superlinked products, model support, and integration boundaries remain to be verified against the [sponsor notes](docs/sponsors/SuperLinked.md) and official documentation.

| Task | Studio responsibility | Expected output |
| --- | --- | --- |
| **Generate & code** | Turn structured briefs into design instructions and supporting game-integration code. | Design requests, asset metadata, and integration scripts. |
| **Search & retrieve** | Find relevant client preferences, prior assets, references, and reusable components. | Ranked context with source references. |
| **Read & structure** | Convert client requests, documents, and feedback into consistent requirements. | Structured briefs, constraints, and revision requests. |
| **Decide & protect** | Select next actions, check requirements and usage rights, and enforce client-context boundaries. | Routing decisions and recorded review results. |
| **See & hear** | Interpret visual references and, when supported, spoken briefs or audio references. | Style observations and structured multimodal input. |

Cognee owns persistent relationship-based memory; the retrieval and task-execution integration should reuse that context rather than create competing sources of truth.

## Agent organization

| Role | Responsibility |
| --- | --- |
| Studio coordinator | Track an order, assign work, and move it through production. |
| Client and style agent | Structure requests and recall the client's preferences through Cognee. |
| Design agent | Translate the brief into OpenForma MCP design operations and revisions. |
| Asset engineer | Convert supported exports, validate engine compatibility, and package deliverables. |
| Review agent | Check style fit, technical requirements, source provenance, and client isolation. |
| Commerce agent | Draft previews, product descriptions, pricing proposals, and delivery records. |

These are logical responsibilities; the MVP can implement several roles in one runtime.

## Initial customer journey

1. A client submits a brief and optional reference images.
2. The studio structures the request and retrieves relevant style memory.
3. The coordinator creates an asset job and delegates design work through OpenForma MCP.
4. The asset engineer prepares a preview and a supported game-importable export.
5. The client gives feedback; the studio records it in Cognee and produces a revision.
6. The studio delivers a versioned asset package and drafts a sale listing where appropriate.
7. A later request reuses the learned preferences to produce a more personalized result.

## MVP scope and success criteria

- One client, one hard-surface asset category, and one selected game engine/export target.
- One end-to-end job from brief to engine-importable asset and downloadable package.
- A second request demonstrates recall of style preferences from the first.
- Agent handoffs, tool results, revisions, and job status are inspectable.
- Each of the five task areas has a demonstrated path or an explicitly documented integration blocker.
- One listing or commission offer is ready; a first paid delivery is the business validation goal.

## Implementation plan

The [Cognee memory skeleton](docs/memory.md) connects OpenCode to a local memory server and adds `/remember` and `/recall` commands for project decisions and future client-style memory.

Private model calls are available through the [Tinfoil Python integration](docs/private-inference.md), using `gpt-oss-120b` and the SDK's automatic enclave verification.

See [EPIC-001: Launch the sovereign agentic game asset studio](docs/epics/EPIC-001-agentic-game-asset-studio.md) for work items, dependencies, acceptance criteria, and the demo sequence.

Start with [physical design setup](docs/physical-designs.md) to connect OpenCode to the local OpenForma MCP and install the native CAD tools. Cognee's initial skeleton is available above; end-to-end memory validation, Superlinked, and the studio application remain planned.

## Project references

- [Track notes](Tracks.md)
- [Original ideas](docs/idea.md)
- [Cognee notes](docs/sponsors/Cognee.md)
- [Superlinked notes](docs/sponsors/SuperLinked.md)
- [OpenForma repository](https://github.com/Mapped-Assembly/OpenForma)
- [OpenForma agent integration documentation](https://github.com/Mapped-Assembly/OpenForma/blob/main/docs/agent-clients.md)

Use [client reference ingestion](docs/client-references.md) to index approved source material through SIE Local and pass versioned references to the OpenForma design workflow.

[Build and revise a game prop](docs/game-props.md) using the same client handoff, local OpenForma MCP, and a Godot-verified delivery package.
