#!/usr/bin/env python3
"""Build a lossless TOC navigation catalogue from installed SW2021 Help archives.

This inventories *documentation entries*, not feature behaviour or independently
reviewed diagnostic cards. It does not copy full copyrighted Help text.
"""
from __future__ import annotations
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from index_help_toc import toc
from scan_archive_tocs import prefix, sources, check

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "library"
SOURCE_ROOT = "https://help.solidworks.com/2021/english/SolidWorks/sldworks/"
CORE_RELEVANT = {
    "User Interface", "Fundamentals", "Assemblies", "Configurations",
    "SOLIDWORKS Costing", "Design Studies in SOLIDWORKS", "Import and Export",
    "Model Display", "Mold Design", "Motion Studies", "Parts and Features",
    "Routing", "Sheet Metal", "Sketching", "Tolerancing", "TolAnalyst",
    "Toolbox", "SOLIDWORKS Utilities", "Weldments and Structure System",
    "Troubleshooting", "Moving from 2D to 3D", "SOLIDWORKS File Utilities"
}
CORE_EXCLUSIONS = {
    "Detailing and Drawings": "out-of-scope drawings",
    "CircuitWorks": "PCB excluded by owner",
    "Simulation": "Simulation not established; Flow Simulation separately in scope",
    "SimulationXpress": "SimulationXpress distinct from Flow Simulation",
    "SOLIDWORKS MBD": "model-based definition not included in modelling-core scope",
    "3DEXPERIENCE Add-Ins": "external platform not in initial research scope",
    "Administration": "administration, not modelling diagnosis",
    "SOLIDWORKS Sustainability": "specialist module not explicitly requested",
    "DFMXpress": "not explicitly requested",
    "DriveWorksXpress": "not explicitly requested",
    "FloXpress": "distinct from licensed Flow Simulation",
    "SLDXML Data Exchange": "outside defined feature families",
}
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    variants = []
    source_manifest = []
    available = [(n,rel) for n,rel in sources.items() if (prefix/rel).is_file()]
    toc_info = {n:check((n,rel))[2] for n,rel in available}
    for name,rel in available:
        path = prefix/rel
        members = toc_info[name]
        base = {
            "source": name, "archive_path": str(path), "archive_name": path.name,
            "archive_sha256": sha256(path), "archive_size": path.stat().st_size,
            "toc_members": members,
            "note": "2019.hhc internal title" if name=="inspection" else "",
            "status": "installed_archived_source"
        }
        source_manifest.append(base)
        for member_name in members:
            raw, nodes = toc(path, member_name)
            base.setdefault("toc_sha256",{})[member_name]=hashlib.sha256(raw).hexdigest()
            base.setdefault("toc_entries",{})[member_name]=len(nodes)
            for node in nodes:
                title = " ".join(node["title"].split())
                crumbs = [" ".join(c.split()) for c in node["breadcrumbs"]]
                group = crumbs[0] if crumbs else ""
                if name=="core":
                    scope = "in_scope" if group in CORE_RELEVANT else "excluded_or_adjacent"
                    reason = "" if scope=="in_scope" else CORE_EXCLUSIONS.get(group,"not part of requested modelling scope")
                elif name in ("api","flow_api","cam_api"):
                    scope,reason="reference_only","API catalogue; UI and API entries must not be equated"
                else:
                    scope,reason="in_scope","module requested by owner"
                local = node["local"].replace("\\","/")
                if name=="core" and local:
                    url = SOURCE_ROOT + local.lstrip("/")
                else:
                    url = None
                variants.append({
                    "source":name, "toc":member_name, "toc_id":node["id"], "parent":node["parent"],
                    "title": title, "breadcrumbs": crumbs, "slug":local,
                    "merged_to":node["merge"], "url":url,
                    "scope":scope, "scope_reason":reason, "evidence_status":"source_toc_indexed",
                    "review_status":"unreviewed","runtime_status":"untested"
                })
            print(name, member_name, "entries",len(nodes))
    # Deduplicate TOC aliases without losing their original locations.
    uniques = {}
    for row in variants:
        key=(row["source"], row["slug"].lower()) if row["slug"] else (row["source"], row["toc"], "TOC:" + str(row["toc_id"]))
        if key not in uniques:
            uniques[key]={k:v for k,v in row.items() if k!="toc_id" and k!="parent"}
            uniques[key]["toc_positions"]=[]
        uniques[key]["toc_positions"].append({"toc":row["toc"],"toc_id":row["toc_id"],"parent":row["parent"],"breadcrumbs":row["breadcrumbs"]})
    inventory = list(uniques.values())
    inventory.sort(key=lambda r:(r["source"],r["toc"],r["title"].lower(),r["slug"].lower()))
    fn=OUT/"source_inventory.jsonl.gz"
    with fn.open("wb") as fd:
        with gzip.GzipFile(filename="",fileobj=fd,mode="wb",compresslevel=9,mtime=0) as g:
            for row in inventory:
                g.write((json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n").encode())
    manifest={"schema":1,"source_kind":"installed CHM TOC, not source text",
              "version":"SOLIDWORKS 2021 SP1 installation",
              "records_total":len(variants),"unique_entries":len(inventory),
              "source_archives":source_manifest,
              "counts_by_source":dict(Counter(x["source"] for x in inventory)),
              "counts_by_scope":dict(Counter(x["scope"] for x in inventory)),
              "help_inventory_file":str(fn.relative_to(ROOT)),
              "content_research_complete":False,"independent_review_complete":False}
    (OUT/"SOURCE_CATALOGUE_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TOTAL positions",len(variants),"unique entries",len(inventory),
          "in scope",manifest["counts_by_scope"].get("in_scope",0),
          "gzip bytes",fn.stat().st_size)
    print("by source",manifest["counts_by_source"])

if __name__=="__main__":
    main()
