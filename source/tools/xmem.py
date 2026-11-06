"""Pure-python LZX decoder for Xbox XMemCompress streams (Forza zip method 21)."""
import struct
def _slots(wbits):
    n={15:30,16:32,17:34,18:36,19:38,20:42,21:50}[wbits]
    extra=[];base=[];b=0
    for i in range(n):
        e=0 if i<4 else min(17,(i-2)//2)
        extra.append(e); base.append(b); b+=1<<e
    return n,extra,base
class Huff:
    def __init__(s,lens):
        s.maxl=max(lens) if lens else 0; s.tab={}
        code=0
        for l in range(1,17):
            for sym,x in enumerate(lens):
                if x==l: s.tab[(l,code)]=sym; code+=1
            code<<=1
class LZX:
    def __init__(s,wbits=17):
        s.wbits=wbits; s.wsize=1<<wbits; s.win=bytearray(s.wsize); s.pos=0
        s.nslots,s.extra,s.base=_slots(wbits)
        s.mainel=256+8*s.nslots
        s.R=[1,1,1]; s.mainlen=[0]*s.mainel; s.lenlen=[0]*249
        s.blk_type=0; s.blk_rem=0; s.hdr=False; s.e8=0; s.first=True
        s.out_total=0
    # bit reader over a bytes chunk
    def _init(s,data): s.d=data; s.p=0; s.buf=0; s.bl=0
    def _ens(s,n):
        while s.bl<n:
            w=struct.unpack_from('<H',s.d,s.p)[0] if s.p+1<len(s.d) else 0
            s.p+=2; s.buf=(s.buf<<16)|w; s.bl+=16
    def _rd(s,n):
        if n==0: return 0
        s._ens(n); v=(s.buf>>(s.bl-n))&((1<<n)-1); s.bl-=n; s.buf&=(1<<s.bl)-1; return v
    def _sym(s,h):
        code=0
        for l in range(1,17):
            code=(code<<1)|s._rd(1)
            r=h.tab.get((l,code))
            if r is not None: return r
        raise ValueError('bad huffman code')
    def _lens(s,lens,start,end):
        pre=Huff([s._rd(4) for _ in range(20)])
        i=start
        while i<end:
            z=s._sym(pre)
            if z==17:
                r=4+s._rd(4)
                for _ in range(r):
                    if i<end: lens[i]=0; i+=1
            elif z==18:
                r=20+s._rd(5)
                for _ in range(r):
                    if i<end: lens[i]=0; i+=1
            elif z==19:
                r=4+s._rd(1); z2=s._sym(pre); v=(lens[i]-z2+17)%17
                for _ in range(r):
                    if i<end: lens[i]=v; i+=1
            else:
                lens[i]=(lens[i]-z+17)%17; i+=1
    def frame(s,data,usize):
        """decode one frame (chunk) producing usize bytes"""
        s._init(data); out=bytearray()
        if s.first:
            s.first=False
            if s._rd(1): s.e8=(s._rd(16)<<16)|s._rd(16)
        while len(out)<usize:
            if s.blk_rem==0:
                if s.blk_type==3 and s.blk_rawpad:
                    pass
                s.blk_type=s._rd(3); hi=s._rd(8); mid=s._rd(8); lo=s._rd(8)
                s.blk_rem=(hi<<16)|(mid<<8)|lo; s.blk_rawpad=0
                if s.blk_type==2:
                    s.alen=[s._rd(3) for _ in range(8)]; s.ah=Huff(s.alen)
                if s.blk_type in (1,2):
                    s._lens(s.mainlen,0,256); s._lens(s.mainlen,256,s.mainel); s._lens(s.lenlen,0,249)
                    s.mh=Huff(s.mainlen); s.lh=Huff(s.lenlen)
                elif s.blk_type==3:
                    # align to 16 bits then 3 x u32
                    s.bl-=s.bl%16; s.buf&=(1<<s.bl)-1
                    s.R=[s._rd(16)|(s._rd(16)<<16) for _ in range(3)]
                    s.blk_rawpad=s.blk_rem&1
                else: raise ValueError('bad block type %d'%s.blk_type)
            n=min(s.blk_rem,usize-len(out))
            if s.blk_type==3:
                # raw bytes: bit reader is byte-aligned in 16 bit units
                got=0
                while got<n:
                    if s.bl==0: s._ens(16)
                    b=(s.buf>>(s.bl-8))&0xff; s.bl-=8; s.buf&=(1<<s.bl)-1
                    s._put(b,out); got+=1
                s.blk_rem-=n
                if s.blk_rem==0 and s.blk_rawpad: s.bl-=s.bl%16 if s.bl%16 else 0
                continue
            end=len(out)+n
            while len(out)<end:
                m=s._sym(s.mh)
                if m<256: s._put(m,out); s.blk_rem-=1; continue
                m-=256; ml=m&7; slot=m>>3
                if ml==7: ml+=s._sym(s.lh)
                ml+=2
                if slot==0: off=s.R[0]
                elif slot==1: off=s.R[1]; s.R[1]=s.R[0]; s.R[0]=off
                elif slot==2: off=s.R[2]; s.R[2]=s.R[0]; s.R[0]=off
                else:
                    e=s.extra[slot]
                    if s.blk_type==2 and e>=3:
                        v=s._rd(e-3)<<3; v+=s._sym(s.ah)
                    else: v=s._rd(e)
                    off=s.base[slot]-2+v
                    s.R[2]=s.R[1]; s.R[1]=s.R[0]; s.R[0]=off
                for _ in range(ml):
                    s._put(s.win[(s.pos-off)%s.wsize],out)
                s.blk_rem-=ml
            # (matches may overrun frame end; handled by caller using exact sizes)
        # frame end: align
        if s.bl%16: s.bl-=s.bl%16
        res=bytes(out[:usize])
        if s.e8:
            res=s._e8(res)
        return res
    def _put(s,b,out): s.win[s.pos]=b; s.pos=(s.pos+1)%s.wsize; out.append(b)
    def _e8(s,buf):
        return buf  # TODO if needed
def decompress(raw,usize,wbits=17):
    """raw = entry data of zip method 21"""
    dec=LZX(wbits); out=bytearray(); p=0
    while len(out)<usize and p<len(raw):
        if raw[p]==0xff:
            fs=struct.unpack_from('>H',raw,p+1)[0]; cs=struct.unpack_from('>H',raw,p+3)[0]; p+=5
        else:
            cs=struct.unpack_from('>H',raw,p)[0]; fs=32768; p+=2
        out+=dec.frame(raw[p:p+cs],min(fs,usize-len(out))); p+=cs
    return bytes(out)
