import sys
import time
sys.setrecursionlimit(2**31-1)
class Error:
    ERRCODE_MEMORY_INDEX=0x10
    ERRCODE_MEM_OVERFLOW=0x20
    ERRCODE_UNKNOWN=0xff
    ERRCODE_JUMP_TO=0xaa
    ERRCODE_NO_INSTR=0xbb
    ERRCODE_IS_STDIN=0xcc
    ERRCODE_OK=0x0
ERROR_DICT={v:k for k,v in Error.__dict__.items() if k.isupper()}
class TouLangRuntimeEror(RuntimeError):pass
RESET=0xff
def toul_raise(errcode,ans):
    print(f"LAPP ERR -> {ERROR_DICT[errcode]}: {ans}",file=sys.stderr)
    sys.exit(errcode)

def compute_mem_change(a):
    if a==3:
        return RESET
    if a==2:
        return -1
    return a
def mk_mem_change(mem_con,mem_ch,const,o):
    mem_ch_add=compute_mem_change(mem_ch)
    if mem_ch_add==RESET:
        if const==0:
            return o
        return const
    return mem_con+mem_ch_add

class Cell:
    def __init__(self,cell):
        self.cell_code=cell
        self.memory_cell=self.cell_code&0xf0000000
        self.memory_cell//=0x10000000
        self.cmp_cell=self.memory_cell
        self.jump_target=self.cell_code&0xf000000
        self.jump_target//=0x1000000
        self.mem_change=self.cell_code&0xc00000
        self.mem_change//=0x400000
        self.cmp_mode=self.cell_code&0x300000
        self.cmp_mode//=0x100000
        self.jump_else=self.cell_code&0xf0000
        self.jump_else//=0x10000
        self.cmp_const=self.cell_code&0xffff
    def call_upon(self,instr,mem,orig=None):
        if orig is None:
            orig=mem[self.memory_cell]
        try:
            mem_con=mem[self.memory_cell]
        except IndexError:
            return Error.ERRCODE_MEMORY_INDEX,self.memory_cell
        try:
            mem_con=mk_mem_change(mem_con,self.mem_change,self.cmp_const,orig)
            if mem_con>0xffff:
                return Error.ERRCODE_MEM_OVERFLOW,self.memory_cell
            mem[self.memory_cell]=mem_con
            cmp_con=mem_con
            cmp_const=self.cmp_const
            if (self.cmp_mode==0) \
                    or (self.cmp_mode==1 and (cmp_con)==(cmp_const))\
                    or (self.cmp_mode==2 and cmp_con<cmp_const)\
                    or (self.cmp_mode==3 and cmp_con>cmp_const):
                if self.jump_target<15:
                    
                    if self.jump_target>=len(instr):
                        return Error.ERRCODE_NO_INSTR,self.jump_target
                    return Error.ERRCODE_JUMP_TO,self.jump_target
            elif self.jump_else<15:
                if self.jump_else>=len(instr):
                        return Error.ERRCODE_NO_INSTR,self.jump_else

                return Error.ERRCODE_JUMP_TO,self.jump_else
        except Exception as e:
            raise
            return Error.ERRCODE_UNKNOWN,str(e)

        return Error.ERRCODE_OK,mem[15]
def fill_in(i,l):
    while len(i)<l:
        i.append(0)
    return i
class LaPP:
    def __init__(self,instr,mem,seq=False):
        self.seq=seq
        self.instr=[Cell(i) for i in instr]
        if len(self.instr)>15:
            raise ValueError("The program must have at most 15 instructions.")
        self.mem=mem
        if len(self.mem)>15:
            raise ValueError("Default memory must have at most 30 bytes")

    def run(self,index=0,vis=None,memo=None):
        vis=vis or set()
        original_memo=fill_in(self.mem.copy(),16)
        runtime_memo=memo or (fill_in(self.mem.copy(),16))
        errcode=Error.ERRCODE_JUMP_TO
        import time
        while errcode==Error.ERRCODE_JUMP_TO:
            errcode,ans=self.instr[index].call_upon(self.instr,runtime_memo,original_memo[self.instr[index].memory_cell])
            vis.add(index)
            if errcode!=Error.ERRCODE_JUMP_TO:
                break
            if errcode not in [0,Error.ERRCODE_JUMP_TO]:
                toul_raise(errcode,ans)

            index=ans
            
        if self.seq:
            for i in range(len(self.instr)):
                if i not in vis:
                    _,vis,runtime_memo=self.run(index=i,vis=vis,memo=runtime_memo)
        if errcode>0:
            toul_raise(errcode,ans)
        return runtime_memo[15],vis,runtime_memo
  


