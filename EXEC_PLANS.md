# EXEC_PLANS.md — SOLIDWORKS 2021 diagnostic-library execution plan

**Plan type:** Living ExecPlan; subordinate to frozen `GUARDRAILS.md` and `AGENTS.md`.
**Created:** 19 November 2026.
**Repository:** `https://github.com/JayDEmily/sw_v1`
**Working branch:** `work/sw2021-research-foundation-20261119`
**Starting point:** `main` at `c6c8eb38ffbd1c82fc8ff62483830f02dcacd55d` ("Initial commit", README only).
**State:** FOUNDATION DOCUMENTS ONLY. Implementation Leaves L01–L09 are **NOT STARTED**. This plan is a specification, not a claim of execution or validated SOLIDWORKS behaviour.
**Current authority:** Publish ONLY the three root Markdown documents on the working branch, verify commit/readback and **STOP**. A subsequent, explicit user request is required to begin implementing this plan.

## A. Purpose, user outcome and scope

Create a version-specific, pre-researched **English SOLIDWORKS 2021 part/assembly/mate diagnostic library**. Its entry point is the designer's observable symptom, not merely the name of a Help topic. Each useful answer identifies plausible competing causes, the least disruptive discriminating test, possible results (including inconclusive), what each result establishes **and does not establish**, and the next investigation.

Astra's supplied `WORK_ORDER.md` is the principal research commission. Keep the existing `PartCrawler.bas` and `Research.bas`/`research.py` conceptually distinct from the research builder: the crawler probes a current part; the helper is an early lookup interface; the builder organises the **future knowledge corpus**. None proves the corpus already exists or has been tested.

Success means three independently evidence-reviewed and owner-judged pilot diagnostic cards, then a reconciled in-scope feature inventory, a resumable reviewed-card campaign, accurate status/exception reports, and ultimately selectively runtime-tested procedures. A future retrieval interface is a separate implementation deliverable. Do not promise that every modelling failure is diagnosed or that every UI operation has an accessible API.

### Non-goals

No production CAD modifications, unapproved SOLIDWORKS execution, generic unsourced chatbot, automatic copying of confidential geometry to external services, drawings/Simulation/CAM/Electrical/specialist-add-in coverage by implication, or merger into `main` under the present commission.

## B. Source-of-truth inventory (inspected 19 November 2026)

The following were uploaded to this ChatGPT project, not found in the initial Git repository. **This foundational commit does not import or modify them.** During L01, recover the original bytes, verify these SHA-256 values and record where they are staged.

| Exact attachment | SHA-256 | Observed role |
| --- | --- | --- |
| `PartCrawler.bas` | `7cd1d511d5d47dca1d1e80b43b8cba934c5fb75551419e59e89dab2471aaf7c2` | 140-line VBA part-body/feature and optional per-face temporary offset probe; outputs a text report; no observed SW2021 runtime result |
| `SW2021-Research-This.zip` | `c761be9e239d64e1b8e35c56583482c84f45968e427b79d93753a412790127df` | `Research.bas`, `research.py`: selected-topic lookup and curated Help references, with optional Brave web search; not a reasoning model or completed library |
| `SW2021-Research-Builder.zip` | `8d0e8c9ffe21d5f6fb96e90788ae50f259c90d9a939e5847de964df82de10f2e` | `WORK_ORDER.md`, `build.py`, `START.txt`: web-research instructions plus local JSON queue and model-runner adapter contract |

Verified individual builder member hashes: `WORK_ORDER.md` SHA-256 `0529849181f9fa604b79f1efd3a9c4361ab5013b7a49091a6ea6a634acdaf1aa`; `build.py` SHA-256 `241ed1dc8bfa17093d4c024dfe71ac564354af1f7f2890df22e78e5aefe5aa98`.

Source scope from `WORK_ORDER.md`: part modelling including sketch entities/relations, sheet metal, weldments and surfaces; assemblies, configurations, component states, references and assembly features; mate families and subtypes. Official 2021 Help is the proposed primary inventory source, with independent second-inventory reconciliation. Add-in dependencies/exclusions must be explicit.

### Initial technical observations (planning evidence, not runtime claims)

- `build.py` seeds three card jobs (`shell`, `spline-3d`, `mate-concentric`) and three discovery jobs (`parts`, `assemblies`, `mates`). Its `current()` function selects any `todo`/`review` job, so the pilot approval/owner gate is **not enforced** before discovery work begins.
- The driver checks structural presence of fields but does not verify source truth or review independence. One adapter can produce both a card and its review. Recorded `done` therefore means an accepted review-shaped object, not proven diagnostic validity.
- A model-runner executable, browser access, completed cards, production retrieval layer and SOLIDWORKS bench test results are **not supplied**.
- Its ledger is `ledger.json` in the working directory, written via temporary file and `os.replace`. The source instructs **one coordinator** per directory; concurrent ownership, robust backup/recovery and detailed exception accounting are not yet implemented.
- The `status` command reports aggregate job states, not the work order's requested per-branch coverage/reconciliation. Existing `retry` simply reopens a blocked job, not an adjudicated evidence repair.
- No observed demonstration establishes that `PartCrawler.bas`'s probes or `Research.bas`'s selected-context logic behave as expected in the actual installed 2021 service pack. Their documentation may be useful, but has not been empirically validated.
- For Shell, a returned temporary offset body for every isolated face does **not** prove the integrated shell's intersection, trimming, topology or final body will succeed. This should be a pilot inference-boundary test.

These are specific engineering tasks, **not** a reason to add unrelated process gates or redesign the entire builder.

## C. Frozen baseline fingerprints

The following are the SHA-256 checksums of the original governance documents written for this foundation. These fingerprints detect content changes; Git commit history is the audit authority, and there is no claim of an OS-enforced immutable flag.

- `GUARDRAILS.md`: `1f6c9cd584bf083173c4562dc0aec52caf359270e7bbb5f2e1169e8e6e51c89e`
- `AGENTS.md`: `2b032d3cb4dbc6951137e886edba9314b44ce66c9cebd028d1357eba4daa593a`

Future implementation may update **this** plan's progress, evidence and decisions. It must preserve these two documents exactly unless the user explicitly authorises a separate governance revision.

## D. Execution rules for future authorised work

Each leaf below is a bounded unit. Start with read-only inspection of the required files and the exact current branch/commit; implement only its stated scope; carry out the least sufficient verification; record actual outcomes and commit a traceable checkpoint when authorised for that implementation. Never turn a failed verification into an unsupported pass. Preserve state and stop at the specified owner gate.

Keep a concise leaf log here (date, branch, commit, changed paths, check commands/results, remaining issues). Add more detail in a separate evidence artefact only if a material finding needs it; do not inflate permanent governance. A worker may divide a large leaf into independently recoverable subjobs without changing its acceptance criteria or scope.

### G0 — Governance foundation: CURRENT COMMISSION

**Input:** blank GitHub `sw_v1` repo at the initial commit; three supplied project attachments; official OpenAI documentation referenced below.

**Deliverable:** only root `GUARDRAILS.md`, root `AGENTS.md`, root `EXEC_PLANS.md` on `work/sw2021-research-foundation-20261119`.

**Verification:** confirm `main` remains at its starting commit; only the three intended files are added; run `git diff --check` (or staged equivalent); verify exact GitHub remote head SHA, tree, parent, changed-path list and complete content readback. Record SHA-256 of both frozen docs.

**Exit gate:** after verification, **STOP**. Do not automatically start L01. A foundation commit is not an endorsement of later code or research.

### L01 — Source admission and reproducible workspace

**Status:** Not started. **Prerequisite:** new user instruction authorising implementation.

**Work:** obtain the three exact supplied attachments, verify archive/member hashes above, reject mismatches, unpack into a clearly labelled source/staging area; preserve the originals. Establish the project's dedicated Ubuntu working path and concise README/run instructions. No Python execution beyond local dry-run/structural checks and no CAD runtime execution. Reconcile Python 3.8+ and Windows macro constraints without assuming the same interpreter or filesystem.

**Acceptance:** source provenance manifest, reproducible extraction, clean path handling, source/derived separation and exact mismatch reporting. No unrequested changes to other repositories, system Python or environment configuration.

### L02 — Repair essential queue/control gaps, not the research method

**Status:** Not started. **Depends:** L01.

**Work:** retain `WORK_ORDER.md`'s `discover`/`card`/`review` JSON contract, improving only justified coordination features:
1. Hard gate all non-pilot discovery/card jobs until the **three** pilot cards each have a valid independent evidence-review outcome **and** an explicit recorded owner decision to scale; block `run` and manual `next/accept` from bypassing this condition.
2. Record research author/session, reviewer/session, reviewed source pointers and verdict; prevent a reviewer from being accepted as independent if it merely reuses its own research output. Human confirmation or genuine distinct pass is required where an independent review claim is made.
3. Add durable exceptions, bounded revision attempts, reliable restart semantics, backups and one-writer state ownership. Revisions must preserve provenance and failed results, not silently reset history.
4. Generate per-branch inventory/card/review/runtime-status summaries with honest denominators and unresolved exclusions; do not label a sampled inventory complete.
5. Provide local synthetic fixtures/tests for gate bypass, stale replies, duplicate IDs/aliases, atomic recovery, corrupted state and rejected reviews. A structurally valid synthetic card must **not** satisfy the evidence or owner gate by itself.
6. Keep external worker adapter optional and explicit; do not imply a model subscription, browser, agent runner or unattended service was bundled.

**Acceptance:** tests demonstrate that pilot gate and separate review evidence actually prevent premature rollout; project remains operational without a model API; no real SOLIDWORKS tests; no unexplained change to original research requirements.

### L03 — Three bounded pilot research jobs

**Status:** Not started. **Depends:** L02 and working public-documentation access.

**Work:** with a web-enabled worker, create one diagnostic card each for:
- `shell` (part geometry / whole-feature versus individual-face offset);
- `spline-3d` (3D sketch entity, constraints, control behaviour);
- `mate-concentric` (assembly mate and constraints).

For each: cite source URL + exact 2021 section and paraphrased fact; distinguish verified documentation from hypotheses; list designer-visible symptoms; enumerate plausible rival causes; give reversible/manual tests first where appropriate; record exact conditions, units, configuration, side effects, possible outcomes, inconclusive outcomes, limitations and next discriminating step. An API probe needs a verified **2021** member/signature. Sources inaccessible or absent must remain blocked, not invented.

**Acceptance:** three inspectable first-pass cards and evidence pointers with no false `tested` or `approved` label. This is research output, not a validation of the methodology.

### L04 — Genuine evidence review of each pilot

**Status:** Not started. **Depends:** L03.

**Work:** a separate reviewer pass independently reopens cited 2021 sources, verifies exact version/API references, challenges the strongest diagnostic claim, evaluates competing explanations, tests/probe reversibility, missing inconclusive outcomes and unsupported generalisations. Reject inadequate cards with specific corrections; blocked primary evidence remains blocked.

**Acceptance:** for each pilot, a linked evidence-backed `approve` / `revise` / `blocked` record; traceable reviewer independence and source-to-claim findings. An approved card becomes **EVIDENCE-REVIEWED**, explicitly **NOT RUNTIME-TESTED**.

### G1 — Owner assesses pilot usefulness (HARD STOP)

**Status:** Not started. **Depends:** L04.

Present the three reviewed cards to the user together with weaknesses, remaining unknowns and a concrete comparison with a generic Help summary. Ask **one actual engineering judgement**: do these cards explain the next discriminating experiment and limits well enough to scale?

- **Proceed:** record explicit owner decision; enable L05 onwards.
- **Revise:** refine method and rerun affected pilot review, no full-catalogue work.
- **Stop/block:** preserve records; no automatic discovery or scale-up.

An agent cannot self-approve this gate, nor infer approval from elapsed time or absence of objections.

### L05 — Enumerate and reconcile official SW2021 inventory

**Status:** Not started. **Depends:** G1 proceed.

**Work:** traverse the **actual** 2021 Help contents across parts, assemblies and mates. Enumerate every in-scope immediate child rather than sampling search results. Record official URL, section and parent, canonical ID, alias, type (UI command, tree feature, sketch entity, mate subtype, API-only), add-in dependency and explicit exclusion. Cross-check against an independent inventory (2021 API Help catalogue / PropertyManager or command index). Different labels in the UI/API are not silently equated.

**Acceptance:** reconciled tree with counts and explicit missing/contradictory cases; unresolved branches labelled blocked, not zero children. Canonical IDs stable; no duplicate card created for aliases. No claim of 100% coverage where evidence is missing.

### L06 — Controlled feature-by-feature research and review campaign

**Status:** Not started. **Depends:** L05.

**Work:** dispatch one bounded source-backed card at a time, review evidence before acceptance, use stable reusable probe IDs with contextual applicability. Allow batches under one authorised coordinator with budget, retry bounds and resume checkpoints. Honour inaccessible source blocks. Keep research and review trace distinct. Preserve detailed actual coverage and exception reporting.

**Acceptance:** evidence-reviewed corpus by branch with `todo`, `review`, `done`, `blocked`, `untested` and excluded counts; every approval points to review evidence; no claim to diagnose all possible failures. Document cost/throughput so a lower-cost worker is actually used for repetitive work where configured.

### L07 — Controlled SOLIDWORKS 2021 bench validation

**Status:** Not started. **Depends:** suitable reviewed cards and separate authorisation for use of a real installation.

**Work:** identify actual SOLIDWORKS version/service pack, use known-good and deliberately failing **disposable** parts/assemblies. Run only authorised probes, monitor any side effects and preserve observations. Compare outcome against prediction for supported conditions. Classify runtime result separately from evidence-review state; record discrepancies without mutating production models.

**Acceptance:** fixture manifests and actual results supporting any `RUNTIME-TESTED` designation, with negative/inconclusive evidence and reproducible inputs where shareable. No automatic promotion of an untested card.

### L08 — Retrieval and designer-facing diagnosis

**Status:** Not started. **Depends:** sufficiently useful corpus and retrieval design informed by pilots.

**Work:** create a minimal local search/index over accepted records by feature, symptom and observed outcome; link back to evidence and uncertainty. Decide whether `Research.bas`/`research.py` should be retained, adapted or replaced. Keep search-only capabilities distinct from any permission to execute a CAD probe.

**Acceptance:** on disposable/test data, a designer can retrieve relevant reviewed cards, see rival hypotheses and limits, and trace a claim to evidence; the interface never represents research-only procedures as runtime-tested.

### L09 — Completion audit and handoff

**Status:** Not started. **Depends:** previous authorised leaves.

**Work:** audit actual scope coverage, excluded submodules, blocked records, unreconciled aliases, API limitations, review provenance, validation evidence and remaining UI/runtime gaps. Publish a concise handoff with exact repository checkpoints and reproducible commands.

**Acceptance:** auditably report what is and is not built or tested, with no blanket completeness claims and no unauthorised merge, release or production CAD deployment.

## E. Research-record semantics and acceptance rules

Keep the supplied `WORK_ORDER.md` terminology and `build.py` contracts as the starting interface. For cards, the minimal useful answer is: sources → observable symptom → rival hypotheses → reversible discriminating probe → conditions → possible outcomes (including inconclusive) → what follows / what cannot be inferred. For discovery: official inventory and section pointers → complete child list → aliases/exclusions → second-inventory reconciliation → blocked gaps. For review: reopened-source findings → acceptance or precise revision/block reason.

Record **three different thresholds**: (i) `research authored`, (ii) `source evidence reviewed`, (iii) `observed running on specific SW2021 fixtures`. Passing a JSON shape check achieves none of (ii)/(iii). Never treat a local geometry test as equivalent to full-feature success, and never infer API invocability from a UI command.

## F. Checkpoint register (maintain only after observed work)

| Gate or leaf | State as of foundation | Required evidence before changing state |
| --- | --- | --- |
| G0 governance commit | Pending remote verification during this commission | remote SHA/tree/parent, exact file list/readback, checksums |
| L01 source admission | Not started | source hashes and manifest |
| L02 queue gates | Not started | observed synthetic tests and code diff |
| L03 three pilot research cards | Not started | three sourced records |
| L04 independent review | Not started | three actual review verdicts |
| G1 owner scale decision | Not started | user decision recorded |
| L05 inventory | Not started | official tree plus reconciliation |
| L06 research campaign | Not started | reviewed cards and coverage/exception report |
| L07 SW2021 bench validation | Not started | actual service pack, fixtures and observed results |
| L08 retrieval | Not started | demonstrated retrieval and provenance |
| L09 audit | Not started | scope/evidence audit and handoff |

A later authorised agent may update this table with observed evidence, dates and commit IDs. It must not edit the frozen documents to record progress.

## G. Official methodological references

The following links were consulted on 19 November 2026; they justify the **form** of the agent/work-plan system and the choice to keep it proportionate. Project-specific requirements above come from the user's instruction and the inspected SOLIDWORKS attachments; OpenAI guidance is not proof of SOLIDWORKS functionality.

1. [OpenAI Cookbook — Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans): ExecPlans, durable self-contained milestones and status.
2. [OpenAI Cookbook — Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex): root `AGENTS.md`, execution plans, bounded reviews/acceptance.
3. [OpenAI Developers — Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): context-specific instructions, avoiding unnecessary process.
4. [OpenAI Developers — Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex): frozen goals, milestone verification and durable progress state.
5. [OpenAI API — Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals): distinguish policy prose from actual enforced side-effect/approval boundaries.

A `PLANS.md` or `.agent/PLANS.md` name is an OpenAI Cookbook **convention**, not a mandatory API. This project deliberately uses the requested named plan `EXEC_PLANS.md`, referenced explicitly from `AGENTS.md`.

## H. Immediate stop condition

After committing and independently reading back the **three** foundational documents on the named working branch, provide the branch, GitHub commit URL, three file paths and observed verification. **STOP.** Do not treat publication of this plan as permission to begin L01 or any subsequent leaf.
