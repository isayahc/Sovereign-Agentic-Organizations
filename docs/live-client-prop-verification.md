# Live verification: client references and game props

Completed on 2026-11-07 against `bb62511` (merged implementation of issues #5 and #6).
Fresh client/run ID: `relay-live-fa4306a32d2a`.

## Results

| Stage | Result | Evidence |
| --- | --- | --- |
| SIE embedding and reference ingestion/retrieval | PASS | Real 384-dimensional embeddings; generation-approved source and immutable original retained |
| Duplicate, revision and client isolation controls | PASS | Unchanged ingestion created no revision; replacement advanced revision; other-client references excluded |
| Cognee permanent remember/recall | PASS | Preference recalled over a separate MCP connection with source references |
| Fresh recipe and native OpenForma compilation | PASS | Both versions compiled through live local MCP under one fresh project |
| Godot import and validation | PASS | Dimensions, material, triangle count and floor pivot measured in Godot |
| Exported geometry and previews | PASS | Four versus six slots independently measured from GLB ray intersections; both previews visually inspected |
| Delivery | PASS | Fresh ZIP extracted; artifact hashes and native STEP headers checked |

No fixture encoder, copied sample ZIP, or manually substituted recalled preference was used.
The `/game-prop` instructions were followed in OpenCode. The unchanged
`scripts/build_game_prop.py` ran through a logging-only wrapper preserving compiler responses.

## Inputs and provenance

Brief:

> Design a 92 × 64 mm industrial field relay for a maintenance game. Give it a mounting flange, four corner bolt heads, a raised dial, and four cooling slots. The finished prop should be 29 mm tall.

Separate Cognee preference:

> Use a satin cobalt-blue finish.

The finish was absent from the brief and retrieved request. The recipe preference
was extracted from actual Cognee recall.

Revision feedback:

> Raise the dial so the prop is 46 mm tall and add two cooling slots. Keep the footprint and finish.

- SIE Local `0.11.0`, Ubuntu WSL, CPU PyTorch `2.9.1+cpu`.
- Model: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- Reference source: `9cf2d328-42f4-537d-a7ed-46ba6de24d06`, revision `1`.
- Reference SHA-256: `64f864e4ab22bf281b6c0aa7ab85f2e2bf4340f2881c846b4d962a953adacc76`.
- Cognee dataset: `sao_client_relay-live-fa4306a32d2a`.
- Recall data ID: `655172f0-c661-435b-8bf1-54a494546cfe`.
- Recall document: `text_2cf787738c0a62d4a2611ec436604a49`.
- OpenForma project: `93eaf141-53d0-44f6-b305-337df1bd297c`.

## Measurements

Godot `4.6.3.stable.official.7d41c59c4` imported and instantiated both GLBs.
Godot uses meters with Y up; CAD uses millimeters with Z up.

| Measurement | v1 | v2 |
| --- | --- | --- |
| Godot X size (m) | 0.0920000001788139 | 0.0920000001788139 |
| Godot Y size (m) | 0.028999999165535 | 0.046000000089407 |
| Godot Z size (m) | 0.0640000030398369 | 0.0640000030398369 |
| Floor Y (m) | 0 | 0 |
| Triangles (budget 5,000) | 3,196 | 3,228 |
| Cooling slots (GLB ray inspection) | 4 | 6 |
| Watertight mesh | Yes | Yes |
| Material | SatinCobaltBlue | SatinCobaltBlue |
| Imported sRGB | 0047ab | 0047ab |
| Metallic | 0.200000002980232 | 0.200000002980232 |
| Roughness | 0.479999989271164 | 0.479999989271164 |

The numeric interpretation of satin cobalt-blue (`#0047AB`, metallic `0.20`,
roughness `0.48`) is an explicit author assumption, not additional client data.
Slot counts were measured independently from the exported meshes, not by Godot
or solely by counting recipe operations.

## Recovered failures

- SIE returned `HTTP Error 503: Service Unavailable` during initial model loading.
  Retrying after weights loaded succeeded.
- Cognee's embedding connection test timed out after 30 seconds. Installed
  `nomic-embed-text:latest` and independently verified a real 768-dimensional embedding.
- Cognee's LLM connection test timed out after 30 seconds. Direct `qwen2.5:14b`
  warmup failed with `llama runner process has terminated: exit status 2`.
  A CPU-only alias `sao-live-qwen-coder` derived from `qwen2.5-coder:7b` succeeded.
- LanceDB failed to persist a temporary file in the deep Windows storage path:
  `The system cannot find the path specified. (os error 3)`.
  An isolated Cognee MCP on port `8002`, shorter `.local/cg-fa4306` storage,
  and `ENABLE_BACKEND_ACCESS_CONTROL=false` allowed permanent ingestion and recall.
  The original port `8001` service/store was preserved.
- `COGNEE_SKIP_CONNECTION_TEST=true` bypassed the cold-start probe only after
  independent real chat and embedding checks; actual graph extraction and recall ran.
- The delivery builder omitted the workspace-root `forma-project.json`.
  Persisting the actual v2 compiler response with the upstream manifest helper
  restored `forma-oss status` to `Validation: ok`.

No blockers remained for this run. These were local runtime adjustments and a
manifest recovery, not committed implementation fixes. The pass does not imply
that the default setup works without those adjustments. Client dataset labels
remain organizational labels in the single-user skeleton, not tenant isolation.

## Local artifacts

All paths below are relative to the repository root on the test machine.
Ignored runtime artifacts are not included in this commit.

- ZIP: `.local/relay-live-fa4306a32d2a/delivery.zip`
- v1 preview: `.local/relay-live-fa4306a32d2a/inspected-delivery/v1/preview.png`
- v2 preview: `.local/relay-live-fa4306a32d2a/inspected-delivery/v2/preview.png`
- Detailed report: `.local/relay-live-fa4306a32d2a/run-report.md`
- Machine-readable report: `.local/relay-live-fa4306a32d2a/run-report.json`
- Request: `.local/relay-live-fa4306a32d2a/references/handoffs/102668f9edd649158e9cc6ae0fbbe9c8/request.json`
- Recall: `.local/relay-live-fa4306a32d2a/cognee-recall.json`
- Compiler responses: `.local/relay-live-fa4306a32d2a/openforma-v1-response.json`
  and `.local/relay-live-fa4306a32d2a/openforma-v2-response.json`
- Geometry inspection: `.local/relay-live-fa4306a32d2a/geometry-inspection.json`

ZIP SHA-256: `f19831b596128907913ac50c3c33cb096b0b01cfd03d49fc5eac061f258d089e`.
The ZIP includes both revisions' editable IR and model sources, STEP, GLB, PNG,
Godot measurements, recipe, manifest, and import instructions.
