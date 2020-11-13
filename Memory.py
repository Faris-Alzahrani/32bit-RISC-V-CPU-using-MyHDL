from myhdl import block, always, Signal, intbv, instances, bin, instance, delay, concat, modbv


@block
def MainMemory(address, INdata, OUTdata, MEMwrite, MEMread, MEMcontrol, clock,reset):
    ''' a byte addressable storage for the data memory '''
    storage = [Signal(intbv(0)[8:]) for i in range(10000)]

    @always(clock.posedge)
    def MEM():
        if reset ==0:
            if MEMread == 0b1:
                if MEMcontrol == 0:  # LB
                    OUTdata.next = storage[address]
                elif MEMcontrol == 1:  # LH

                    OUTdata.next=int(concat(storage[address+1],storage[address])) # concat method
                elif MEMcontrol == 2:

                    OUTdata.next= concat(storage[address + 3],storage[address + 2],
                                         storage[address + 1],storage[address]) # method concat
                elif MEMcontrol==4 : # LBU
                    OUTdata.next = storage[(address[32:])]
                elif MEMcontrol==7 : # LHU
                    OUTdata.next = int(concat(storage[(address[32:]) + 1], storage[address[32:]]))  # concat method

            elif MEMwrite == 0b1:
                if MEMcontrol == 4:  # SB
                    storage[address].next = INdata

                elif MEMcontrol == 5:  # SH
                    storage[address].next = INdata[8:]
                    storage[address + 1].next = INdata[16:8]
                elif MEMcontrol == 6:  # SW
                    storage[address].next = INdata[8:]
                    storage[address + 1].next = INdata[16:8]
                    storage[address + 2].next = INdata[24:16]
                    storage[address + 3].next = INdata[32:24]
        else:
            MEMwrite.next=0
            MEMread.next=0



    return instances()


''' TEST BENCH TO TEST THE CORRECTNESS OF THE INSTRUCTION MEMORY'''


@block
def test():

    address, INdata, OUTdata, MEMwrite, MEMread, MEMcontrol= [Signal(intbv(0)) for i in range(6)]
    clock = Signal(bool(0))

    test = MainMemory(address, INdata, OUTdata, MEMwrite, MEMread, MEMcontrol, clock)

    @always(delay(5))
    def clk_driver():
        clock.next = not clock

    @instance
    def run():
        address.next = 1
        INdata.next = 0b00000000000000000000010110010011
        MEMwrite.next = 1
        MEMcontrol.next = 6
        MEMread.next = 0
        yield delay(10)
        print(address,INdata,MEMwrite)

        MEMread.next = 1
        MEMcontrol.next = 2
        address.next = 1
        MEMwrite.next = 0
        yield delay(10)
        print(address,INdata,MEMwrite)
        print('out -->',bin(OUTdata,32))

    return instances()

#
# tb = test()
# tb.run_sim(100)


# if __name__ == '__main__':
#     address1=Signal(intbv(0,min=0,max=1024))
#     INdata1=Signal(intbv(0,min=-2**31,max=2**31))
#     OUTdata1=Signal(intbv(0,min=-2**31,max=2**31))
#     MEMwrite1 = Signal(bool(0))
#     MEMread1=Signal(bool(0))
#     MEMcontrol1= Signal(intbv(0)[3:])
#     clock1 = Signal(bool(0))
#     tb = MainMemory(address1, INdata1, OUTdata1, MEMwrite1, MEMread1, MEMcontrol1, clock1)  # type: Module
#     tb.run_sim()
#     tb.convert(hdl='verilog')
