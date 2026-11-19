#!/usr/bin/env python3
"""Build a local, reproducible full-text SW2021 Help search DB.

Source pages remain on the user's computer under .cache; this is not
a reviewed diagnostic library or an API equivalence claim.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent.parent
INVENTORY=ROOT/"library/source_inventory.jsonl.gz"
DB=ROOT/".cache/sw2021_search.sqlite"
CACHE=ROOT/".cache/help"
TEXT_LIMIT=0  # 0 means no truncation of locally indexed Help text

class TextParser(HTMLParser):
    HIDE={"script","style","noscript","svg","head"}
    BLOCK={"p","li","h1","h2","h3","h4","td","th","tr","dd","dt","br","div","section"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden=0
        self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in self.HIDE: self.hidden+=1
        if tag in self.BLOCK and not self.hidden: self.parts.append("\n")
    def handle_endtag(self,tag):
        if tag in self.HIDE and self.hidden: self.hidden-=1
        if tag in self.BLOCK and not self.hidden: self.parts.append("\n")
    def handle_data(self,data):
        if not self.hidden: self.parts.append(data)
    def text(self):
        lines=[" ".join(l.split()) for l in "".join(self.parts).splitlines()]
        return "\n".join(l for l in lines if l)
def page_text(path):
    raw=path.read_bytes()
    head=raw[:1000].decode("latin-1","ignore").lower()
    match=re.search(r"charset\s*=\s*[\"']?([a-z0-9_-]+)",head)
    charset=match.group(1) if match else "windows-1252"
    try: content=raw.decode(charset,errors="replace")
    except LookupError: content=raw.decode("cp1252","replace")
    parser=TextParser()
    parser.feed(content)
    return parser.text(),hashlib.sha256(raw).hexdigest()

def build_paths(source):
    folder = ROOT/".cache/help_core" if source=="core" else CACHE/source
    if not folder.exists(): return {},{}
    paths={}
    names=defaultdict(list)
    for p in folder.rglob("*"):
        if not p.is_file(): continue
        rel=p.relative_to(folder).as_posix().lower()
        paths[rel]=p
        names[p.name.lower()].append(p)
    return paths,names

def resolve(row,cache):
    rel=unquote(row["slug"].split("#",1)[0].split("?",1)[0]).replace("\\","/").lstrip("/").lower()
    if not rel or rel.startswith(("http:","https:","mk:")) or ".." in rel.split("/"):
        return None
    paths,names=cache
    if rel in paths:return paths[rel]
    same=names.get(rel.rsplit("/",1)[-1],[])
    if len(same)==1:return same[0]
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",type=Path,default=DB)
    args=ap.parse_args()
    args.db.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(INVENTORY,"rt",encoding="utf-8") as f:
        rows=[json.loads(l) for l in f]
    caches={n:build_paths(n) for n in sorted(set(r["source"] for r in rows))}
    scratch=args.db.with_name(args.db.name+".rebuild.tmp")
    if scratch.exists(): raise RuntimeError("incomplete previous build; inspect "+str(scratch))
    c=sqlite3.connect(scratch)
    c.execute("PRAGMA journal_mode=DELETE")
    c.execute("PRAGMA synchronous=FULL")
    c.executescript("""
        CREATE TABLE topics(
          id INTEGER PRIMARY KEY, source TEXT NOT NULL, title TEXT NOT NULL,
          breadcrumbs TEXT NOT NULL, slug TEXT, url TEXT, scope TEXT NOT NULL,
          scope_reason TEXT, review_status TEXT NOT NULL, runtime_status TEXT NOT NULL,
          source_status TEXT NOT NULL, text_status TEXT NOT NULL, text_sha256 TEXT,
          body TEXT, toc_positions_json TEXT
        );
        CREATE VIRTUAL TABLE topic_fts USING fts5(
          title, breadcrumbs, body, content='topics',content_rowid='id',
          tokenize='unicode61 remove_diacritics 2'
        );
        CREATE INDEX idx_topic_source ON topics(source);
        CREATE INDEX idx_topic_scope ON topics(scope);
    """)
    counters=Counter()
    for i,row in enumerate(rows,1):
        path=resolve(row,caches[row["source"]])
        body=""
        digest=None
        if path:
            try: body,digest=page_text(path)
            except Exception as exc:
                counters["read_fail_"+row["source"]]+=1
        text_status = "source_text_indexed" if body else "toc_only"
        counters["total"]+=1
        counters[text_status]+=1
        counters[row["source"]+"_"+text_status]+=1
        c.execute("""INSERT INTO topics
          (id,source,title,breadcrumbs,slug,url,scope,scope_reason,review_status,
           runtime_status,source_status,text_status,text_sha256,body,toc_positions_json)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (i,row["source"],row["title"]," / ".join(row["breadcrumbs"]),
           row["slug"],row["url"],row["scope"],row["scope_reason"],
           row["review_status"],row["runtime_status"],row["evidence_status"],
           text_status,digest,body,json.dumps(row["toc_positions"])))
        if i%2000==0: print("indexed",i,flush=True)
    c.execute("INSERT INTO topic_fts(topic_fts) VALUES('rebuild')")
    c.commit()
    integrity=c.execute("PRAGMA integrity_check").fetchone()[0]
    c.close()
    if integrity!="ok": raise RuntimeError("rebuilt database integrity failure: "+str(integrity))
    os.replace(scratch,args.db)
    info={
      "indexed_records":counters["total"],
      "with_source_text":counters["source_text_indexed"],
      "toc_only":counters["toc_only"],
      "breakdown":dict(sorted(counters.items())),
      "db_path":str(args.db),"db_size":args.db.stat().st_size,
      "integrity_check":integrity,
      "assessment":"source-indexed, not diagnostic cards and not independently reviewed"
    }
    (ROOT/"library/SEARCH_BUILD_REPORT.json").write_text(json.dumps(info,indent=2)+"\n")
    print(json.dumps(info,indent=2))

if __name__=="__main__":
    main()
