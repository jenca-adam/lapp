#!/usr/bin/env python3
import sys
print("LA++MK v1.0")
out=sys.argv[-1]
if out.endswith(".py") or out.endswith("lamk"):
    print("ERR::Unknown file")
    sys.exit(1)
import getkey
import lapp
instr=[]

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
        print(f"\t MEM => SET TO {x.cmp_const  if x.cmp_const>0 else 'ORIG'}")
    if x.cmp_mode==0:
        print("\t CMP: ALWAYS")
    elif x.cmp_mode==1:
        print(f"\t CMP: C{hex(x.cmp_cell)} == {x.cmp_const}")
    elif x.cmp_mode==2:
        print(f"\t CMP: C{hex(x.cmp_cell)} < {x.cmp_const}")
    elif x.cmp_mode==3:
        print(f"\t CMP: C{hex(x.cmp_cell)} > {x.cmp_const}")


for iix in range(15) :
    print("new instruction?[*n]",end='',flush=True)
    g=getkey.getkey()
    if g.lower()=='n':
        print()
        break
    while True:
        print("\nINSTRUCTION",iix)
        print("\nmemory cell:[0123456789ABCDEF]",end='',flush=True)
        memcell=int(getkey.getkey(),16)
        code=memcell<<28
        print("\nCode is",hex(code))
        report_instruction(iix,lapp.core.Cell(code))
        print("jump target: [0123456789ABCDEF]",end='',flush=True)
        jarget=int(getkey.getkey(),16)
        code=code|jarget<<24
        print("\nCode is",hex(code))
        report_instruction(iix,lapp.core.Cell(code))
        print("memo change: [0123]",end='',flush=True)
        memoch=int(getkey.getkey(),4)
        code=code|memoch<<22
        print("\nCode is",hex(code))
        report_instruction(iix,lapp.core.Cell(code))
        print("compare mode: [0123]",end='',flush=True)
        cmpm=int(getkey.getkey(),4)
        code=code|cmpm<<20
        print("\nCode is",hex(code))
        report_instruction(iix,lapp.core.Cell(code))
        print("Else jump: [0123456789ABCDEF]",end='',flush=True)
        elsj=int(getkey.getkey(),16)
        code=code|elsj<<16
        print("\nCode is",hex(code))
        report_instruction(iix,lapp.core.Cell(code))
        const=input("Comparative/Setter constant: [hex 16bit] =>")
        code=code|int(const,16)
        print("==== INSTRUCTION DONE ====")
        print(f"Code for INSTR{iix} => {hex(code)}")
        agree='\x00'
        while agree not in 'ynYN':
            print("\nRetry?[yn]",end='',flush=True)
            agree=getkey.getkey()
        if agree.lower()=='n':
            break
    instr.append(code)
    print()
print("Sequential?[yn]")
seq=getkey.getkey().lower()=='y'
print("\nCompiling...\r",end='')
t=lapp.LaPP(instr,[],seq)

print("== DONE ==")
print("Write an overview of the program?[y*]") 
if getkey.getkey().lower()=="y":
    for x,i in enumerate(t.instr):
        report_instruction(x,i)
print("Save the program?[y*]")
if getkey.getkey().lower()=="y":
    lapp.write_lapp(t,out)
    print("Source saved to",out)

