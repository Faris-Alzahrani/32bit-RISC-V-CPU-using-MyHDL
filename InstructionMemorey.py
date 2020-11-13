from myhdl import block, always, intbv, Signal, instances, instance, delay, bin, modbv, concat


@block
def inst_memory(clk, enable, pc, instructionIn, instructionOut,reset):

    ''' storage to store the loading the instruction'''
    memory = [Signal(intbv(0)[8:]) for i in range(2000)]


    @always(clk.posedge)
    def inst():
        if enable == 0b0:  # when the enable is 0 --> loading mode is on , sore the instructions according to the PC
            memory[pc + 0].next = instructionIn[8:]
            memory[pc + 1].next = instructionIn[16:8]
            memory[pc + 2].next = instructionIn[24:16]
            memory[pc + 3].next = instructionIn[:24]
        if reset==1:
            instructionOut.next=0
        else:  # when the enable equals 1 --> loading mode is off, ad start to send the instructions out
            instructionOut.next = concat((memory[pc + 3]) , (memory[pc + 2]) ,(memory[pc + 1]) , (memory[pc + 0]))

    return instances()


@block
def test():
    clock = Signal(bool(0))
    enable = Signal(bool(0))
    pc = Signal(intbv(0))
    instructionIn = Signal(intbv(0b00000000010000110000001100010011))
    instructionOut = Signal(intbv(0)[32:])
    INST = inst_memory(clock, enable, pc, instructionIn, instructionOut)

    @always(delay(5))
    def clk_generator():
        clock.next = not clock

    @instance
    def start():
        enable.next=0 # loading the instruction
        yield delay(5)
        print('not loaded yet:',instructionOut)
        yield delay(10)
        enable.next = 1
        yield delay(10)
        print('after loading:',instructionOut)
        yield delay(5)

    return instances()

#
# tb = test()
# tb.run_sim(100)

'''
if __name__ == '__main__':
    clk1=Signal(bool(0))
    enable1=Signal(bool(0))
    pc1=Signal(intbv(0,min=0,max=1024))
    instructionIn1 = Signal(intbv(0)[32:])
    instructionOut1=Signal(intbv(0)[32:])

    tb = inst_memory(clk1, enable1, pc1, instructionIn1, instructionOut1)  # type: Module
    tb.run_sim()
    tb.convert(hdl='verilog')'''