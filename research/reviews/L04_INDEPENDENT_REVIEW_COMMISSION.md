# L04 independent pilot review commission — SOLIDWORKS 2021

**Status: UNEXECUTED REVIEW ASSIGNMENT.** Authored 19 November 2026. The existence of this commission is not a review verdict. The commissioning author produced the pilot cards and is **not an independent reviewer**.

## Exact scope and evidence

Repository: `JayDEmily/sw_v1`; branch `work/sw2021-research-foundation-20261119`. Read frozen `GUARDRAILS.md` and `AGENTS.md`, living `EXEC_PLANS.md`, original `WORK_ORDER.md`, and the full original-source manifest `docs/SOURCE_MANIFEST.md`. The only candidates are:

- `research/pilots/shell.json` and `.md`
- `research/pilots/spline-3d.json` and `.md`
- `research/pilots/mate-concentric.json` and `.md`

These are authored research, **not** existing independent reviews. Their original primary-source topics are indexed in `research/evidence/OFFLINE_HELP_INDEX.md`. Same-session preliminary checks in `research/reviews/PRE_REVIEW_EVIDENCE_CHECK.md` are non-independent and must **not** substitute for your own evidence.

## Reopen the original 2021 documentation yourself

On the user's connected Windows machine, **read-only**, locate:

`C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\lang\english\sldworks.chm`

Installed file SHA-256 as previously observed: `9e4357baab971a63bb3a8c4e431cae579ba42f8c3a6d2a69d410f513cb77aec6`. Verify the hash independently. `C:\Program Files\7-Zip\7z.exe` can stream named internal HTM bytes with `7z.exe e -so [CHM path] [topic]`, requiring no extraction or filesystem writes. Inspect the actual content of every material cited topic, not just the filenames, web search snippets, other-year Help, or the research author's summaries. If local access is unavailable, use directly accessible official 2021 Help page content and label every source-access limitation precisely.

Pilot topic checklist (topic paths are relative to CHM root):

- Shell: `t_Shell_Feature_Diagnostics.htm`, `HIDE_SHELL_MODEL_FAIL.htm`, `c_Shell_Diagnostic_Cut.htm`
- 3D spline: `t_Creating_3D_Splines.htm`, `HIDD_DVE_SKETCH_SPLINE_3D.htm`, `c_Sketch_Relations_in_3D_Sketches.htm`, `t_Using_Control_Polygons.htm`
- Concentric mate: `c_Example_of_Concentric_Mate_Error_SWassy.htm`, `t_techniques_fixing_mate_problems.htm`, `t_allowing_misaligned_concentric_mates.htm`

## Required independent checks, **for each** card

1. Map each consequential source-derived statement to content you independently read in the installed 2021 Help. Verify exactly what is documented versus a hypothesis. Challenge misleading terminology, undocumented assumptions and the wrong release.
2. Check whether the symptom and the alternatives are plausible yet distinct; identify material omitted alternatives without guessing a definitive diagnosis.
3. Scrutinise every probe's preconditions, units, configurations, user actions, reversibility, source/engineering basis and whether the test truly distinguishes the named rivals.
4. Verify each possible observation, especially **inconclusive**, with explicit interpretation, inference boundary and next step. Challenge any claim that a passed local probe proves success of the full feature.
5. For Shell, examine local offset vs whole shell intersections/trimming and the effect of cutting away material; for 3D spline, plane/XYZ/relations/handle/continuity controls; for mates, exact concentric geometry, redundant constraints, fixed states and deliberate misalignment tolerance.
6. No runtime/SOLIDWORKS application tests or macros are authorised by this review commission. Never claim fixture validation or change the local licence, CAD models, add-ins or installed software.

## Publication and queue contract

Publish one independent report containing the reviewed candidate Git SHA, reviewer context, source-read method, CHM hash, individual verdict and finding for each of the three pilot cards, claim-to-evidence citations, unresolved claims, and exact recommendations. Give `approve`, `revise`, or `blocked` separately by pilot. Do not approve syntactically valid JSON as sufficient evidence.

Where the independent reviewer is an actually separate worker and session, a queue review response for each pilot may be recorded using `python3 build.py next` / `python3 build.py accept RESPONSE.json`, with the current queue token and an honest `actor` identity. A `review` response must provide `checks`, `reason`, `independence: distinct-worker-and-context`, `reopened_sources` (original source URL, section, specific finding, `access_mode: offline-chm` or `directly-opened`). **Never fabricate independence or claim the current author performed this review.**

The current queue is saved locally under ignored `ledger.json` and is single-writer. Preserve the existing research admissions; do not delete the ledger or create a different unlinked review history. Before accepting any review, verify the local queue head is a pilot in `review` and that the candidate JSON and stored card payload agree. Non-pilot discovery and owner decision remain blocked until all three pilots are genuinely reviewed and the owner expressly decides to scale.

Stop after the three evidence-backed verdicts. Present them for the user's engineering usefulness decision at **G1**; no L05 inventory or full rollout on this commission.
