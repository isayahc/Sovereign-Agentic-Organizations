# Sovereign Agentic Game Asset Studio

An agent-run creative studio pursuing paid commissions for custom game props and promotional trailers. A game developer can commission a prop with editable source and a Godot-ready model. A mystery-game publisher can commission a teaser for its next case. The studio uses its own sample work to find prospective buyers and show them what they could order.

**Hackathon track** · [Sovereign Agentic Organization · $2,750 prize](https://localhostai.nyc/tracks#organization)

**Commercial status** · The studio has produced sample work and researched seven prospective buyers. The documented trailer experiment ended before outreach. The first paid commission is still the goal. The repository records no customer payment.

## From a sample trailer to a first sale

1. **Make the sample.** For *The Last Light at Bellweather Pier*, the studio assembled five generated clips into a 75-second, 1080p mystery trailer and checked that the final MP4 decoded successfully.
2. **Find a buyer with a reason to buy.** OpenCode described scenes from the finished trailer. Superlinked SIE embedded the descriptions and buyer profiles. Local ranking surfaced mystery experiences, and research on official websites identified The Detective Society as a prospect because it already uses trailers for its mystery games. [Prospect research and render evidence](docs/video-prospecting-verification.md)
3. **Make an offer.** The proposed outreach workflow drafts a message offering a custom teaser for one of the prospect’s own cases. The operator reviews the recipient, sample and price, then explicitly authorizes sending through Playwright. The studio would record the actual submission outcome and any reply. [Outreach workflow design](docs/asset-prospecting-plan.md)
4. **Earn the first dollar.** For an accepted commission, agree on scope and price, collect payment and deliver the commissioned file. A redacted payment receipt showing amount and currency, linked to the order and delivery record, would substantiate a revenue claim.

## What the studio has produced

| Offer | Evidence |
| --- | --- |
| Custom hard-surface game prop | OpenCode used a client brief and a finish preference recalled through Cognee to produce a cobalt-blue industrial relay. A revision raised it from 29 to 46 mm and increased the cooling slots from four to six. Both GLBs imported in Godot. The verified delivery ZIP included editable sources, STEP, GLB, previews and import instructions. [Live prop verification](docs/live-client-prop-verification.md) |
| Custom promotional trailer | The Bellweather experiment produced a titled MP4, a technical verification record and seven sourced prospect profiles. The report includes the media checksum. The MP4 and one-off production scripts stayed on the operator’s machine. [Bellweather experiment](docs/video-prospecting-verification.md) |

## What the operator controls

| Workflow | Execution and dependencies |
| --- | --- |
| Prop production | OpenCode directs a local OpenForma MCP server. Native CAD tools compile the design and Godot validates the export. The operator keeps the editable source, revisions and delivery files. [Physical design setup](docs/physical-designs.md) |
| References and memory | Superlinked SIE Local embeds approved references. A local Cognee service stores and recalls preferences. The verified run used local models and required the runtime adjustments recorded in the [verification report](docs/live-client-prop-verification.md). |
| Trailer production and prospecting | The verified run relied on **GMI Cloud** for video generation. FFmpeg editing, SIE text embeddings, SQLite storage and Python ranking ran locally. A fully self-hosted trailer generation run remains to be demonstrated. |
| Optional hosted inference | Tinfoil provides a separate hosted model option with enclave verification. Operators can configure this integration independently of the local prop workflow. [Private inference setup](docs/private-inference.md) |

## Run the prop workflow

1. [Connect OpenCode to OpenForma and install the CAD tools](docs/physical-designs.md).
2. [Start Cognee](docs/memory.md) and [ingest approved client references with SIE Local](docs/client-references.md).
3. [Build and revise a game prop](docs/game-props.md), import it into Godot and inspect the delivery package.

The [studio epic](docs/epics/EPIC-001-agentic-game-asset-studio.md) covers the broader organization design. The [asset-to-prospect plan](docs/asset-prospecting-plan.md) describes how to turn the trailer experiment into a repeatable sales workflow.
