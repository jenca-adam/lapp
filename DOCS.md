## Introduction

LAPP is an esoteric programming language purpose of which is to have as few features as possible and be as unreadable as possible.

## Programs

Each program consists of two or three lines.

First line contains 15 *instructions*, encoded in `base36` and split by whitespace characters.
The second line contains 15 cells of the *initial memory* of the program, likewise encoded in `base36` and split by whitespace characters.
If the third line is present and not empty, the program is considered *sequential*. *Sequential* programs are deprecated and supported only by the *LAPP interpreter*. *LAPP compiler* does not support sequential programs.

### Instructions

Each instruction is an 32-bit integer, whose bits represent different instruction parts.
Instruction structure is as follows:

|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                          Instruction (32 bits)                                                            |
|---------------------------|--------------------|-------------------------|------------------------|------------------|------------------------------------|
|Active memory cell (4 bits)|Jump Target (4 bits)|Memory Increment (2 bits)|Jump condition  (2 bits)|Else Jump (4 bits)|Comparative/Setter constant(16 bits)|
|---------------------------|--------------------|-------------------------|------------------------|------------------|------------------------------------|

#### Active memory cell

Active memory cell is represented as its index in the memory field. It's the memory cell the instruction will work with.
This includes incrementing,decrementing,setting and comparing.

#### Jump target

The index of the instruction the executing program will jump to after the evaluation of the current one, if the condition is met.
If the jump target is 16 and jump condition is met, the program will end.

#### Memory Increment

Memory Increment describes how the active memory cell is to be changed.
It has four different possible values:
  0 - don't change the memory cell
  1 - increase the memory cell value by 1
  2 - decrease the memory cell value by 1
  3 - set the memory cell value to the Setter Constant
The Setter constant consist of the last 16 bits of the instruction.

##### Jump Condition

Jump Condition describes the condition for deciding between jumping to Jump target or Else Jump.
It has four possible values:
 0 - Always True
 1 - Memory Cell == Comparative Constant
 2 - Memory Cell >  Comparative Constant
 3 - Memory Cell <  Comparative Constant


