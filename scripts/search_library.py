#!/usr/bin/env python3
"""Read-only search of the local SW2021 source-indexed library.

For future task-pane integration the --json result contains stable fields;
do not treat a source-indexed hit as a reviewed diagnosis.
"""
import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/".cache/sw2021_search.sqlite"

def find(query,limit=10,scope="in_scope",source=None,db=DB):
    terms=re.findall(r"[^\W_]+",query.lower(),re.UNICODE)[:12]
    if not terms:
        return []
    match=" OR ".join('"' + x.replace('"','') + '"' for x in terms)
    where=["topic_fts MATCH ?"]
    params=[match]
    if scope!="all":
        where.append("t.scope=?")
        params.append(scope)
    if source:
        where.append("t.source=?")
        params.append(source)
    params.append(limit)
    conn=sqlite3.connect("file:"+str(db)+"?mode=ro",uri=True)
    try:
        rows=conn.execute("""
          SELECT t.id, t.source, t.title, t.breadcrumbs, t.slug, t.url,
                 t.scope, t.source_status, t.text_status, t.review_status,
                 t.runtime_status, t.text_sha256,
                 snippet(topic_fts,2,'[',']',' … ',20) AS evidence_snippet,
                 bm25(topic_fts, 12.0, 4.0, 1.0) AS relevance
          FROM topic_fts JOIN topics t ON t.id=topic_fts.rowid
          WHERE """+" AND ".join(where)+"""
          ORDER BY relevance ASC LIMIT ?""",params).fetchall()
        fields=["id","source","title","breadcrumbs","slug","url","scope",
                "source_status","text_status","review_status","runtime_status",
                "text_sha256","evidence_snippet","relevance"]
        return [dict(zip(fields,row)) for row in rows]
    finally:
        conn.close()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("query",help="Search phrase, e.g. shell fails")
    parser.add_argument("--source")
    parser.add_argument("--scope",choices=("in_scope","all","reference_only","excluded_or_adjacent"),default="in_scope")
    parser.add_argument("--limit",type=int,default=10)
    parser.add_argument("--json",action="store_true")
    a=parser.parse_args()
    result=find(a.query,max(1,min(a.limit,100)),a.scope,a.source)
    if a.json:
        print(json.dumps({"query":a.query,"reviewed":False,
                          "runtime_tested":False,"results":result},indent=2,ensure_ascii=False))
    else:
        print(f"Source-indexed evidence for {a.query!r}; no results claim independent review or CAD runtime validation.")
        for i,row in enumerate(result,1):
            print(f'{i}. [{row["source"]}] {row["title"]} — {row["breadcrumbs"]}')
            if row["url"]:print("   2021 URL:",row["url"])
            else:print("   local Help member:",row["slug"])
            print("   Index:",row["text_status"],"Review:",row["review_status"],"Runtime:",row["runtime_status"])
            snip=" ".join((row["evidence_snippet"] or "").split())[:250]
            if snip:print("   Context:",snip)

if __name__=="__main__":
    main()
