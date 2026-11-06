import pickle,re,difflib,sys,json,hashlib
sys.path.insert(0,'/tmp/rel13')
from forza_template import render
num=re.compile(r'(-?\d+(?:\.\d+)?)')
def dec(x): return len(x.split('.')[1]) if '.' in x else 0
def tmpl_hunk(old,new):
    to=num.split(old); tn=num.split(new); out=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,to,tn,autojunk=False).get_opcodes():
        seg=tn[j1:j2]
        if tag=='equal': out+=seg; continue
        olds=[x for x in to[i1:i2] if num.fullmatch(x)]
        for x in seg:
            if not num.fullmatch(x): out.append(x); continue
            d=dec(x); v=float(x); r=None
            if x=='2580': r='@W@'
            elif x=='2490': r='@E:1830:F:0:2@'
            elif x=='1.34375': r='@K@'
            elif x=='330': r='@S@'
            elif x=='-330': r='@E:0:F:0:-1@'
            else:
                for o in olds:
                    dv=v-float(o)
                    if abs(dv-330)<1e-9: r='@E:%s:S:%d@'%(o,d); break
                    if abs(dv+330)<1e-9: r='@E:%s:F:%d:-1@'%(o,d); break
                    if abs(dv+240)<1e-9: r='@E:%s:F:%d:-1@'%(('%g'%(float(o)+90)),d); break
            out.append(r if r else x)
    return ''.join(out)
def templ_file(orig,new):
    a=orig.split('\n'); b=new.split('\n'); out=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=='equal': out+=b[j1:j2]
        else: out+=tmpl_hunk('\n'.join(a[i1:i2]),'\n'.join(b[j1:j2])).split('\n') if j2>j1 else []
    return '\n'.join(out)
new=pickle.load(open(sys.argv[1],'rb'))
files={}; bad=0
for f,t in sorted(new.items()):
    o=open('/tmp/fm6/fm6ui/'+f,'rb').read().decode('latin-1')
    assert not re.search(r'@(W|S|K|PR|TICKS|LTICKS)@|@E:',o),f
    tp=templ_file(o,t)
    if render(tp,2580)!=t: bad+=1; print('MISMATCH',f)
    files[f]={'sha256':hashlib.sha256(o.encode('latin-1')).hexdigest(),'full':tp}
print('files',len(files),'mismatch',bad)
# W=2560 sanity: no leftover 2580/1.34375 in changed regions
for f,v in files.items():
    r=render(v['full'],2560)
    if '2580' in r or '1.34375' in r or '2490' in r: print('LEFTOVER',f,[m.start() for m in re.finditer('2580|1.34375|2490',r)][:3])
json.dump(files,open('fm6_files.json','w'))
