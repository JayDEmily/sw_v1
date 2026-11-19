"""Single-coordinator queue. Run from a dedicated, persistent workspace. Stdlib only."""
import json,sys,subprocess,os,re
from pathlib import Path
db=Path('ledger.json')
def save():
    t=db.with_suffix('.tmp');t.write_text(json.dumps(D,indent=2),encoding='utf8');os.replace(t,db)
def item(i,k,title,url=''):
    return dict(id=i,kind=k,title=title,url=url,state='todo',history=[])
roots=[('parts','Part modelling'),('assemblies','Assembly modelling'),('mates','Mate families and subtypes')]
pilots=[('shell','Shell'),('spline-3d','3D spline'),('mate-concentric','Concentric mate')]
D=json.loads(db.read_text(encoding='utf8')) if db.exists() else {i:item(i,k,t) for k,ls in [('card',pilots),('discover',roots)] for i,t in ls}
contracts={
'discover':{'sources':['2021 official URL + section + what inventory it establishes'],'children':[{'id':'canonical-slug','kind':'discover or card','title':'name','url':'2021 official URL'}],'exclusions':['item and reason'],'reconciliation':'second inventory comparison, aliases, unresolved differences'},
'card':{'sources':['2021 official URL + section + paraphrased fact; number by position'],'symptoms':['observable symptom'],'probes':[{'test':'procedure or explicit diagnostic limitation','mode':'read_only_api/disposable_copy/ui_only/unknown','conditions':'inputs, configuration, units, side effects','rivals':'which explanations it distinguishes','outcomes':['observation -> meaning, limit, next step'],'basis':'documented or hypothesis; cite source numbers','member':'exact 2021 signature, or not applicable/unverified'}],'limitations':['what cannot be concluded']},
'review':{'verdict':'approve or revise','checks':['URL + section reopened, comparison made and result'],'reason':'specific justification or correction'}}
def current():
    return next((v for v in D.values() if v['state'] in ('todo','review')),None)
def prompt(v):
    phase='review' if v['state']=='review' else v['kind']
    return (Path(__file__).with_name('WORK_ORDER.md').read_text(encoding='utf8')+'\nJOB '+json.dumps(v)+'\nCanonical IDs already known: '+', '.join(D)+'\nPHASE '+phase+'\nReturn {"id":"'+v['id']+'","phase":"'+phase+'","data":'+json.dumps(contracts[phase])+'}. If blocked use data={"blocked":"specific reason"}.')
def accept(r):
    v=current()
    if not v: raise ValueError('queue empty')
    i=v['id']; k='review' if v['state']=='review' else v['kind']; x=r['data']
    if (r['id'],r['phase'])!=(i,k): raise ValueError('stale or wrong reply')
    if x.get('blocked'): v['state']='blocked'
    else:
        for field in contracts[k]:
            if field not in x: raise ValueError('missing '+field)
        if k=='discover':
            for c in x['children']:
                if not re.fullmatch('[a-z0-9][a-z0-9-]*',c['id']) or c['kind'] not in ('card','discover') or not c['title'] or not c['url']: raise ValueError('invalid child')
        if k=='card' and (not x['sources'] or not x['probes']): raise ValueError('missing evidence or probes')
        if k=='review':
            if x['verdict'] not in ('approve','revise') or not x['checks']: raise ValueError('bad review')
            v['state']='done' if x['verdict']=='approve' else ('blocked' if len(v['history'])>=5 else 'todo')
            if v['state']=='done' and v['kind']=='discover':
                for c in v['history'][-1]['data']['children']:
                    if c['id'] not in D: D[c['id']]=item(**dict(i=c['id'],k=c['kind'],title=c['title'],url=c['url']))
        else: v['state']='review'
    v['history'].append(r);save()
def main(a):
    save()
    if not a or a[0]=='status':
        from collections import Counter
        print(dict(Counter(v['state'] for v in D.values())))
        for v in D.values():
            if v['state']=='blocked': print(v['id'],v['history'][-1]['data'])
    elif a[0]=='next':print(prompt(current()) if current() else 'No queued work. Check blocked items.')
    elif a[0]=='accept':accept(json.loads(Path(a[1]).read_text(encoding='utf8')))
    elif a[0]=='run':
        # Budget is a bound on calls, not hours. Worker reads one prompt on stdin.
        if len(a)<3:raise SystemExit('run MAX_CALLS EXECUTABLE [ARGS...]')
        for _ in range(int(a[1])):
            if not current(): break
            out=subprocess.run(a[2:],input=prompt(current()),text=True,encoding='utf8',capture_output=True,timeout=1800,check=True)
            accept(json.loads(out.stdout))
    elif a[0]=='retry' and D[a[1]]['state']=='blocked':D[a[1]]['state']='todo';save()
    else:raise SystemExit('status | next | accept reply.json | run MAX_CALLS EXECUTABLE [ARGS...] | retry blocked-id')
if __name__=='__main__':main(sys.argv[1:])
