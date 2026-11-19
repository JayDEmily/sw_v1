#!/usr/bin/env python3
"""Read the *installed* SOLIDWORKS 2021 compiled Help table of contents.

No CAD, network, model runner, or installer is invoked. This script reads the
local CHM in a single 7-Zip stream and records TOC hierarchy/provenance only.
"""
import argparse
import hashlib
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_CHM = Path("/mnt/c/Program Files/SOLIDWORKS Corp/SOLIDWORKS/lang/english/sldworks.chm")
SEVENZIP = Path("/mnt/c/Program Files/7-Zip/7z.exe")

class TOCParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.li_stack = []
        self.ul_parents = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ul":
            self.ul_parents.append(self.li_stack[-1] if self.li_stack else None)
        elif tag == "li":
            parent = self.ul_parents[-1] if self.ul_parents else None
            idx = len(self.nodes)
            self.nodes.append({"id": idx, "parent": parent, "title": "", "local": "", "merge": ""})
            self.li_stack.append(idx)
        elif tag == "param" and self.li_stack:
            node = self.nodes[self.li_stack[-1]]
            name = attrs.get("name", "").lower()
            if name == "name":
                node["title"] = attrs.get("value", "")
            elif name in ("local", "merge"):
                node[name] = attrs.get("value", "")
    def handle_endtag(self, tag):
        if tag == "li" and self.li_stack:
            self.li_stack.pop()
        elif tag == "ul" and self.ul_parents:
            self.ul_parents.pop()

def member(chm, name):
    win = subprocess.check_output(["wslpath", "-w", str(chm)], text=True).strip()
    result = subprocess.run([str(SEVENZIP), "e", "-so", win, name],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=True)
    return result.stdout

def toc(chm, index_member="sldworks.hhc"):
    raw = member(chm, index_member)
    parser = TOCParser()
    parser.feed(raw.decode("cp1252", errors="replace"))
    for n in parser.nodes:
        path = []
        p = n["id"]
        while p is not None:
            path.append(parser.nodes[p]["title"])
            p = parser.nodes[p]["parent"]
        n["breadcrumbs"] = list(reversed(path))
    return raw, parser.nodes

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chm", type=Path, default=DEFAULT_CHM)
    p.add_argument("--member", default="sldworks.hhc")
    p.add_argument("--out", type=Path)
    p.add_argument("--roots", action="store_true")
    a = p.parse_args()
    raw, nodes = toc(a.chm, a.member)
    print("TOC member", a.member, "bytes", len(raw),
          "sha256", hashlib.sha256(raw).hexdigest(),
          "nodes", len(nodes), "unique local", len({n["local"].lower() for n in nodes if n["local"]}))
    if a.roots:
        for n in nodes:
            if n["parent"] is None or (n["parent"] is not None and nodes[n["parent"]]["parent"] is None):
                print(f'{len(n["breadcrumbs"]):2} {n["id"]:5} {n["title"][:85]}')
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with a.out.open("w", encoding="utf-8") as f:
            for n in nodes:
                f.write(json.dumps(n, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
