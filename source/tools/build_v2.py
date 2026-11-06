import struct,sys,zlib,re,pickle
sys.path.insert(0,'/tmp/fm6')
from zp import parse
SRC,PK,OUT,MAN_IN,MAN_OUT=sys.argv[1:6]
d,ents,_=parse(SRC); new={k:v.encode('latin-1') for k,v in pickle.load(open(PK,'rb')).items()}
names={e['name'] for e in ents}; assert all(k in names for k in new)
out=bytearray(); cdl=[]
for e in ents:
    nm=e['name']; nb=nm.encode(); lo=e['lo']
    if nm in new: data=new[nm]; meth=0; crc=zlib.crc32(data)&0xffffffff; cs=us=len(data)
    else:
        nl=struct.unpack_from('<H',d,lo+26)[0]; data=d[lo+30+nl:lo+30+nl+e['cs']]; meth=e['meth']; crc=e['crc']; cs=e['cs']; us=e['us']
    pos=len(out)
    out+=b'PK\x03\x04'+struct.pack('<HHHHHIIIHH',e['vn'],e['fl'],meth,e['mt'],e['md'],crc,cs,us,len(nb),0)+nb+data
    ex=b'\x23\x11\x04\x00'+struct.pack('<I',pos+30+len(nb))
    cdl.append(b'PK\x01\x02'+struct.pack('<HHHHHHIIIHHHHHII',e['vm'],e['vn'],e['fl'],meth,e['mt'],e['md'],crc,cs,us,len(nb),len(ex),0,0,e['ia'],e['ea'],pos)+nb+ex)
cstart=len(out); cd=b''.join(cdl); out+=cd
out+=b'PK\x05\x06'+struct.pack('<HHHHIIH',0,0,len(ents),len(ents),len(cd),cstart,0)
open(OUT,'wb').write(out)
m=open(MAN_IN,'rb').read().decode('latin-1')
rx=r'(path="game:\\media\\ui\.zip"[^>]*?dirstart=")\d+(" dirsize=")\d+(")'
assert re.search(rx,m,re.I)
m=re.sub(rx,lambda x:x.group(1)+str(cstart)+x.group(2)+str(len(cd)+22)+x.group(3),m,flags=re.I)
open(MAN_OUT,'wb').write(m.encode('latin-1')); print('ok',len(out),len(new))
