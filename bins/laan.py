#!/usr/bin/env python3
2322
#^^^^ You can run LAAN on itself! It's a feature, not a bug.
print("LA++AN v1.0")
from lapp import parse_lapp
def report_instruction(i,x):
    print(f"INSTR {i} ({hex(x.cell_code)}):")
    print(f"\t MEMORY CELL => {hex(x.memory_cell)}")
    if x.jump_target==15:
        print(f"\t TARGET => RETURN")
    else:
        print(f"\t TARGET => {x.jump_target}")
    if x.jump_else==15:
        print(f"\t ELSE => RETURN")
    else:
        print(f"\t ELSE => JUMP {x.jump_else}")
    if x.mem_change==1:
        print("\t MEM => INCR")
    elif x.mem_change==2:
        print("\t MEM => DECR")
    elif x.mem_change==3:
        print(f"\t MEM => SET TO {x.cmp_const if x.cmp_const>0 else 'ORIG'}")
    if x.cmp_mode==0:
        print("\t CMP: ALWAYS")
    elif x.cmp_mode==1:
        print(f"\t CMP: C{hex(x.cmp_cell)} == {x.cmp_const}")
    elif x.cmp_mode==2:
        print(f"\t CMP: C{hex(x.cmp_cell)} < {x.cmp_const}")
    elif x.cmp_mode==3:
        print(f"\t CMP: C{hex(x.cmp_cell)} > {x.cmp_const}")

def write_report(file):
    parsed=parse_lapp(file,[])
    print("REPORT FOR",file)
    for x,i in enumerate(parsed.instr):
        report_instruction(x,i)
    print("INFO:")
    print("\tDEFAULT MEMO => {}".format(' '.join(str(i) for i in parsed.mem)))
    print(f"\t{'SEQUENTIAL' if parsed.seq else 'NON-SEQUENTIAL'}")
import sys

if __name__=='__main__':write_report(sys.argv[-1]) 
