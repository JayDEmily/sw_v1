#!/usr/bin/env python3
"""Find available TOC members in installed help archives without modifying them."""
from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor

prefix=Path("/mnt/c/Program Files/SOLIDWORKS Corp")
sources={
"core":"SOLIDWORKS/lang/english/sldworks.chm",
"api":"SOLIDWORKS/api/sldworksapi.chm",
"flow":"SOLIDWORKS Flow Simulation/lang/english/FloWorks.chm",
"flow_api":"SOLIDWORKS Flow Simulation/lang/english/CFWAPI.chm",
"cam_master":"SOLIDWORKS CAM/Lang/English/master.chm",
"cam_milling":"SOLIDWORKS CAM/Lang/English/milling.chm",
"cam_turning":"SOLIDWORKS CAM/Lang/English/turning.chm",
"cam_techdb":"SOLIDWORKS CAM/Lang/English/techdb.chm",
"cam_tbm":"SOLIDWORKS CAM/Lang/English/tbm.chm",
"cam_techtips":"SOLIDWORKS CAM/Lang/English/techtips.chm",
"cam_api":"SOLIDWORKS CAM/Lang/English/swcamapihelp.chm",
"inspection":"SOLIDWORKS Inspection/PDF/en/solidworks inspection standalone.chm",
"inspection_quickstart":"SOLIDWORKS Inspection/PDF/solidworks inspection quick start.chm",
"plastics":"SOLIDWORKS Plastics/Document/english/swplastics.chm",
}
def check(item):
    name,rel=item; src=prefix/rel
    if not src.is_file(): return name, "MISSING", [],0
    win=subprocess.check_output(["wslpath","-w",str(src)],text=True).strip()
    out=subprocess.run(["/mnt/c/Program Files/7-Zip/7z.exe","l","-ba",win],
                       capture_output=True,check=True).stdout.decode("cp1252","replace")
    found=[]
    for line in out.splitlines():
        if line.lower().endswith(".hhc"):
            found.append(line.split(maxsplit=2)[-1].strip())
    return name,src.name,found,src.stat().st_size
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        for name,filename,found,size in pool.map(check,sources.items()):
            print(f"{name:23} {size:>10}  {filename:34} TOCs={found}")
