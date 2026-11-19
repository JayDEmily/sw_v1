# Shoco SW2021 Chat Succession trial - 20 November 2026

## Scope and pinned baseline

- Repository: `JayDEmily/sw_v1`.
- Original branch: `work/sw2021-full-source-library-20261119`.
- Exact pinned baseline: `bb258b66d311f3a5a8c2d5eea83310d41dfdce6a`.
- Isolated receipt branch: `work/chat-succession-audit-sw2021-20261119`, branched directly from that baseline.
- Scope: a read-only lookup against the existing local English SOLIDWORKS 2021 Help index. No CAD document, SOLIDWORKS application, macro or diagnostic probe was run. Source extracts and SQLite database remain local; no source text is published.

## Worker 1 - observed lookup receipt

- Requested command: `python3 scripts/search_library.py "concentric mate" --limit 1 --json` (existing Ubuntu index at `/home/jds/sw_v1`).
- Corrected direct Python invocation: exit code `0`; JSON query `concentric mate`; one result.
- Result: source label `core`; title `Concentric Mate`; topic ID `14028`.
- Observed status: `source_text_indexed`, `unreviewed`, `untested`. This is a source-index lookup, not an independently reviewed diagnostic or CAD runtime validation.
- Invocation caveat: an initial Windows-to-WSL shell quoting attempt lost the exact query and flags and produced default text results. Only the corrected one-result JSON invocation is used for this receipt.

## Worker 2 - verification to append

Verify the exact source label/title/topic and lookup outcome against this narrow receipt. Verify that worker 1's published audit commit has parent `bb258b66d311f3a5a8c2d5eea83310d41dfdce6a`, that its only changed path is this note, and that the original work branch and files remain unchanged. Append exactly one verification line here stating the actual findings; do not promote research, review or CAD claims. Publish a second commit on this same audit branch and use a nonterminal `Chat-Succession-Next` trailer naming a third evidence review as the eligible next task. The controller's two-worker cap stops before that third review.
