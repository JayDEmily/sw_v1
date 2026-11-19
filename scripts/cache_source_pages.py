#!/usr/bin/env python3
"""Cache locally installed SW2021 Help HTML pages, never the source CAD model."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from scan_archive_tocs import sources,prefix
import subprocess
import json
import sys
import time

ROOT=Path(__file__).resolve().parent.parent
CACHE=ROOT/".cache"/"help"
SEVEN="/mnt/c/Program Files/7-Zip/7z.exe"
def winpath(p):
    return subprocess.check_output(["wslpath","-w",str(p)],text=True).strip()
def extract(item):
    name,rel=item
    archive=prefix/rel
    dest=CACHE/name
    dest.mkdir(parents=True,exist_ok=True)
    cmd=[SEVEN,"x","-y","-r","-bso0","-bsp0","-bse1",
         "-o"+winpath(dest),winpath(archive),"*.htm","*.html"]
    started=time.monotonic()
    result=subprocess.run(cmd,capture_output=True,check=False)
    files=sum(1 for p in dest.rglob("*") if p.is_file() and p.suffix.lower() in (".htm",".html"))
    return {"name":name,"exit_code":result.returncode,"pages":files,
            "seconds":round(time.monotonic()-started,1),
            "message":result.stderr.decode("cp1252","replace")[-600:]}
def main():
    only=set(sys.argv[1:]) or set(sources)
    items=[x for x in sources.items() if x[0] in only and x[0]!="core"]
    CACHE.mkdir(parents=True,exist_ok=True)
    manifest=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(extract,item):item[0] for item in items}
        for f in as_completed(futures):
            result=f.result()
            manifest.append(result)
            print(json.dumps(result),flush=True)
    (CACHE/"CACHE_STATUS.json").write_text(json.dumps(sorted(manifest,key=lambda r:r["name"]),indent=2)+"\n")
    if any(x["exit_code"]!=0 for x in manifest):
        sys.exit(1)
if __name__=="__main__":
    main()
