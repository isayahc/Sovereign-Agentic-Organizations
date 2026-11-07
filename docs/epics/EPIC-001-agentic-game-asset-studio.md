# EPIC-001: Launch the sovereign agentic game asset studio

**Status:** Planned

**Track:** Sovereign Agentic Organizations

**Concept:** Idea 2 — personalized, living gaming assets

**Priority:** MVP

**Product overview:** [README](../../README.md)

## Outcome

A client can commission a custom game prop from an agent-run studio, review a revision, receive an engine-importable package, and return for another asset that reflects remembered preferences. The studio can prepare the result for commercial delivery.

## Committed direction

- Use **Cognee** for persistent agent memory and client-style learning.
- Use the MCP implementation in **Mapped-Assembly/OpenForma** for the current design integration.
- Use **Superlinked** for the intended Generate & code, Search & retrieve, Read & structure, Decide & protect, and See & hear task areas, subject to interface/model verification.
- Start with a mechanical or hard-surface prop; define “living” as feedback-driven, versioned evolution for this release.

## Milestone 1 — Prove the integration path

### SAO-001: Establish the runtime and integration contracts

- [ ] Select the agent runtime and document local versus hosted components.
- [ ] Verify Cognee installation, persistence, and client-scoped retrieval.
- [ ] Connect to OpenForma MCP using the selected repository's integration documentation; record actual exposed tools and prerequisites.
- [ ] Verify the relevant Superlinked offering, interfaces, model support, and deployment requirements for all five task areas.
- [ ] Choose one target engine, asset category, and export format.
- [ ] Document setup, environment variables, and a repeatable smoke check.

**Acceptance:** A developer can reproduce connectivity checks for all three integrations. The capability matrix distinguishes verified support, required adapter work, and blockers. No integration is described as operational solely on the basis of sponsor notes.

### SAO-002: Validate OpenForma-to-game asset delivery

- [ ] Create one representative hard-surface prop through OpenForma MCP.
- [ ] Export it using a supported native CAD path and preserve its source project.
- [ ] Define conversion steps for scale, orientation, geometry budget, materials, and the chosen engine.
- [ ] Import the converted asset into the target engine and capture a preview.

**Acceptance:** One generated prop loads in the chosen engine at the documented scale and orientation. The source, export, conversion steps, and known limitations are recorded. Any unsupported step has an explicit implementation task before expanding asset scope.

**Dependencies:** SAO-001. This is the feasibility gate for the remaining production workflow.

## Milestone 2 — Learn the client and coordinate work

### SAO-003: Implement structured intake and style memory

- [ ] Define a brief containing client ID, asset purpose, style, references, technical constraints, and intended use.
- [ ] Implement Read & structure for briefs and revision requests.
- [ ] Implement See & hear for reference images; verify audio support and record any remaining audio blocker.
- [ ] Store preferences, references, feedback, and asset relationships in Cognee.
- [ ] Implement Search & retrieve over client-scoped context, with source references.

**Acceptance:** A second request recalls an explicitly stated preference from the first. Conflicting feedback updates the active preference while retaining its history. A second test client's retrieval does not expose the first client's private references or preferences.

**Dependencies:** SAO-001.

### SAO-004: Implement the studio coordinator

- [ ] Define logical coordinator, style, design, asset engineering, review, and commerce roles.
- [ ] Track jobs through intake, design, review, revision, packaging, and delivery.
- [ ] Record role handoffs, tool calls, output references, and failure reasons.
- [ ] Persist job state and support resuming a failed step without duplicating completed asset versions.
- [ ] Implement Decide & protect for task routing, client-context scope, and brief constraints.

**Acceptance:** A job has inspectable state and history from intake to delivery. A failed design or conversion step reports a useful error and can resume from the last completed stage.

**Dependencies:** SAO-001, SAO-003.

## Milestone 3 — Produce and evolve an asset

### SAO-005: Connect generation, review, and revision

- [ ] Implement Generate & code to turn the brief and recalled style into design instructions and required integration scripts.
- [ ] Execute supported design operations through OpenForma MCP.
- [ ] Reuse the conversion path from SAO-002 and produce a preview.
- [ ] Review the result against the brief and target-engine constraints.
- [ ] Accept client feedback, store it in Cognee, and create a linked asset revision.
- [ ] Record source provenance and declared usage rights for supplied references and reusable components.

**Acceptance:** A client can request a change and receive a new version linked to the original. Both versions have previews and source/export references. Review results identify whether the requested change and technical constraints were met.

**Dependencies:** SAO-002, SAO-003, SAO-004.

### SAO-006: Package and deliver

- [ ] Bundle the game-importable asset, preview, metadata, version history, and engine-import instructions.
- [ ] Include source project references and documented usage terms.
- [ ] Expose job status and deliverables through a minimal client-facing interface.
- [ ] Record delivery and client feedback for future orders.

**Acceptance:** A user can download the package and import it by following its instructions. The package identifies the client, job, asset version, format, and relevant usage terms.

**Dependencies:** SAO-005.

## Milestone 4 — Demonstrate an operating business

### SAO-007: Prepare the first commercial offer

- [ ] Choose a custom commission or reusable asset pack as the first offer.
- [ ] Generate a listing draft with previews, supported formats, usage terms, and a proposed price.
- [ ] Record production time and available compute/model costs per delivery.
- [ ] Offer the asset to a prospective customer and record the outcome.
- [ ] Track actual payment and delivery if a sale occurs.

**Acceptance:** An offer is ready to share with a customer and the production cost record is available. Revenue is reported only when a real payment is recorded; an unpaid demo remains an unpaid demo.

**Dependencies:** SAO-006.

### SAO-008: Assemble the track demo

- [ ] Show the agent organization and a job's role handoffs.
- [ ] Show a brief becoming a usable game prop through OpenForma MCP.
- [ ] Show feedback creating a revision and updating Cognee memory.
- [ ] Submit a second brief and demonstrate recalled style preferences.
- [ ] Show the five task areas, identifying their verified implementations or blockers.
- [ ] Show the downloadable package, commercial offer, costs, and any verified revenue.
- [ ] Document how to reproduce the demo and which services run locally.

**Acceptance:** The demo can be reproduced from the setup documentation and saved sample inputs, with evidence for each claimed capability.

**Dependencies:** SAO-006, SAO-007.

## Definition of done

- [ ] A complete brief-to-delivery workflow succeeds with real integration outputs.
- [ ] The delivered asset imports into the selected engine.
- [ ] Feedback produces a versioned revision and influences a subsequent request.
- [ ] Client-scoped memory and resumable failure handling are verified.
- [ ] All five task areas have recorded implementation evidence or explicit blockers; unresolved core integration blockers keep this epic open.
- [ ] Setup, integration contracts, limitations, and the demo are documented.
- [ ] A sale-ready offer exists, with revenue tracked separately from technical completion.

## Decisions to resolve during SAO-001

- Which game engine and asset format should the first delivery target?
- Which Superlinked interfaces provide each task area, and which require an application adapter or model backend?
- Which OpenForma exports and conversion tools meet the first asset's requirements?
- Where will clients submit briefs, preview revisions, and receive packages?
- What is the first commercial offer and its licensing model?

## Later extensions

Runtime-adaptive assets, animated characters, automatic marketplace publishing, broader asset categories, and multi-client production scheduling follow the initial validated workflow.
