# Implementation evidence — L01–L04

## L01 — source admission

Source ZIP archives and VBA macro admitted byte-for-byte into `source/originals/`, extracted without running into `source/extracted/`. Hashes: see `SOURCE_MANIFEST.md`. Root `WORK_ORDER.md` is identical to source. No user CAD file imported. Ubuntu checkout and Windows environment preflight recorded separately.

## L02 — queue redesign

Root `build.py` is a stdlib CLI wrapper for `src/queue.py`; original `build.py` is preserved in `source/extracted/builder/build.py`. Features:

- Three pilot drafts required before pilot review; **no discovery job eligible until all three pilots have independent approved reviews AND the explicit owner decision is recorded.**
- Response binding: expected ID, phase and token; actor worker/session IDs; stale replies rejected.
- Card contracts require observable symptoms, rivals, inputs/side effects, supported source links, outcomes (including inconclusive), inference limits and next step.
- Review contracts require a separate worker/session identity and actual reopened source IDs; index snippets are not an acceptable review. An attestation is required; this prevents accidental self-review **but cannot cryptographically prove that an actor did not falsify identity**.
- Single-writer directory lock, atomic saves with prior-state `.bak`, bounded `revise` cycles, persistent history and explicit blocked exception trail. A stale lock requires operator inspection; a corrupted ledger is never silently overwritten.
- All output is labelled evidence-reviewed **or** runtime-untested, not conflated. `inventory_complete` deliberately false until a separate inventory reconciliation exists.

Verification: `PYTHONPATH=. python3 -m unittest discover -s tests -v`. These are synthetic tests, not a SOLIDWORKS execution. See actual results in run ledger below; do not claim a full security boundary on review identity from metadata alone.

## L03 — three authored pilot drafts

Source inspected directly from the installed 2021 `sldworks.chm` via `7z.exe e -so`: see `research/evidence/OFFLINE_HELP_INDEX.md`. Three `.json` and three `.md` pilot outputs are in `research/pilots/`. Source-to-claim mappings, competing explanations and inconclusive outcomes are included. No API member is asserted for a UI-only probe. No CAD part, assembly or macro was opened or executed.

## L04 — separate review required / pending

The same-session preliminary source-to-claim challenge in `research/reviews/PRE_REVIEW_EVIDENCE_CHECK.md` is **not an independent review**. A distinct reviewing worker and source reopening is needed before marking any pilot approved. The original worker runner is a placeholder and did not provide a separate reviewer. G1 remains pending; full-catalogue discovery and add-in research are not authorised until the stated gate is satisfied.

## Reproduction and next checkpoint

In a clean temporary working directory with the repository available on `PYTHONPATH`:

1. Run `python3 -m unittest discover -s tests -v` in the repository root for synthetic tests.
2. Run `python3 build.py status` from `/home/jds/sw_v1`. The local `ledger.json` already contains the three authored pilot submissions, currently all in `review`, with three discovery jobs `todo` but ineligible, owner gate `pending` and zero cards evidence-reviewed. This runtime ledger is deliberately Git-ignored; preserve it for continuity. For a fresh clone, `python3 scripts/import_pilot_drafts.py` creates/admits the three original authored records idempotently.
3. Commission a genuinely distinct reviewing worker using `research/reviews/L04_INDEPENDENT_REVIEW_COMMISSION.md`. Reviewer independently reopens actual 2021 documentation, writes a reasoned separate verdict for each pilot, then submits correctly token-bound `build.py accept` review responses with honest actor/session and reopened-source records. Do not impersonate an independent worker or clear the owner gate.

**Observed Ubuntu execution, 19 November 2026:** Three original source SHA-256s match `docs/SOURCE_MANIFEST.md`; `python3 -m unittest discover -s tests -v` passed 14/14 under Python 3.14.4; `python3 -m compileall -q build.py src research/create_pilots.py` passed; `PYTHONPATH=. python3 research/create_pilots.py` generated three schema-checked pilot files; `python3 scripts/import_pilot_drafts.py` admitted three research responses, no review responses; queue status verified review=3 / owner pending / discovery ineligible. Git branch commit and remote verification are recorded in `EXEC_PLANS.md` once published.
