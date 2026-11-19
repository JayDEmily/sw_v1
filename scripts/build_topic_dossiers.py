#!/usr/bin/env python3
"""Prepare a traceable source dossier for every indexed CHM topic.

A dossier is NOT an independently reviewed diagnostic card. This process
does not invent hypotheses, instructions, tests, or API signatures.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import gzip
import hashlib
import json
import re
import sqlite3

ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/".cache/sw2021_search.sqlite"
OUT=ROOT/"library/topic_dossiers.jsonl.gz"
REPORT=ROOT/"library/DOSSIER_REPORT.json"
SIGNAL=re.compile(r"\b(error|fail(?:ure|ed|s|ing)?|diagnos(?:is|tic)|troubleshoot|problem|fix(?:ing)?|repair|conflict|over.?defin|invalid|warning|resolve|solve)\b",re.I)

def hint(body,title):
    lines=[x.strip() for x in body.splitlines() if x.strip()]
    # Choose an actual source line that directly indicates diagnostic content.
    for line in lines[1:]:
        if SIGNAL.search(line) and len(line)>25:
            return " ".join(line.split())[:210]
    return ""
def main():
    c=sqlite3.connect("file:"+str(DB)+"?mode=ro",uri=True)
    cursor=c.execute("""SELECT source,title,breadcrumbs,slug,url,scope,scope_reason,
                               source_status,text_status,review_status,runtime_status,
                               text_sha256,body FROM topics ORDER BY id""")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    counts=Counter()
    with OUT.open("wb") as fd:
        with gzip.GzipFile(filename="",fileobj=fd,mode="wb",compresslevel=9,mtime=0) as g:
            for row in cursor:
                (source,title,breadcrumbs,slug,url,scope,reason,source_status,
                 text_status,review_status,runtime_status,digest,body)=row
                title_signal=bool(SIGNAL.search(title))
                source_hint=hint(body or "",title) if title_signal else ""
                dossier={
                    "id":source+":"+slug.lower() if slug else source+":"+title.lower(),
                    "source":source,"title":title,"breadcrumbs":breadcrumbs,
                    "source_locator":slug,"public_help_url":url,"scope":scope,
                    "scope_reason":reason,"text_sha256":digest,
                    "content_status":text_status,"research_status":"source_extracted_only",
                    "review_status":review_status,"runtime_status":runtime_status,
                    "diagnostic_candidate":title_signal,
                    "verbatim_source_hint":source_hint,
                    "hypotheses":[],"diagnostic_tests":[],
                    "unknowns":["Competing causes and discriminating test not independently researched"] if title_signal else [],
                }
                counts["total"]+=1
                counts[scope]+=1
                if title_signal:counts["diagnostic_title_signals"]+=1
                if source_hint:counts["diagnostic_source_hints"]+=1
                g.write((json.dumps(dossier,ensure_ascii=False,sort_keys=True)+"\n").encode())
    c.close()
    report={
        "records":counts["total"],"in_scope":counts["in_scope"],
        "reference_only":counts["reference_only"],"excluded_or_adjacent":counts["excluded_or_adjacent"],
        "diagnostic_title_signals":counts["diagnostic_title_signals"],
        "diagnostic_source_hints":counts["diagnostic_source_hints"],
        "reviewed_diagnostic_cards_generated":0,
        "runtime_validated_diagnostic_cards_generated":0,
        "assessment":"Complete navigation dossiers; differential diagnoses and tests require reasoned source-backed work.",
        "file":str(OUT.relative_to(ROOT)), "size_bytes":OUT.stat().st_size,
        "sha256":hashlib.sha256(OUT.read_bytes()).hexdigest()
    }
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
