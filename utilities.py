from myhdl import block, always, Signal, intbv, instance, delay, instances, modbv, always_seq, ResetSignal, always_comb


@block
def BranchAdder(PC, imm, result):
    @always_comb
    def add():  # this simple block adds the the calculated jump value shifted to the left by 1
        jump = intbv((imm << 1), min=-1024, max=1024)
        result.next = PC + jump  # assigning the next value to the result

    return instances()

@block
def pc(clock, incremented, enable, PC):

    @always(enable.posedge) # when the enable is on we reset the PC (after finishing loading the instructions)
    def reset():
        PC.next = 0

    @always(clock.posedge)
    def count():

        if enable == 0b0: # increment the PC to load the instruction properly
            PC.next = PC + 4

        elif enable == 0b1: # send the current PC received from the adders
            PC.next = incremented

    return instances()

@block
def mux(z,a,b,sel):

    @always_comb
    def comb():
        if sel==1:
            z.next=b
        else:
            z.next=a
    return comb


@block
def adder(PC,result):

    @always_comb
    def add():
        increament=intbv(4,-1024,1024)
        result.next = PC + increament

    return instances()


























'''@block
def util(clock, incremented, enable, PC, imm, result):

    @always(enable.posedge) # when the enable is on we reset the PC (after finishing loading the instructions)
    def reset():
        PC.next = 0

    @always(clock.posedge)
    def count():

        if enable == 0b0: # increment the PC to load the instruction properly
            PC.next = PC + 4

        elif enable == 0b1: # send the current PC received from the adders
            PC.next = incremented

    @always_comb
    def add():  # this simple block adds the the calculated jump value shifted to the left by 1
        jump = intbv((imm << 1), min=-1024, max=1024)
        result.next = PC + jump  # assigning the next value to the result

    return instances()'''

