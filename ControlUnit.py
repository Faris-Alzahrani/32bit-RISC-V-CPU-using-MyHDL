from myhdl import always_comb, block, instance, instances, Signal, intbv, delay, bin, now, always, modbv


@block
def ControlUnit(intruction, ALUsig, ALUMUXsig, REGwrite, Branch, MEMwrite, MEMtoREG, MEMread,MEMsignal,clock,enable,rest):
    @always(clock.posedge)
    def control():
        op = intruction[7:0]
        if rest==0:
            if op == 0b0110011:  ###R_type control
                #print('control unit: R Type --> confirmed')
                func3 = intruction[15:12]
                func7 = intruction[32:25]
                ALUMUXsig.next = 0   # will take rs2 not imm
                REGwrite.next = 1    # there will be a write back
                Branch.next = 0       # take PC+4
                MEMwrite.next = 0    # the memory will not receive data
                MEMtoREG.next = 0    # the write back will receive the value from the ALU
                MEMread.next = 0     # the memory will not output any data
                MEMsignal.next = 0
                if (func3 == 0b000):
                    if func7 == 0b0000000:
                        ALUsig.next = 0         #ADD
                    elif func7 == 0b0100000:
                        ALUsig.next = 1         #SUB
                    elif func7 == 0b0000001:
                        ALUsig.next = 8         # MUL
                elif (func3 == 0b001):
                    if (func7==0b0100000):
                        ALUsig.next = 7         #SLL
                    elif (func7==0b0000001):
                        ALUsig.next=14          #MULH
                elif (func3 == 0b010):
                    if (func7==0b0100000):
                        ALUsig.next = 2         #SLT
                    elif (func7==0b0000001):
                        ALUsig.next=15          #MULHSU
                elif (func3 == 0b011):
                    if (func7 == 0b0100000):
                        ALUsig.next = 12        #SLTU
                    elif (func7==0b0000001):
                        ALUsig.next=16          #MULHU
                elif (func3 == 0b100):
                    if (func7 == 0b0100000):
                        ALUsig.next = 3         #XOR
                    elif (func7==0b0000001):
                        ALUsig.next=9           #DIV
                elif (func3 == 0b101):
                    if (func7 == 0b0000000):
                        ALUsig.next = 6         #SRL
                    elif (func7 == 0b0100000):
                        ALUsig.next = 13        #SRA
                    elif (func7==0b0000001):
                        ALUsig.next=11          #DIVU
                elif (func3 == 110):
                    if (func7 == 0b0100000):
                        ALUsig.next = 5         #AND
                    elif (func7==0b0000001):
                        ALUsig.next=10          #REM
                elif (func3 == 111):
                    if (func7 == 0b0100000):
                        ALUsig.next = 4         #OR
                    elif (func7==0b0000001):
                        ALUsig.next=17          #REMU

            elif (op == 0b0010011):  # I_type
                #print('control unit: I Type --> confirmed')
                ALUMUXsig.next = 1       # will take imm not rs2
                REGwrite.next = 1        # there will be a write back
                Branch.next = 0           # take PC+4
                MEMwrite.next = 0        # the memory won't be written into
                MEMtoREG.next = 0        # will take the value from the ALU to the registers
                MEMread.next = 0         # the memory won't be read from
                MEMsignal.next=0
                enable.next= 0

                func3 = intruction[15:12]
                if (func3 == 0b000):     # ADDI
                    ALUsig.next = 0
                elif (func3 == 0b101):   # SLTI
                    ALUsig.next = 2
                elif (func3 == 0b011):   # SLTIU
                    ALUsig.next = 12
                elif (func3 == 0b100):   # XORI
                    ALUsig.next = 3
                elif (func3 == 0b110):   # ORI
                    ALUsig.next = 4
                elif (func3 == 0b111):   # ANDI
                    ALUsig.next = 5
                elif (func3 == 0b001):   # SLLI
                    ALUsig.next = 7
                elif (func3 == 0b101):
                    func7 = intruction[32:25]
                    if func7 == 0b0000000:      # SRLI
                        ALUsig.next = 6
                    elif func7 == 0b0100000:    # SRAI
                        ALUsig.next = 13

            elif (op == 0b0100011):  # S_type
                func3 = intruction[15:12]
                #print('control unit: S Type --> confirmed')
                ALUsig.next = 0     # we use ADDI to add rs1 and and the immediate to calculate the address in memory
                ALUMUXsig.next = 1  # the ALU receives the value from the immediate instead of rs2
                MEMwrite.next = 1   # to indicate the memory will receive write data
                Branch.next = 0      # will take PC+4
                MEMtoREG.next = 0   # we set it to 0 by default but it will not occur (looking at it's a store instruction)
                MEMread.next = 0    # the memory won't output any data
                REGwrite.next=0
                if func3==000:
                    MEMsignal.next=4
                elif func3==0b001:
                    MEMsignal.next=5
                elif func3==0b010:
                    MEMsignal.next=6

            elif (op == 0b0000011):  # Load_instructions
                func3 = intruction[15:12]
                print('control unit: Load instruction --> confirmed')
                ALUsig.next = 0     # we use ADDI to add rs1 and and the immediate to calculate the address in memory
                ALUMUXsig.next = 1  # the ALU receives the value from the immediate instead of rs2
                MEMwrite.next = 1   # to indicate the memory will receive write data
                Branch.next = 0      # will take PC+4
                MEMtoREG.next = 1   # we set it to 1 so the MUX take the value from the memory no the ALU
                MEMread.next = 1    # to enable the load
                REGwrite.next = 1   # to enable writing to the register file
                if func3==000:
                    MEMsignal.next=0
                elif func3==0b001:
                    MEMsignal.next=1
                elif func3==0b010:
                    MEMsignal.next=2
                elif func3==0b100:
                    MEMsignal.next=4
                elif func3==0b101:
                    MEMsignal.next=7



            elif (op == 0b1100011): # SB_type -->Branch instructions

                #print('control unit: SB Type --> confirmed')
                ALUMUXsig.next = 0   # the ALU receives the value from the rs2 instead of imm
                MEMwrite.next = 0    # to indicate the memory won't receive any data
                Branch.next = 1       # activate when a Branch instruction occurs
                MEMtoREG.next = 0    # set by default but won't be needed
                MEMread.next = 0     # the memory wont receive data
                REGwrite.next = 0    # to disable writing to the register file
                MEMsignal.next=0

                func3 = intruction[15:12]
                if (func3 == 0b000):
                    ALUsig.next = 18     # BEQ
                elif (func3 == 0b001):
                    ALUsig.next = 19     # BNQ
                elif (func3 == 0b100):
                    ALUsig.next = 20     # BLT
                elif (func3 == 0b101):
                    ALUsig.next = 21     # BGE
                elif (func3 == 0b110):
                    ALUsig.next = 22     # BLTU
                elif (func3 == 0b111):
                    ALUsig.next = 23     # BGEU

            elif (op == 0b0110111):  # LUI
                #print('control unit: LUI instruction --> confirmed')
                ALUsig.next = 24
                ALUMUXsig.next = 1      # the ALU receives the value from the imm instead of rs2
                MEMwrite.next = 0       # to indicate the memory won't receive any data
                Branch.next = 0          # the PC will be PC+4
                MEMtoREG.next = 1       # to enable the write back
                MEMread.next = 1        # to enable read load from memory
                MEMsignal.next=0

            elif (op == 0b0010111):  # AUIPC
                #print('control unit: AUIPC instruction --> confirmed')
                ALUsig.next = 25
                ALUMUXsig.next = 1      # the ALU receives the value from the imm instead of rs2
                MEMwrite.next = 0       # to indicate the memory won't receive any data
                Branch.next = 0          # the PC will be PC+4
                MEMtoREG.next = 1       # to enable the write back
                MEMread.next = 0        # to enable read load from memory
                MEMsignal.next=0

            elif(op==0b0000000) : # empty instruction (bubble)
                ALUsig.next = 0
                ALUMUXsig.next = 0
                MEMwrite.next = 0
                Branch.next = 0
                MEMtoREG.next = 0
                MEMread.next = 0
                REGwrite.next=0
                MEMsignal.next=0
                enable.next= 1

        else:
            ALUsig.next = 0
            ALUMUXsig.next = 0
            MEMwrite.next = 0
            Branch.next = 0
            MEMtoREG.next = 0
            MEMread.next = 0
            REGwrite.next = 0
            MEMsignal.next = 0
            enable.next = 0




    return instances()


@block
def testBench():

    intruction,ALUsig,ALUMUXsig,REGwrite,PCSrc,MEMwrite,MEMtoREG,MEMread = [Signal(intbv(0)) for i in range(8)]
    h = ControlUnit(intruction,ALUsig,ALUMUXsig,REGwrite,PCSrc,MEMwrite,MEMtoREG,MEMread)

    @instance
    def runner():
        yield delay(5)  # starter delay

        # testing signals for R type
        intruction.next=0b00000000010100010000001000110011
        yield delay(10)
        print('ALUsig', ALUsig, 'ALUMUXsig', ALUMUXsig, 'REGwrite', REGwrite, 'PCSrc', PCSrc, 'MEMwrite', MEMwrite,
              'MEMtoREG',
              MEMtoREG, 'MEMread', MEMread, sep=' ')
        print()

        # testing signals for I type
        intruction.next = 0b00000000010100000000000100010011
        yield delay(10)
        print('ALUsig', ALUsig, 'ALUMUXsig', ALUMUXsig, 'REGwrite', REGwrite, 'PCSrc', PCSrc, 'MEMwrite', MEMwrite,
              'MEMtoREG',
              MEMtoREG, 'MEMread', MEMread, sep=' ')
        print()

        # testing signals for S type
        intruction.next = 0b00000110001000100010001000100011

        yield delay(10)
        print('ALUsig', ALUsig, 'ALUMUXsig', ALUMUXsig, 'REGwrite', REGwrite, 'PCSrc', PCSrc, 'MEMwrite', MEMwrite,
              'MEMtoREG',
              MEMtoREG, 'MEMread', MEMread, sep=' ')
        print()

        # testing signals for SB type
        intruction.next = 0b00000000010100010000010001100011
        yield delay(10)
        print('ALUsig', ALUsig, 'ALUMUXsig', ALUMUXsig, 'REGwrite', REGwrite, 'PCSrc', PCSrc, 'MEMwrite', MEMwrite,
              'MEMtoREG',
              MEMtoREG, 'MEMread', MEMread, sep=' ')
        print()




    return instances()


# test = testBench()
# test.run_sim(120)


'''if __name__ == '__main__':
    intruction1=Signal(intbv(0)[32:])
    ALUsig1=Signal(intbv(0)[5:])
    ALUMUXsig1=Signal(bool(0))
    REGwrite1=Signal(bool(0))
    PCSrc1=Signal(intbv(0,min=0,max=1024))
    MEMwrite1=Signal(bool(0))
    MEMtoREG1=Signal(bool(0))
    MEMread1=Signal(bool(0))
    MEMsignal1=Signal(intbv(0)[5:])

    tb = ControlUnit(intruction1, ALUsig1, ALUMUXsig1, REGwrite1, PCSrc1, MEMwrite1, MEMtoREG1, MEMread1,MEMsignal1)  # type: Module
    tb.run_sim()
    tb.convert(hdl='verilog')'''