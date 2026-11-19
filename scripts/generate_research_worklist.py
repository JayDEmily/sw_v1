#!/usr/bin/env python3
"""Generate a durable bounded research worklist without faking reviewed output.

One entry = one documentation topic awaiting capability/alias triage. A worker
must merge duplicates and distinguish UI features from API references.
"""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DOSSIERS=ROOT/"library/topic_dossiers.jsonl.gz"
WORKLIST=ROOT/"library/research_worklist.jsonl.gz"
REPORT=ROOT/"library/WORKLIST_REPORT.json"

def main():
    tasks=[]
    navigation_only=0
    with gzip.open(DOSSIERS,"rt",encoding="utf-8") as f:
        for line in f:
            item=json.loads(line)
            if item["scope"]!="in_scope":
                continue
            if not item["source_locator"]:
                navigation_only+=1
                continue
            title=item["title"]
            pid=hashlib.sha256(item["id"].encode("utf-8")).hexdigest()[:20]
            if item["content_status"]=="toc_only":status="blocked_missing_source"
            else:status="needs_diagnostic_research"
            tasks.append({
                "work_id":"sw21-"+pid,"topic_key":item["id"],"source":item["source"],
                "title":title,"breadcrumbs":item["breadcrumbs"],"member":item["source_locator"],
                "url":item["public_help_url"],"text_sha256":item["text_sha256"],
                "priority":1 if item["diagnostic_candidate"] else 2,
                "status":status,"reasoned_diagnosis_complete":False,
                "independent_review_complete":False,"runtime_validated":False,
                "instructions":"Determine whether this is a distinct selectable capability, subtopic or alias. Reopen exact source; document symptoms, competing causes, reversible discriminating tests, outcome meanings/limits and 2021 API availability when actually verified. Return blocked when unsupported. Independent review remains separate."
            })
    tasks.sort(key=lambda r:(r["priority"],r["source"],r["title"].casefold(),r["work_id"]))
    with WORKLIST.open("wb") as fd:
        with gzip.GzipFile(filename="",fileobj=fd,mode="wb",compresslevel=9,mtime=0) as gz:
            for t in tasks:gz.write((json.dumps(t,ensure_ascii=False,sort_keys=True)+"\n").encode())
    counts=Counter(t["status"] for t in tasks)
    report={"research_topic_jobs":len(tasks),"navigation_only_headings_not_queued":navigation_only,"by_status":dict(counts),
            "ready_for_independent_review":0,"finished_differential_diagnoses":0,
            "worklist_path":str(WORKLIST.relative_to(ROOT)),
            "worklist_sha256":hashlib.sha256(WORKLIST.read_bytes()).hexdigest(),
            "warning":"Worklist documents scope, not completed diagnosis or accepted review."}
    REPORT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    main()
