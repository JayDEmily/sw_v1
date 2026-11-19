#!/usr/bin/env python3
"""Document exact library source coverage and unresolved locators."""
import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/".cache/sw2021_search.sqlite"
OUT=ROOT/"library"

def main():
    c=sqlite3.connect("file:"+str(DB)+"?mode=ro",uri=True)
    grouped=c.execute("""SELECT source,scope,COUNT(*),
            SUM(CASE WHEN text_status='source_text_indexed' THEN 1 ELSE 0 END)
            FROM topics GROUP BY source,scope ORDER BY source,scope""").fetchall()
    summaries={}
    for source,scope,n,have in grouped:
        s=summaries.setdefault(source,{"total":0,"indexed":0,"missing":0,"by_scope":{}})
        s["total"]+=n;s["indexed"]+=have;s["missing"]+=n-have
        s["by_scope"][scope]={"total":n,"indexed":have,"missing":n-have}
    unknown=c.execute("""SELECT source,title,slug,scope
                         FROM topics WHERE text_status='toc_only' ORDER BY source,title""").fetchall()
    with (OUT/"UNRESOLVED_SOURCE_LOCATORS.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f,lineterminator=chr(10))
        writer.writerow(["source","title","local_member","scope"])
        writer.writerows(unknown)
    totals=Counter()
    for s in summaries.values():
        totals["total"]+=s["total"]
        totals["indexed"]+=s["indexed"]
        totals["missing"]+=s["missing"]
    linked_in_scope=c.execute("SELECT COUNT(*) FROM topics WHERE scope='in_scope' AND length(trim(coalesce(slug,'')))>0").fetchone()[0]
    missing_linked=c.execute("SELECT COUNT(*) FROM topics WHERE scope='in_scope' AND text_status='toc_only' AND length(trim(coalesce(slug,'')))>0").fetchone()[0]
    navigation_only=sum(s["by_scope"].get("in_scope",{}).get("total",0) for s in summaries.values())-linked_in_scope
    lines=[
      "# SOLIDWORKS 2021 library — source coverage",
      "",
      "**Scope:** installed English Design Help, API Help, Flow Simulation, CAM, Inspection and Plastics.",
      "Electrical/PCB omitted; photorealistic Visualize workflows omitted per owner preference.",
      "",
      f"**Entries:** {totals['total']:,} TOC records; {totals['indexed']:,} with source text; {totals['missing']:,} TOC-only.",
      f"**In-scope content:** {linked_in_scope:,} linked topic pages, {linked_in_scope-missing_linked:,} with readable text, {missing_linked:,} linked pages unresolved; plus {navigation_only:,} navigation-only headings.",
      "A TOC record is not necessarily a unique designer-selectable feature, and source indexing is not diagnostic validation.",
      "**Newly independently reviewed diagnostic cards: 0. Runtime-tested cards: 0.**",
      "Earlier three pilot drafts remain unreviewed.",
      "",
      "| Archive family | TOC entries | Source text | TOC only |",
      "| --- | ---: | ---: | ---: |"]
    for name,s in sorted(summaries.items()):
        lines.append(f'| {name} | {s["total"]:,} | {s["indexed"]:,} | {s["missing"]:,} |')
    lines += [
      "",
      "## Source limitations and version distinctions",
      "",
      "- Core Help has scope labels distinguishing modelling from adjacent/excluded chapters.",
      "- API and CAM API references are indexed separately; matching titles do not establish callable method equivalence.",
      "- Inspection's installed CHM internally references a 2019 TOC, so blanket 2021 applicability remains unverified.",
      "- Every unresolved locator is in UNRESOLVED_SOURCE_LOCATORS.csv; structural headings and external merges are not presumed readable.",
      "- Full text is in .cache/sw2021_search.sqlite, locally generated from installed archives and ignored by Git.",
      "- The compressed topic dossiers contain source pointers, statuses and source hints, not complete independently reasoned diagnoses.",
      "",
      "## Example queries",
      "",
      "    python3 scripts/search_library.py 'shell fails'",
      "    python3 scripts/search_library.py 'concentric mate'",
      "    python3 scripts/search_library.py 'turbulent flow pressure drop' --source flow",
      "    python3 scripts/search_library.py 'milling toolpath' --source cam_milling",
      "    python3 scripts/search_library.py 'inspection balloon' --source inspection",
      "    python3 scripts/search_library.py 'mesh quality' --source plastics",
      "    python3 scripts/search_library.py 'Shell Feature' --json",
      "",
      "## Rebuild from installed sources",
      "",
      "    python3 scripts/build_full_catalogue.py",
      "    python3 scripts/cache_source_pages.py",
      "    python3 scripts/build_search_db.py",
      "    python3 scripts/build_topic_dossiers.py",
      "    python3 scripts/audit_coverage.py",
      "    python3 -m unittest discover -s tests -v",
      "",
      "Windows 7-Zip is used to extract local Help files; SOLIDWORKS itself and its macros are not launched.",
      ""]
    (OUT/"COVERAGE.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps({"totals":dict(totals),"by_source":summaries,
                      "unresolved_sample":unknown[:18]},indent=2,ensure_ascii=False))
    c.close()
if __name__=="__main__":
    main()
