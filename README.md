# sw_v1 — SOLIDWORKS 2021 diagnostic knowledge project

**Read** frozen [GUARDRAILS.md](GUARDRAILS.md) and [AGENTS.md](AGENTS.md), then living [EXEC_PLANS.md](EXEC_PLANS.md). The 19 November owner instruction authorises full-catalogue research now, without waiting for the pilot review decision; see [scope update](docs/OWNER_SCOPE_UPDATE_20261119.md).

## What is actually built

- Source archive admission with exact input hashes, local Ubuntu Git checkpoints and source version notes.
- A synthetic-tested, independently review-gated three-pilot research queue (`build.py`, `src/queue.py`). Its three source-backed pilot diagnostic drafts remain **unreviewed**.
- A **separate full-product source index**, assembled from 14 locally installed 2021-era CHM Help archives: core modelling, API, Flow Simulation, CAM, Inspection and Plastics. API references are deliberately not equated to UI commands or model features.
- Complete TOC topic dossiers and a research worklist, each explicitly marked as source-indexed / unreviewed / runtime-untested.
- A local read-only SQLite FTS search index generated from the locally installed Help text, suitable as the data-side starting point for a future SOLIDWORKS Task Pane integration. The UI add-in **does not yet exist**.

See [exact source and missing-content counts](library/COVERAGE.md) and [original input manifest](docs/SOURCE_MANIFEST.md). The installed Inspection CHM includes an internally 2019-labelled TOC; do not assert a blanket release-specific validation from that archive.

## Search locally in Ubuntu

```sh
cd /home/jds/sw_v1
python3 scripts/search_library.py "shell fails"
python3 scripts/search_library.py "concentric mate"
python3 scripts/search_library.py "turbulent flow" --source flow
python3 scripts/search_library.py "milling toolpath" --source cam_milling
python3 scripts/search_library.py "mesh quality" --source plastics
python3 scripts/search_library.py "shell feature" --json
```

The search API can return source text context and source locators. A result is **not** an independent engineering diagnosis and is not proof that any CAD macro or API method works.

## Reproduce the index using installed source archives

```sh
python3 scripts/build_full_catalogue.py
python3 scripts/cache_source_pages.py
python3 scripts/build_search_db.py
python3 scripts/build_topic_dossiers.py
python3 scripts/generate_research_worklist.py
python3 scripts/audit_coverage.py
python3 -m unittest discover -s tests -v
```

The extraction uses the existing Windows 7-Zip binary and read-only installed Help archives. The extracted copyrighted Help pages and the full-text SQLite database are kept under ignored `.cache/` on this Ubuntu computer, not committed for external distribution. Compressed catalogue metadata, reports, worklist and scripts are versioned in **local Ubuntu Git only**.

## Remaining work

The whole documentation corpus is indexed, **not** a finished feature-by-feature causal diagnostic library. A real research/review runner or separate reviewing workers must use the bounded worklist and produce independently checked differential diagnoses, then validate selected tests on disposable SW2021 models. Feature inventory reconciliation and a Windows SOLIDWORKS Task Pane add-in also remain open. Do not create fake review approvals, claim full feature coverage from TOC counts, or run macros on production CAD.

The previous macro sources remain in `source/originals/` and `source/extracted/`, unexecuted. For the legacy six-job pilot queue: `python3 build.py status`; the local `ledger.json` is intentionally ignored by Git.
