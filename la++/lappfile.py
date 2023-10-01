from .core import LaPP
def b62_encode(i):
    if i < 62: return "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
    return b62_encode(i // 62) + b62_encode(i % 62)    
def b62_decode(i):
    result=0
    for x,q in enumerate(reversed(i)):
        result+="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".find(q)*62**x
    return result
        
def write_lapps(tl):
    instr=[]
    memo=[]
    for q in tl.instr:
        instr.append(b62_encode(q.cell_code))
    for m in tl.mem:
        memo.append(str(m))
    a=[' '.join(instr),' '.join(memo)]
    if tl.seq:
        a.append("S")
    return'\n'.join(a)
def write_lapp(tl,tlf):
    if isinstance(tlf,str):
        tlf=open(tlf,'w')
    with tlf:
        return tlf.write(write_lapps(tl))

def parse_lapp(tlf,argmemo):
    argmemo=[int(i) for i in argmemo]
    if isinstance(tlf,str):
        tlf=open(tlf,'r')
    memo=[]
    instr=[]
    with tlf:
        instrl=tlf.readline().strip()
        if instrl:
            instr=[b62_decode(i) for i in instrl.split(' ')]
        memol=tlf.readline().strip()
        if memol:
            memo=[int(i) for i in memol.split(' ')]
        seq=bool(tlf.readline().strip())
    memo.extend(argmemo)
    memo=memo[:15]
    return LaPP(instr,memo,seq)
