"""Read-only SOLIDWORKS 2021 research helper. Python 3.8+, standard library."""
import argparse, html, json, os, re, tempfile, webbrowser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlsplit
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

ROOT = "https://help.solidworks.com/2021/english/SolidWorks/sldworks/"
# Each card: match expression, article slug, title, reason for showing it.
CARDS = [
 (r"3d.*spline|spline.*3d","HIDD_DVE_SKETCH_SPLINE_3D","3D spline controls","For a point or handle moving unexpectedly, inspect the relations on that selection."),
 (r"spline|curvature comb","t_Displaying_Curvature_Combs","Curvature combs","For an unexpected change of shape, inspect the curve itself before investigating a downstream feature."),
 (r"spline","r_Spline_Tools_Toolbar","Spline inspection tools","Find the commands for handles, inflections and minimum radius."),
 (r"3d.*(spline|sketch)","c_Sketch_Relations_in_3D_Sketches","3D sketch relations","Use the spatial relation guide rather than assuming a planar constraint applies."),
 (r"sketch|spline|constraint","c_Sketch_Status_Conventions","Sketch status","Separate an under-defined sketch from a solver conflict or invalid geometry."),
 (r"over.?defined|conflict|redundant","c_SketchXpert","SketchXpert","For conflicting relations, preview alternatives before accepting changes."),
 (r"shell","t_Shell_Feature_Diagnostics","Shell diagnostics","Distinguish failing-face diagnostics from checks on the entire body."),
 (r"shell|offset|knit|invalid face|edge gap","t_check_entity_assembly","Check Entity","Use the geometry check for gaps, short edges or small radii.")
]
class Headings(HTMLParser):
    def __init__(self):
        super().__init__(); self.tag=None; self.parts=[]; self.found=[]
    def handle_starttag(self,t,a):
        if t in ('h2','h3'): self.tag=t; self.parts=[]
    def handle_data(self,d):
        if self.tag: self.parts.append(d)
    def handle_endtag(self,t):
        if t==self.tag:
            s=' '.join(''.join(self.parts).split())
            if s and len(s)<100 and s not in self.found: self.found.append(s)
            self.tag=None

def read(url, headers=None):
    with urlopen(Request(url,headers=headers or {}),timeout=7) as r:
        return r.read(3000000).decode('utf-8','replace')

def anchor(url,title):
    return '<a href="%s">%s</a>'%(html.escape(url,quote=True),html.escape(title))

def card(c):
    _,slug,title,why=c; url=ROOT+slug+'.htm?format=P'
    try:
        parser=Headings(); parser.feed(read(url))
        status=('Page headings: '+' / '.join(parser.found[:4])) if parser.found else 'Page fetched; no section headings extracted.'
    except Exception: status='Live page unavailable; showing saved reference.'
    return '<p>'+anchor(url,title)+'<br>'+html.escape(why)+'<br><small>'+html.escape(status)+'</small></p>'

def search(q,key,official):
    try:
        u='https://api.search.brave.com/res/v1/web/search?'+urlencode({'q':q,'count':5})
        rows=json.loads(read(u,{'X-Subscription-Token':key,'Accept':'application/json'})).get('web',{}).get('results',[])
        out=[]
        for r in rows:
            url=r['url']; parts=urlsplit(url)
            if parts.scheme!='https': continue
            if official and (parts.hostname!='help.solidworks.com' or '/2021/' not in parts.path): continue
            out.append('<li>'+anchor(url,r['title'])+'<br>'+html.escape(html.unescape(re.sub('<[^>]+>','',r.get('description',''))))+'</li>')
        return '<ul>'+''.join(out)+'</ul>' if out else '<p>No matching results returned.</p>'
    except Exception: return '<p>Live search unavailable. Use the search link below.</p>'

def run(topic):
    topic=topic[:300]; key=os.environ.get('BRAVE_SEARCH_API_KEY')
    selected=[c for c in CARDS if re.search(c[0],topic,re.I)]
    s=['<!doctype html><meta charset=utf-8><title>Research this</title><style>body{max-width:52em;margin:3em auto;font:16px/1.5 Segoe UI,sans-serif}small{color:#555}</style>',
       '<h1>'+html.escape(topic)+'</h1><p>SOLIDWORKS 2021 research brief. References, not model findings.</p><h2>Matched help topics</h2>']
    with ThreadPoolExecutor(max_workers=5) as pool: s.extend(pool.map(card,selected))
    if not selected: s.append('<p>No curated module matched; use the searches below.</p>')
    for official,label,q in [(True,'More from 2021 Help','site:help.solidworks.com/2021/ '+topic),(False,'Wider web (versions may differ)','SOLIDWORKS 2021 '+topic)]:
        s.append('<h2>'+label+'</h2>')
        if key: s.append(search(q,key,official))
        else: s.append('<p>No search API configured; open the search manually.</p>')
        s.append(anchor('https://search.brave.com/search?'+urlencode({'q':q}),'Search: '+q))
    with tempfile.NamedTemporaryFile(suffix='.html',prefix='SW_research_',delete=False,mode='w',encoding='utf-8') as f:
        f.write(''.join(s))
    print(f.name); webbrowser.open(Path(f.name).as_uri())

if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('--job',type=Path); a.add_argument('topic',nargs='?'); args=a.parse_args()
    if args.job:
        topic=args.job.read_text(encoding='utf-16'); args.job.unlink()
    else: topic=args.topic or input('Public topic (e.g. 3D spline tangent): ')
    if topic.strip(): run(topic.strip())
