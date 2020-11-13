from myhdl import always_comb, always, always_seq, block, Signal, intbv, delay, instance, instances,bin
#from mux import mux
#from ControlUnit import ControlUnit
#from decoder import decoder
#from ALU import ALU


@block
def RegisterFile(rs1IN,rs2IN,rd,rs1OUT,rs2OUT,REGwrite,data,clock,enable,reset):

    registers = [Signal(intbv(0,min=-2**31,max=2**31)) for i in range(32)]  # reprsinting the registers as a list of signals

    @always(clock.posedge)  # at each positive edge the REGs will be executed
    def REGs():
        if reset==0:
            rs1OUT.next = registers[rs1IN]  # the output of rs1 will be take by Rigsters List of signals[the input register rs1 address]
            rs2OUT.next = registers[rs2IN]  # the output of rs1 will be take by Rigsters List of signals[the input register rs2 address]
            if REGwrite:                    # if the regsiter write is enable is active
                registers[rd].next = data
                # store the data in the specified address
            # print('value of register x1', bin(registers[1], 32))
            # print('value of register x2', bin(registers[2], 32))
            # print('value of register x3', bin(registers[3], 32))
            # print('value of register x4', bin(registers[4], 32))
            # print('value of register x5', bin(registers[5], 32))
            # print('-----------------------------------------------------------------'
            #       '--------------------------------------------------->>>>> value of register x6', int(registers[6]))
            # print('value of register x7', bin(registers[7], 32))
            # print('value of register x8', bin(registers[8], 32))
            # print('value of register x9', bin(registers[9], 32))
            # print('value of register x10', bin(registers[10], 32))
            # print('value of register x11', bin(registers[11], 32))
            # print('value of register x12', int(registers[12]))
        else:
            REGwrite.next=0


    @always(enable.posedge)
    def display():
        print('<--------------------------REGISTERS--------------------------->')
        print('value of register x1 --->', int(registers[1]))
        print('value of register x2 --->', int(registers[2]))
        print('value of register x3 --->', int(registers[3]))
        print('value of register x4 --->', int(registers[4]))
        print('value of register x5 --->', int(registers[5]))
        print('value of register x6 --->', int(registers[6]))
        print('value of register x7 --->', int(registers[7]))
        print('value of register x8 --->', int(registers[8]))
        print('value of register x9 --->', int(registers[9]))
        print('value of register x10 --->', int(registers[10]))
        print('value of register x11 --->', int(registers[11]))
        print('value of register x12 --->', int(registers[12]))
        print()

    return instances()

@block
def test():


    rs1IN,rs2IN,rd=[Signal(intbv(0)[5:]) for i in range(3)]   # assigning the rs1,rs2 and rd that comes from the decoder to 5 bits signals
    rs1out, rs2out=[Signal(intbv(0,min=-2**31,max=2**31-1)) for i in range(2)] # assigning the outputs as 32 signed signals
    REGwrite=Signal(bool(0))        # assigning the REGwrite to boolean signal
    data=Signal(intbv(0,min=-2**31,max=2**31-1)) # # assigning the data as 32 signed signals
    clock=Signal(bool(0))           # assigning the boolean to boolean signal

    HALF_PERIOD = delay(5)
    @always(HALF_PERIOD)
    def clockGen():
        clock.next = not clock     # toggling the clock so we get postive edge and negative edge

    reg = RegisterFile(rs1IN, rs2IN, rd, rs1out, rs2out, REGwrite, data, clock)     # a driver from the Register file
    @instance
    def run():
        # the coming steps done to load the register file with values
        REGwrite.next=1         # enable writing into the register file
        rd.next=0b010           # giving the address the data to be stored
        data.next=0b011         # assigning the value of the data
        yield (clock.negedge)   # wait for the negative edge

        print('Assign x', rd, ' = ', int(data), sep='') # print which address the data will be store and the value of the data

        rd.next = 0b011         # giving the address the data to be stored
        data.next = 0b101       # assigning the value of the data
        yield (clock.negedge)   # wait for the negative edge

        print('Assign x', rd, ' = ', int(data), sep='') # print which address the data will be store and the value of the data

        rd.next = 0b100              # giving the address the data to be stored
        data.next = 0b101101010101   # assigning the value of the data

        yield (clock.negedge)        # wait for the negative edge
        print('Assign x', rd, ' = ', int(data), sep='')  # print which address the data will be store and the value of the data


        REGwrite.next=0       # done loading the register file
        rs1IN.next= 0b010     # take the register number 2 (x2) as an input
        rs2IN.next= 0b011     # take the register number 3 (x3) as an input

        yield clock.negedge   # wait for the negative edge
        print('rs1IN=x',rs1IN,'  rs2IN=x',rs2IN ,sep='')     # printing the input registers addresses
        print('rs1OUT=',int(bin(rs1out),2),'rs2OUT=',int(bin(rs2out),2)) # printing the value stored in the input addresses
        print()

    return instances()
#
# tb= test()
# tb.run_sim(40)

# if __name__ == '__main__':
#     INrs1=Signal(intbv(0)[5:])
#     INrs2=Signal(intbv(0)[5:])
#     rd1=Signal(intbv(0)[5:])
#     OUTrs1=Signal(intbv(0, min=-2147483648, max=2147483648))
#     OUTrs2=Signal(intbv(0, min=-2147483648, max=2147483648))
#     REGwrite1=Signal(bool(0))
#     data1=Signal(intbv(0, min=-2147483648, max=2147483648))
#     clk=Signal(bool(0))
#
#
#
#     tb = RegisterFile(INrs1,INrs2,rd1,OUTrs1,OUTrs2,REGwrite1,data1,clk)  # type: Module
#     tb.run_sim()
#     tb.convert(hdl='verilog')