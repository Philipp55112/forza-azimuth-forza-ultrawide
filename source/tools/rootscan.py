import re,os,glob,collections
UI='/tmp/fm6/fm6ui/Scenes/WPF'
res={}
for f in sorted(glob.glob(UI+'/F*.xaml')):
    L=open(f,encoding='latin-1').read().split('\n')
    r=[i for i,l in enumerate(L) if 'x:Name="LayoutRoot"' in l and l.lstrip().startswith('<local:ZPanel')]
    if not r: continue
    i0=r[0]; ind=len(L[i0])-len(L[i0].lstrip()); ch=[]
    for i in range(i0+1,len(L)):
        l=L[i]; s=l.lstrip(); d=len(l)-len(s)
        if s.startswith('</local:ZPanel') and d==ind: break
        if d==ind+4 and s.startswith('<') and not s.startswith('</') and not s.startswith('<!--'):
            # gather tag text until '>'
            j=i; t=l
            while '>' not in t and j+1<len(L): j+=1; t+=' '+L[j].strip()
            ch.append((i,t.strip()))
    res[os.path.basename(f)]=(L[i0].strip(),ch)
import pickle; pickle.dump(res,open('/tmp/fm6/rootkids.pkl','wb'))
cnt=collections.Counter()
for fn,(root,ch) in res.items():
    for i,t in ch:
        tag=t.split()[0]
        pos='L' if re.search(r'Canvas\.Left="(?!0")',t) else 'R' if re.search(r'Canvas\.Right="(?!0")',t) else 'M' if re.search(r'\bMargin="[1-9]',t) else 'S' if 'GridStyle}' in t else '-'
        cnt[pos]+=1
print(len(res),cnt)
