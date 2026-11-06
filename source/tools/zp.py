import struct,sys
def parse(path):
    d=open(path,'rb').read()
    e=d.rfind(b'PK\x05\x06')
    n,cds,cdo=struct.unpack_from('<HII',d,e+10)[0],struct.unpack_from('<I',d,e+12)[0],struct.unpack_from('<I',d,e+16)[0]
    ents=[];p=cdo
    for i in range(n):
        assert d[p:p+4]==b'PK\x01\x02'
        (vm,vn,fl,meth,mt,md,crc,cs,us,nl,xl,cl,ds,ia,ea,lo)=struct.unpack_from('<HHHHHHIIIHHHHHII',d,p+4)
        name=d[p+46:p+46+nl].decode(); ex=d[p+46+nl:p+46+nl+xl]
        ents.append(dict(name=name,vm=vm,vn=vn,fl=fl,meth=meth,mt=mt,md=md,crc=crc,cs=cs,us=us,ex=ex,ia=ia,ea=ea,lo=lo,cdpos=p))
        p+=46+nl+xl+cl
    return d,ents,(e,n,cds,cdo)
if __name__=='__main__':
    d,ents,eo=parse(sys.argv[1]); print(eo,len(d),len(ents))
    for x in ents[:5]+ents[-3:]:
        print({k:(v.hex() if isinstance(v,bytes) else v) for k,v in x.items()})
        lo=x['lo']; print(d[lo:lo+30].hex(), struct.unpack_from('<HH',d,lo+26))
    import collections; print(collections.Counter(x['meth'] for x in ents))
    print(d[eo[0]:].hex())
