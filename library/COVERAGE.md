# SOLIDWORKS 2021 library — source coverage

**Scope:** installed English Design Help, API Help, Flow Simulation, CAM, Inspection and Plastics.
Electrical/PCB omitted; photorealistic Visualize workflows omitted per owner preference.

**Entries:** 18,234 TOC records; 17,954 with source text; 280 TOC-only.
**In-scope content:** 4,373 linked topic pages, 4,373 with readable text, 0 linked pages unresolved; plus 177 navigation-only headings.
A TOC record is not necessarily a unique designer-selectable feature, and source indexing is not diagnostic validation.
**Newly independently reviewed diagnostic cards: 0. Runtime-tested cards: 0.**
Earlier three pilot drafts remain unreviewed.

| Archive family | TOC entries | Source text | TOC only |
| --- | ---: | ---: | ---: |
| api | 10,353 | 10,350 | 3 |
| cam_api | 2,130 | 2,122 | 8 |
| cam_master | 5 | 4 | 1 |
| cam_milling | 455 | 402 | 53 |
| cam_tbm | 40 | 31 | 9 |
| cam_techdb | 246 | 208 | 38 |
| cam_techtips | 7 | 3 | 4 |
| cam_turning | 188 | 159 | 29 |
| core | 3,819 | 3,801 | 18 |
| flow | 372 | 370 | 2 |
| flow_api | 367 | 284 | 83 |
| inspection | 149 | 117 | 32 |
| inspection_quickstart | 12 | 12 | 0 |
| plastics | 91 | 91 | 0 |

## Source limitations and version distinctions

- Core Help has scope labels distinguishing modelling from adjacent/excluded chapters.
- API and CAM API references are indexed separately; matching titles do not establish callable method equivalence.
- Inspection's installed CHM internally references a 2019 TOC, so blanket 2021 applicability remains unverified.
- Every unresolved locator is in UNRESOLVED_SOURCE_LOCATORS.csv; structural headings and external merges are not presumed readable.
- Full text is in .cache/sw2021_search.sqlite, locally generated from installed archives and ignored by Git.
- The compressed topic dossiers contain source pointers, statuses and source hints, not complete independently reasoned diagnoses.

## Example queries

    python3 scripts/search_library.py 'shell fails'
    python3 scripts/search_library.py 'concentric mate'
    python3 scripts/search_library.py 'turbulent flow pressure drop' --source flow
    python3 scripts/search_library.py 'milling toolpath' --source cam_milling
    python3 scripts/search_library.py 'inspection balloon' --source inspection
    python3 scripts/search_library.py 'mesh quality' --source plastics
    python3 scripts/search_library.py 'Shell Feature' --json

## Rebuild from installed sources

    python3 scripts/build_full_catalogue.py
    python3 scripts/cache_source_pages.py
    python3 scripts/build_search_db.py
    python3 scripts/build_topic_dossiers.py
    python3 scripts/audit_coverage.py
    python3 -m unittest discover -s tests -v

Windows 7-Zip is used to extract local Help files; SOLIDWORKS itself and its macros are not launched.
