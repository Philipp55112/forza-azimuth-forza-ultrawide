import zipfile,zlib,struct,sys,re,json
sys.path.insert(0,'/tmp/fm6'); from zp import parse
def run(C,M,OUT,MOUT,edits):
    zc=zipfile.ZipFile(C); repl={}
    for n,pairs in edits.items():
        t=zc.read(n)
        for a,b,cnt in pairs:
            a=a.encode(); b=b.encode(); assert t.count(a)==cnt,(n,a,t.count(a)); t=t.replace(a,b)
        repl[n]=t
    d,ents,_=parse(C); out=bytearray(); cds=[]
    for e in ents:
        nm=e['name']; nb=nm.encode(); lo=e['lo']; nl=struct.unpack_from('<H',d,lo+26)[0]
        lh=bytearray(d[lo:lo+30+nl]); data=d[lo+30+nl:lo+30+nl+e['cs']]
        cd=bytearray(d[e['cdpos']:e['cdpos']+46+len(nb)+len(e['ex'])])
        if nm in repl:
            raw=repl[nm]; c=zlib.compressobj(9,zlib.DEFLATED,-15); data=c.compress(raw)+c.flush(); crc=zlib.crc32(raw)&0xffffffff
            for b,o1 in ((cd,16),(lh,14)): struct.pack_into('<III',b,o1,crc,len(data),len(raw))
            cd[10:12]=b'\x08\x00'; lh[8:10]=b'\x08\x00'
        pos=len(out); struct.pack_into('<I',cd,42,pos); struct.pack_into('<I',cd,46+len(nb)+4,pos+30+nl)
        out+=lh+data; cds.append(bytes(cd))
    cst=len(out); cdb=b''.join(cds); out+=cdb
    eo=d.rfind(b'PK\x05\x06'); eocd=bytearray(d[eo:eo+22]); struct.pack_into('<II',eocd,12,len(cdb),cst); out+=eocd
    open(OUT,'wb').write(out)
    m=open(M,'rb').read().decode('latin-1')
    rx=r'(path="game:\\media\\ui\.zip"[^>]*?dirstart=")\d+(" dirsize=")\d+(")'
    assert re.search(rx,m,re.I)
    m=re.sub(rx,lambda x:x.group(1)+str(cst)+x.group(2)+str(len(cdb)+22)+x.group(3),m,flags=re.I)
    open(MOUT,'wb').write(m.encode('latin-1'))
    z=zipfile.ZipFile(OUT); print(OUT,'testzip',z.testzip(),'diff',[x for x in zc.namelist() if zc.read(x)!=z.read(x)])
O='/mnt/user-data/outputs/'
r1='\t\t<Rectangle Fill="Black" Style="{StaticResource A_Style_ScreenSize}" />\r\n'
r2='        <Rectangle Fill="Black" Style="{StaticResource A_Style_ScreenSize}" />\r\n'
r3='            <Rectangle Fill="Black" Style="{StaticResource A_Style_ScreenSize}" />\r\n'
fh={'Scenes/Anthem/A_FMVLoading.xaml':[(r1,'',1)],'Scenes/Anthem/A_Splash.xaml':[(r2,'',1)],'Scenes/Anthem/A_VideoPlayer.xaml':[(r3,'',1)]}
run(O+'fh2_UI_ohneBalken.zip','/mnt/user-data/outputs/fh2_zipmanifest_ohneBalken.xml',O+'fh2_UI_v2.zip',O+'fh2_zipmanifest_v2.xml',fh)
run(O+'fnf_UI_ohneBalken.zip','/mnt/user-data/outputs/fnf_zipmanifest_ohneBalken.xml',O+'fnf_UI_v2.zip',O+'fnf_zipmanifest_v2.xml',fh)
B='/mnt/user-data/uploads/Forza Motorsport 5/Forza_1.0.0.20_x64__8wekyb3d8bbwe/Mount/media/'
w=' Height="{StaticResource MaxSceneHeight}" Background="#FF000000">'
fm5={'Scenes/WPF/F000_Splash.xaml':[('        <Rectangle Width="{StaticResource MaxSceneWidth}" Height="{StaticResource MaxSceneHeight}" Fill="#FF000000"/>\n','',1)]}
for f in ('F020_LoadingInitialExperience','F030_VideoPlayer','F050_Installing','F060_Travel','F061_DemoLoading'):
    fm5['Scenes/WPF/%s.xaml'%f]=[(w,' Height="{StaticResource MaxSceneHeight}">',1)]
run(B+'UI.zip',B+'zipmanifest.xml',O+'fm5_UI_v2.zip',O+'fm5_zipmanifest_v2.xml',fm5)
