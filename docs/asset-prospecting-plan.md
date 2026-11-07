# Generalize asset creation into prospect discovery

**Status: proposed, not implemented.** Grounded in the
[Bellweather experiment](video-prospecting-verification.md). This expands the
studio's commerce workflow without replacing the game-prop production path.

## Goal

Given an existing asset or a production brief, OpenCode should deliver a validated
asset package, an evidence-backed semantic profile, a researched prospect list,
and a suitable offer. A subsequent outreach task should use the user's identity
and chosen channels and record the actual result.

Distinguish three commercial outcomes:

- **License this asset:** an identified buyer can use the existing work and its
  available usage terms fit the proposed use.
- **Commission similar work:** the asset demonstrates a capability, but the buyer
  needs a different story, product, branding or format.
- **Production partnership:** the organization already provides related services;
  investigate subcontracting demand rather than labeling it a direct buyer.

Bellweather currently supports the second outcome. Semantic similarity alone
cannot establish any of them as a sale.

## Proposed pipeline

1. **Brief/import:** assign stable job and asset IDs; record client, source,
   intended use, budget, desired format and whether creation or analysis is asked for.
2. **Produce:** discover provider capabilities and exact model schema, estimate
   the requested settings, retain the spending decision, submit once and persist
   each request ID. Resume status checks after interruption; reconcile ambiguous
   submissions before creating another charge.
3. **Validate:** download to temporary files, finalize on success, preserve source
   clips, hash the final deliverable, probe it and decode it. Record technical and
   human-review results separately. Never silently claim requested resolution or
   duration was actually delivered without measurement.
4. **Observe:** extract timestamped frames and available text/audio. Distinguish
   observed content, source captions, supplied story context and inferred themes.
   A still frame cannot establish a motion event; a script is not proof that a
   generated shot contains that action.
5. **Embed/index:** select an appropriate live encoder, chunk by actual tokenizer
   limits, retain exact inputs and model revision, and persist vectors. Start with
   the proven SIE text route; add direct image/video/audio models only after verifying
   their interfaces and running a genuine workload.
6. **Match/research:** rank a broad candidate set; research official websites;
   add new categories when results warrant it. Save source excerpts and retrieval
   dates. Separate semantic resemblance from purchasing evidence and contactability.
7. **Prepare an offer:** identify license/custom/partner route, adaptation work,
   relevant decision-making role, public business contact and a tailored pitch.
8. **Contact/track:** when asked to contact named prospects, use Playwright with
   the user's supplied business identity, portfolio and message instructions.
   Record recipient, message, channel and observed outcome; deduplicate follow-ups.

## Proposed records

Use versioned JSON records with IDs linking them; keep derived data tied to the
asset hash. The field groups below are a design contract, not a shipped schema.

| Record | Minimum fields |
| --- | --- |
| Asset | `schema_version`, `asset_id`, `job_id`, `client_id`, `path`, `sha256`, `media_type`, measured dimensions/duration, provenance, usage terms |
| Generation | Provider/model/revision, exact prompt/settings, estimate and approval, request ID, state, output paths/hashes, error and final charge if reported |
| Observation | `asset_id`, asset hash, time range, extraction method/model, source frame/text references, observation text, inference flag, review status |
| Embedding | Observation/profile ID, text hash, encoder/revision, dimension, chunk/token metadata, vector, creation time |
| Prospect | Stable organization/domain ID, evidence text and URL, retrieval date, public contact source, role, candidate category, qualification status |
| Match | Asset/profile versions, raw score/components, scoring version, supporting scenes, commercial route, rationale and disqualifiers |
| Outreach | Prospect/job IDs, user business identity reference, message version, channel, attempt ID, timestamp, observed status, receipt/evidence and follow-up state |

Credentials belong in provider auth storage or environment configuration, not
these records. Large media, vectors, browser captures and contact attempt records
remain local runtime artifacts. Commit reusable code, synthetic examples and
curated verification reports rather than runtime directories.

## Proposed OpenCode entry points

These command names are specifications only; no command files are introduced here.

| Command | Expected behavior |
| --- | --- |
| `/make-trailer <brief> <output>` | Plan, quote, generate via selected provider, collect, edit, validate |
| `/profile-asset <path>` | Inspect supported media and produce a versioned semantic profile with evidence |
| `/find-clients <asset/profile> <market constraints>` | Match categories, research real prospects and export sources and qualification |
| `/contact-client <prospect> <offer>` | Execute instructed outreach through the selected channel and record outcome |

A client request must specify the service being sold and intended market; use the
asset profile to suggest sensible defaults. For outreach, collect missing sender
identity, contact channel and portfolio URL rather than inventing them. A general
request for prospect research is not a request to submit messages.

Playwright form handling must distinguish filled, submitted, confirmed, rejected
and ambiguous states. Record a visible success receipt when available; clicking
Send does not prove delivery. Avoid automatic re-submission after uncertain results.
Browser logins and interactive challenges need user participation when encountered.

## Existing components and gaps

| Component | Reuse | Needed work |
| --- | --- | --- |
| `scripts/client_references.py` | Live SIE request contract, source IDs, hashes and revisions | Separate asset profiling path; current CLI does not accept MP4 |
| GMI Cloud MCP | Schema discovery, estimate, submit and status tools verified | Persisted provider-neutral orchestration and resumable jobs |
| Local FFmpeg helpers | Clip normalization, titles, contact sheet and decode-check pattern | Parameterize paths, timing and dimensions; explicit handling of short/silent/bad clips |
| Semantic prototype | Exact SIE input/response capture and cosine matching | Token-aware chunks, fresh indexes, configurable scoring, versioned records and query CLI |
| Web research | Official-source verification and category expansion | Source snapshots/excerpts, freshness policy, organization deduplication and market filters |
| Playwright MCP | Browser access available; used to inspect provider sign-in | No prospect-contact workflow has been executed or verified |
| Cognee | Existing `sao_project`/`sao_client_<id>` contract | Store durable decisions/preferences only; do not ingest runtime media or full lead databases |

The local prototype uses hard-coded Bellweather paths and assumptions. It also
upserts SQLite rows without deleting removed candidates, uses a word-count proxy
for the token limit, and weights all scenes equally. These need explicit fixes
when extracting a reusable implementation. Use fresh per-run indexes or pruning,
versioned embedding keys, tokenizer-based chunking, and duration-aware aggregation
where scene lengths vary.

Do not label local cosine computation as the Superlinked vector-search framework.
If scale or multi-field ranking warrants that framework, evaluate and verify it
as a separate integration; the currently verified Superlinked component is SIE.

## Implementation slices and acceptance

1. **Portable records and media profiler.** Accept two different local videos,
   extract timestamped evidence, reject hash mismatches and produce validated
   profiles without assuming a title, folder or five equal-length clips.
2. **Resumable generation and editing.** A stopped run resumes existing request
   IDs without duplicate submissions. Test success, failure, missing audio and
   ambiguous submission using controlled provider responses; verify a live run
   separately with an explicitly approved estimate.
3. **Reusable semantic matching.** Use a configurable SIE endpoint, test token
   boundaries and invalid vectors, prevent stale candidates, and expose score
   components with supporting scenes. Evaluate rankings against a small labeled
   relevance set; do not train or report conversion predictions without outcomes.
4. **Prospect research.** Produce deduplicated organizations with official-source
   evidence and public contact routes. Mark unknown demand as unknown; include
   relevant negative examples such as fiction versus factual reporting.
5. **Outreach execution.** First verify form behavior on a local fixture site,
   including validation errors and ambiguous submission. A real instructed attempt
   must retain the message and observed outcome and prevent duplicate sends.
6. **Business validation.** Track responses, qualified conversations, quotes and
   paid work. Distinguish replies from interest and interest from a purchase.

Each slice should have a small independent PR and meaningful checks. No additional
generation spend or outbound contact is required for this documentation PR.

## Durable project note

- **Verified:** GMI MCP produced a local trailer; SIE embedded agent-authored
  observations; local similarity matching informed official-site prospect research.
- **Planned:** reusable asset profiling, provider orchestration, evidence-backed
  prospecting and Playwright outreach.
- **Unverified:** purchasing demand, final sales value, direct video semantics,
  automated outreach and a production multi-tenant boundary.
- **Source:** this plan and the linked run report, 2026-11-07.

Cognee tools were unavailable when preparing this PR; this note is stored in the
repository and has not been claimed as a successful `sao_project` memory write.
