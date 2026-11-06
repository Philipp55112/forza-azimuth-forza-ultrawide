import xml.parsers.expat,re,pickle,os,glob,sys
S=330
def margin(s):
    if s is None: return [0,0,0,0]
    try: v=[float(x) for x in s.replace(' ','').split(',')]
    except: return None
    if len(v)==1: return v*4
    if len(v)==2: return [v[0],v[1],v[0],v[1]]
    if len(v)==4: return v
    return None
def fmt(v): return ','.join(('%g'%x) for x in v)
PASS={'Grid','ContentControl','Border','local:ZPanel','StackPanel'}
def scan(text):
    data=text.encode('latin-1'); edits=[]; stack=[]
    p=xml.parsers.expat.ParserCreate(encoding='ISO-8859-1')
    def start(name,attrs):
        pos=p.CurrentByteIndex
        parent=stack[-1] if stack else None
        if '.' in name.split(':')[-1]:   # property element e.g. Grid.ColumnDefinitions
            if parent is not None and name.endswith('.ColumnDefinitions'): parent['cols']=True
            stack.append({'full':False,'prop':True,'name':name}); return
        st=attrs.get('Style','')
        full=False
        if re.search(r'StaticResource (BodyGridStyle|BodyGridNascarStyle)\}',st) and parent is not None and not parent.get('intemplate'):
            full=True
        elif parent and parent['full'] and not parent.get('prop'):
            ok_parent = parent['tag'] in PASS and not parent.get('cols') and not (parent['tag']=='StackPanel' and parent.get('orient')=='Horizontal')
            if ok_parent and 'Grid.Column' not in attrs:
                ha=attrs.get('HorizontalAlignment','Stretch'); m=margin(attrs.get('Margin'))
                if m is not None:
                    if ha=='Stretch' and 'Width' not in attrs and m[0]==0 and m[2]==0: full=True
                    elif attrs.get('x:Name') in ('Grid_TitleOptionListContainer','Grid_ListFocus','Grid_ColorSlidersContainer','Grid_OpacitySliderContainer') and ha in('Stretch','Center') and attrs.get('Width')=='{StaticResource MaxSceneWidth}' and m[0]==0 and m[2]==0: edits.append((pos,'W',m,name,attrs.get('x:Name')))
                    elif ha=='Right' and m[2]<=0: edits.append((pos,'R',m,name,attrs.get('x:Name')))
                    elif ha=='Left' and m[0]<=0 and attrs.get('x:Name')!='Rectangle_FadeMask': edits.append((pos,'L',m,name,attrs.get('x:Name')))
        stack.append({'full':full,'tag':name,'orient':attrs.get('Orientation','Vertical'),'intemplate':(parent or {}).get('intemplate') or name in('ControlTemplate','DataTemplate','Style')})
    def end(name): stack.pop()
    p.StartElementHandler=start; p.EndElementHandler=end
    p.Parse(data,True)
    out=text
    for pos,side,m,name,nm in sorted(edits,key=lambda e:-e[0]):
        j=out.index('>',pos); tag=out[pos:j]
        nmv=list(m)
        if side=='R': nmv[2]=m[2]-S
        elif side=='L': nmv[0]=m[0]-S
        else:
            nmv[0]=m[0]-S; nmv[2]=m[2]-S; tag=tag.replace('Width="{StaticResource MaxSceneWidth}"','Width="{StaticResource FullSceneWidth}"',1)
        if re.search(r'\sMargin="[^"]*"',tag): tag2=re.sub(r'(\sMargin=")[^"]*(")',lambda x:x.group(1)+fmt(nmv)+x.group(2),tag,count=1)
        else:
            mm=re.match(r'<[\w:.]+',tag); tag2=tag[:mm.end()]+' Margin="%s"'%fmt(nmv)+tag[mm.end():]
        out=out[:pos]+tag2+out[j:]
    return out,edits
if __name__=='__main__':
    new=pickle.load(open(sys.argv[1],'rb'))
    tot=0
    for p_ in sorted(glob.glob('/tmp/fm6/fm6ui/Scenes/WPF/F*.xaml')):
        f='Scenes/WPF/'+os.path.basename(p_)
        if re.match(r'Scenes/WPF/F7(0|1)\d_',f): continue
        t=new.get(f) or open(p_,'rb').read().decode('latin-1')
        try: o,e=scan(t)
        except Exception as ex: print('ERR',f,ex); continue
        if e:
            tot+=len(e); new[f]=o
            print(f.split('/')[-1][:34].ljust(34),', '.join('%s:%s'%(s,n or nm) for _,s,_,nm,n in e)[:200])
    print('total',tot)
    pickle.dump(new,open(sys.argv[2],'wb'))
