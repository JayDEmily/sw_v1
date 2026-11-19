# sw_v1 — SOLIDWORKS 2021 diagnostic research

Read **frozen** [GUARDRAILS.md](GUARDRAILS.md), [AGENTS.md](AGENTS.md), then the live [EXEC_PLANS.md](EXEC_PLANS.md).

This repository contains a research coordinator and the exact archived starter inputs. It is **not** a validated CAD diagnosis application. No macros are executed by the queue.

- View local queue: `python3 build.py status`
- Request current bounded research job: `python3 build.py next`
- Submit a checked worker response: `python3 build.py accept /absolute/path/reply.json`
- Configure an external independent worker only when separately authorised; `python3 build.py run N WORKER ...` has no bundled AI service or browser.
- The three pilots must pass source reopening by a distinct reviewer and the owner must explicitly approve expansion before any discovery job becomes eligible. Do **not** fabricate owner decisions or reviewer identities.

Original artefacts and hashes: [source manifest](docs/SOURCE_MANIFEST.md). Current environment: [preflight](docs/ENVIRONMENT_PREFLIGHT.md). Research records and review status: `research/`. The queue's local `ledger.json` and `.bak` are ignored to avoid mistaking auto-generated state for source evidence.

Python >=3.8, standard library. This phase does not require installing SOLIDWORKS modules. For queued review, `directly-opened` means the reviewer actually accessed the 2021 page content rather than merely a search-result excerpt; where the Help site's JavaScript shell prevents that, record an evidence blocker and use the user's installed offline 2021 API Help only for API statements it actually contains.

### Current pilot status

Three user-readable drafts: `research/pilots/{shell,spline-3d,mate-concentric}.md`, with machine-readable `.json` partners. Source inspection: `research/evidence/OFFLINE_HELP_INDEX.md`. Same-session preliminary audit: `research/reviews/PRE_REVIEW_EVIDENCE_CHECK.md`. **Independent L04 review has not occurred**; discovery remains gated. Do not confuse author self-check with independent approval.
