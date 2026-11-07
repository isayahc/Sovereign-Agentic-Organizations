# Bellweather: live video-to-prospect experiment

Verified on 2026-11-07. This experiment extends the studio's commerce research:
generate an asset, describe its actual output, retrieve plausible buyer categories,
and research organizations that might commission related work.

## What exists

| Stage | Verified result |
| --- | --- |
| Generation | Five 15-second clips submitted through authenticated GMI Cloud MCP; all five reached `success` |
| Local delivery | Downloaded originals, normalized clips, assembled and titled MP4 |
| Technical verification | 75.008 seconds, 1920 × 1080, 24 fps, H.264 video/AAC audio; complete FFmpeg decode passed |
| Visual review | Contact sheet inspected at 5, 12, 20, 28, 34, 42, 49, 56, 62, 66, 71 and 73 seconds |
| Semantic extraction | OpenCode-authored observations of sampled rendered frames, plus render captions |
| Embeddings | 21 real, normalized 384-dimensional Superlinked SIE vectors persisted in SQLite |
| Retrieval | Eight buyer-category hypotheses and seven sourced organization profiles ranked by local cosine similarity |
| Sales research | Official-site genre/product evidence, contact routes, suggested offers and qualification gaps recorded |

These are completed local experiments, not a packaged application. Scripts and
artifacts reside in ignored `.local/bellweather-pier/`; this PR preserves the
findings and implementation plan. A fresh clone does not contain the media or
the one-off scripts. No outreach or sale occurred.

## Generation and delivery

The user supplied the fictional story **The Last Light at Bellweather Pier** and
selected a 60–90-second trailer. The completed edit is five 15-second sequences:
harbor and abandoned coat; investigation; suspicion and financial papers;
office questioning and departure; telephone, coat and title reveal.

- Provider: GMI Cloud MCP, `https://mcp.gmicloud.ai/mcp`.
- Model: `gemini-omni-1.2-flash`, discovered from the live catalog.
- Parameters: `task=text_to_video`, `durationSeconds="15"`,
  `aspectRatio="16:9"`, `resolution="1080p"`.
- Estimate: $1.50 per clip, $7.50 for five, explicitly approved by the user.
  This is the quoted estimate, not a reconciled final invoice.
- Each accepted request ID was saved before collection. Completion was checked
  through `get_generation`; no replacement generations were needed.
- Generated audio streams were present in all five clips. Local editing added
  fades, captions and a title. No spoken narrator was commissioned.
- Verification used FFprobe and a full FFmpeg decode, plus sampled visual review.
  This does not constitute a full human audiovisual quality review.

Final file: `.local/bellweather-pier/bellweather-pier-trailer.mp4`.
Size: 62,580,983 bytes.
SHA-256: `f232895a46923ec8288ab4d41bd273db8ce1028559f396238080e51b43c95fc5`.

GMI MCP was added to the operator's global OpenCode configuration, not the project
configuration. OAuth credentials remain outside the repository. To set up a new
operator, add the endpoint with `opencode mcp add gmi-cloud --global --url
https://mcp.gmicloud.ai/mcp`, then use `/mcps` to sign in if required.

## What Superlinked did—and did not do

The running SIE Local `0.11.0` served
`sentence-transformers/all-MiniLM-L6-v2`, revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, on CPU in WSL.
Its input capability is **text**, not video.

1. Checked the MP4 hash against the prior render verification record.
2. Inspected the existing 12-frame contact sheet extracted from that render.
3. Authored five timestamped scene descriptions and a whole-video summary.
4. Used the ASS captions that were actually rendered, cross-checked in samples.
5. Embedded the summary, five scenes, eight categories and seven organizations
   through `http://127.0.0.1:8080/v1/embeddings`.
6. Saved exact text inputs and responses; checked vector dimension, finiteness
   and nonzero norm; normalized vectors and stored them in SQLite.
7. Ranked profiles using local Python cosine similarity:

```text
score = 0.6 × cosine(video_summary, buyer_profile)
      + 0.4 × mean(cosine(scene, buyer_profile))
```

SIE supplied embeddings. OpenCode supplied visual interpretation and research.
SQLite and local Python supplied persistence and ranking. This did **not** use
the Superlinked vector-search framework, a video encoder, automatic video
captioning, OCR or speech transcription. The installed reference-ingestion CLI
does not accept MP4; it was not presented with an unsupported video file.

The 256-token model context is a constraint. Descriptions were kept short, but
the prototype's word-count guard is not an exact tokenizer-based length check.
The formula and weights are uncalibrated. Candidate choice, wording and sampled
frames influence results; scores are not probabilities of purchase.

## Findings

Observed semantics: fictional coastal mystery, missing person, female investigative
lead, financial papers, suspicion, withheld evidence, blue/amber nighttime palette,
and a spoiler-free cinematic title reveal. The trailer does not explain the
original story's resolution or prove any real crime occurred.

| Buyer category | Similarity |
| --- | ---: |
| Mystery events and escape-room operators | 0.455 |
| Crime/mystery publishers and authors | 0.420 |
| Narrative detective-game studios | 0.395 |
| Mystery-fiction podcast producers | 0.354 |
| Coastal tourism | 0.257 |
| Critical-thinking educators | 0.255 |
| Factual true-crime producers | 0.195 |
| Consumer product advertisers | 0.002 |

The first research pass emphasized publishers. After mystery experiences ranked
highest, research expanded to The Detective Society and Hunt A Killer. This is a
useful example of letting retrieval change the research direction, while retaining
the fact that the candidate set was selected by an agent rather than exhaustively.

| Organization | Similarity | Evidence and recommended treatment |
| --- | ---: | --- |
| The Detective Society | 0.402 | [Press kit](https://explore.thedetectivesociety.com/press/) lists mystery games and existing trailers. Best first prospect for a custom case teaser. [Business contact](https://explore.thedetectivesociety.com/contact-us/). |
| Hunt A Killer | 0.293 | [Immersive mystery products](https://www.huntakiller.com/pages/our-story); propose a teaser for an actual case. [Contact form](https://www.huntakiller.com/pages/contact). |
| Joffe Books | 0.276 | [Crime/mystery catalog and marketing](https://joffebooks.com/about); potential custom book-trailer client. [Business proposals route](https://joffebooks.com/contact). |
| Storm Publishing | 0.266 | [Genre fit](https://stormpublishing.co/what-we-are-looking-for/) but qualify its [AI approach](https://stormpublishing.co/ai-statement/). Manuscript restrictions do not establish a marketing-video ban. |
| Bookouture | 0.263 | [Thriller publishing and campaign roles](https://bookouture.com/team/); potential custom launch campaign. [Contact form](https://bookouture.com/contact/). |
| Film 14 | 0.242 | [Existing trailer service](https://film-14.com/book-trailer-services/): competitor/possible partner, not a presumed direct buyer. |
| Bloodhound Books | 0.172 | [Digital publishing and marketing](https://www.bloodhoundbooks.com/our-story); genre catalog additionally corroborated by search. [Contact](https://www.bloodhoundbooks.com/contact-us). |

Research date: 2026-11-07. Contact routes and organizational fit are evidence;
current demand, budget, outsourcing intent and acceptance of generated visuals
remain unknown. No qualified buyer of the unchanged Bellweather trailer was found.

The most defensible offer is **custom trailer production demonstrated by this
sample**. A buyer-specific title, call to action, larger mobile captions, vertical
composition and 15/30-second cuts would be additional work. No market price or
conversion rate was validated; competitor service prices are not this asset's value.

## Local evidence inventory

All paths below are relative to `.local/bellweather-pier/` on the test machine.

| Artifact | Purpose |
| --- | --- |
| `generation-jobs.json` | Provider/model/settings, approved estimate and five request IDs |
| `submitted-prompts.json` | Exact shared visual direction and clip prompts |
| `confirmed-outputs.json` | Successful outputs and provider download locations |
| `shot-01.mp4` through `shot-05.mp4` | Downloaded original clips |
| `trailer-plan.md`, `trailer.ass` | Creative outline and actual caption timing |
| `assemble.py`, `download_clips.py` | One-off local assembly and download helpers |
| `verification.json`, `contact-sheet.jpg` | Technical checks, source metadata and sampled visual evidence |
| `semantics/observations.json` | Scene observations, interpretation limits and sales hypotheses |
| `semantics/buyer-profiles.json` | Category hypotheses, researched leads, source URLs and qualification |
| `semantics/analyze.py` | One-off live SIE embedding and local ranking implementation |
| `semantics/video-profile.json` | Hashed asset, timestamps, model metadata and semantic profile |
| `semantics/sie-responses.json`, `semantics/semantic-index.sqlite` | Exact inputs/responses and stored vectors |
| `semantics/rankings.json`, `semantics/prospects.csv`, `semantics/buyer-report.md` | Ranked outputs and commercial interpretation |

See [the generalization plan](asset-prospecting-plan.md) for the proposed reusable
workflow and the gaps this experiment exposed.
