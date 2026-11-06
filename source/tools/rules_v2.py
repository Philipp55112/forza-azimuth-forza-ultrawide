import re,os,pickle,glob
UI='/tmp/fm6/fm6ui'; W=2580; S=(W-1920)//2; C=90
def rd(f): return open(os.path.join(UI,f),'rb').read().decode('latin-1')
new={}; log=[]
def sub1(t,old,newv,f,count=1):
    n=t.count(old); assert n==count,(f,old[:80],n); log.append((f,old[:60],newv[:60]))
    return t.replace(old,newv)
R='Resources/'; Sc='Scenes/WPF/'
# 1 SizeKeys
f=R+'Global_SizeKeys.xaml'; t=rd(f)
t=sub1(t,'<System:Double x:Key="MaxSceneWidth">1920</System:Double>','<System:Double x:Key="MaxSceneWidth">1920</System:Double>\r\n    <System:Double x:Key="FullSceneWidth">%d</System:Double>'%W,f)
for key in ('HeaderGridStyle','BodyGridStyle','BodyGridNascarStyle','FooterGridStyle'):
    old='<Style x:Key="%s" TargetType="{x:Type Grid}">'%key
    t=sub1(t,old,old+'\r\n        <Setter Property="Canvas.Left" Value="%d"/>'%S,f)
i=t.index('x:Key="FullScreenZPanelStyle"'); j=t.index('MaxSceneWidth',i)
t=t[:j]+'FullSceneWidth'+t[j+len('MaxSceneWidth'):]
new[f]=t
# 2 DefaultControlStyles: background grids full width
f=R+'Global_DefaultControlStyles.xaml'; t=rd(f)
neg='Margin="-%d,0,-%d,0" '%(S,S)
t,n1=re.subn(r'<Grid x:Name="Grid_HeaderBg" ',r'<Grid x:Name="Grid_HeaderBg" '+neg,t)
t,n2=re.subn(r'<Grid x:Name="Grid_BodyBg" ',r'<Grid x:Name="Grid_BodyBg" '+neg,t)
t,n3=re.subn(r'<Grid x:Name="Grid_Bg" Tag=',r'<Grid x:Name="Grid_Bg" '+neg+'Tag=',t)
log.append((f,'bg grids',(n1,n2,n3))); new[f]=t
# 3 DecorationStyles dialogs
f=R+'Global_DecorationStyles.xaml'; t=rd(f)
L=t.split('\n')
for k in (897,899,962,1026,1028,1092,1094,1095):
    l=L[k-1]; assert 'MaxSceneWidth' in l,(k,l[:80]); L[k-1]=l.replace('{StaticResource MaxSceneWidth}','{StaticResource FullSceneWidth}',1)
for k in (1029,):
    l=L[k-1]; assert 'Canvas.Left="0"' in l; L[k-1]=l.replace('Canvas.Left="0"','Canvas.Left="%d"'%S,1)
l=L[1102-1]; assert 'Canvas.Left="0"' in l and 'Width="1920"' in l; L[1102-1]=l.replace('Canvas.Left="0"','Canvas.Left="%d"'%S,1)
l=L[733-1]; assert '"1920"' in l; L[733-1]=l.replace('1920',str(W))
# also check 962 template contentPresenter uses DialogAreaLeftMargin (handled by key)
new[f]='\n'.join(L)
# 4 DialogPopup
f=R+'DialogPopupResourceDictionary.xaml'; t=rd(f); L=t.split('\n')
L[8]=L[8].replace('>158<','>%d<'%(158+S)); assert str(158+S) in L[8]
for k in (1003,1005):
    assert 'MaxSceneWidth' in L[k-1]; L[k-1]=L[k-1].replace('{StaticResource MaxSceneWidth}','{StaticResource FullSceneWidth}',1)
assert 'Canvas.Left="0"' in L[1005]; L[1005]=L[1005].replace('Canvas.Left="0"','Canvas.Left="%d"'%S,1)
assert 'Width="1920"' in L[947]; L[947]=L[947].replace('1920',str(W))
new[f]='\n'.join(L)
# 5 scenes
res=pickle.load(open('/tmp/fm6/rootkids.pkl','rb'))
BG=re.compile(r'x:Name="(Rectangle_TravelBg|Rectangle_BlurBG|Rectangle_DarkenBG|Rectangle_Black|Grid_Background|Video)"')
SKIP={'F700_AutovistaHome.xaml','F352_LeagueLeaderboard.xaml'}
CORNER_L={'F901_HudBottomLeft.xaml','F902_HudTopLeft.xaml'}
RIGHTW={'F903_HudBottomRight.xaml','F904_HudTopRight.xaml'}
SPIN=re.compile(r'x:Name="(IdleIndicator|VoiceOverIndicator|Grid_Loading)"')
for fn in sorted(res):
    f=Sc+fn; t=new.get(f) or rd(f); L=t.split('\n'); ch=False
    root,kids=res[fn]
    # LayoutRoot line
    for i,l in enumerate(L):
        if 'x:Name="LayoutRoot"' in l and l.lstrip().startswith('<local:ZPanel'):
            if 'Width="{StaticResource MaxSceneWidth}"' in l:
                v='%d'%(W-C) if fn in RIGHTW else '{StaticResource FullSceneWidth}'
                L[i]=l.replace('Width="{StaticResource MaxSceneWidth}"','Width="%s"'%v,1); ch=True
                if fn in CORNER_L: pass
            break
    if fn in SKIP: 
        if ch: new[f]='\n'.join(L)
        continue
    for i0,tag in kids:
        if tag.startswith('<local:EventFire') or tag.startswith('<VisualStateManager') or 'StoryboardController' in tag: continue
        # find line range of tag
        j=i0
        while '>' not in L[j]: j+=1
        rng=range(i0,j+1)
        def edit(rx,fnc):
            nonlocal_ch=False
            for k in rng:
                m=re.search(rx,L[k])
                if m: L[k]=L[k][:m.start()]+fnc(m)+L[k][m.end():]; return True
            return False
        if 'GridStyle}' in tag: continue
        if BG.search(tag):
            if edit(r'Width="\{StaticResource MaxSceneWidth\}"',lambda m:'Width="{StaticResource FullSceneWidth}"'): ch=True
            continue
        if fn in CORNER_L or SPIN.search(tag) or (fn=='F900_HudScreenSpace.xaml' and 'Grid_321' in tag):
            d=C
        else: d=S
        if fn in RIGHTW: continue
        if edit(r'Canvas\.Left="(\d+(?:\.\d+)?)"',lambda m:'Canvas.Left="%g"'%(float(m.group(1))+d) if float(m.group(1))!=0 else m.group(0)): ch=True; continue
        if edit(r'Canvas\.Right="(\d+(?:\.\d+)?)"',lambda m:'Canvas.Right="%g"'%(float(m.group(1))+d)): ch=True; continue
        if 'Width="{StaticResource MaxSceneWidth}"' in tag or 'Width="1920"' in tag:
            if fn=='F900_HudScreenSpace.xaml' and ('Grid_Footer' in tag or 'ListBox_HudArrows' in tag):
                if 'Grid_Footer' in tag: edit(r'Width="\{StaticResource MaxSceneWidth\}"',lambda m:'Width="{StaticResource FullSceneWidth}"'); ch=True
                continue
            # add Canvas.Left = S on first line after tag name
            l=L[i0]; m=re.match(r'(\s*<[\w:.]+)',l); L[i0]=m.group(1)+' Canvas.Left="%d"'%S+l[m.end():]; ch=True
    if ch: new[f]='\n'.join(L)
# F900 specifics
f=Sc+'F900_HudScreenSpace.xaml'; t=new[f]
t=sub1(t,'<local:CommonListBox x:Name="ListBox_HudArrows" ItemsSource="{Binding HudArrows}" Width="1920"','<local:CommonListBox x:Name="ListBox_HudArrows" ItemsSource="{Binding HudArrows}" Width="%d"'%W,f)
t=sub1(t,'<Canvas Width="1920" Height="1080" IsItemsHost="True"/>','<Canvas Width="%d" Height="1080" IsItemsHost="True"/>'%W,f)
t=sub1(t,'<Grid x:Name="Grid_TutorialText" HorizontalAlignment="Left" Margin="144,0,0,0"','<Grid x:Name="Grid_TutorialText" HorizontalAlignment="Left" Margin="%d,0,0,0"'%(144+S),f)
new[f]=t
# F901/F902: corner +C handled; 
pickle.dump(new,open('/tmp/fm6/new_v2.pkl','wb'))
print(len(new),'files')
for x in log: print(x)
