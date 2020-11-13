# overview

This project is a 32-bit RISC-V CPU design for FPGA.
The CPU is divided to two main components, a datapath and a control unit.

# Getting started 

this project is developed using MyHDL library in python.

to install MyHDL via pip :

 - pip install myhdl 
 
 make sure t upgrade the library by:
 
 - pip install --upgrade myhdl 

for further information about the installtion check out the following link

http://www.myhdl.org/start/installation.html

# running the CPU 

the CPU.py is the top-module in this project. to simulate the CPU, go to the def stimulate() instance and plug in your binary code 

- example:
 --     
        
        # 1
        instructionIN.next = 0b00011111010000000000001110010011
        yield PCclk.posedge

        # 2
        instructionIN.next = 0b00000000000000000000010110010011
        yield PCclk.posedge
        
# further information 

check out MyHDL main repository
 - https://github.com/myhdl/myhdl
MyHDL Docs
- http://docs.myhdl.org/en/stable/
