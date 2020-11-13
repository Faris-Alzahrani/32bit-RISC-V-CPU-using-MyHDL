import random
from myhdl import block, Signal, intbv, enum, delay, always, always_comb, always_seq, now, instance, instances, bin, \
    modbv



import random
from myhdl import block, Signal, intbv, enum, delay, always, always_comb, always_seq, now, instance, instances, bin


@block
def ALU(A, B, Control, Output, Zero,PC):
    @always_comb
    def calculate():
        if Control == 0:  # At control=0 ADD
            Output.next = A + B
            Zero.next=0
        elif Control == 1:  # At control=1 Subtract
            Output.next = A - B
            Zero.next=0
        elif Control == 2:  # At control=2 Set less than
            if A > B:
                Output.next = 1
                Zero.next = 0

            else:
                Output.next = 0
                Zero.next = 0
        elif Control == 3:  # At control=3 XOR
            Output.next = A ^ B
            Zero.next = 0
        elif Control == 4:  # At control=4 OR
            Output.next = A | B
            Zero.next = 0
        elif Control == 5:  # At control=5 AND
            Output.next = A & B
            Zero.next = 0
        elif Control == 6:  # At control=6 shift right logical
            Output.next = A >> B[32:]
            Zero.next = 0
        elif Control == 7:  # At control=7 shift left logical
            Output.next = A << B[32:]
            Zero.next = 0
        elif Control == 8:  # At control=8 Multiply (32 bits-32 bits)
            Output.next = A * B
            Zero.next = 0
        elif Control == 9:  # At control=9 Divide (ignore fraction)
            Output.next = int(A // B)
            Zero.next = 0
        elif Control == 10:  # At control=10 remainder
            Output.next = A % B
            Zero.next = 0
        elif Control == 11:  # At control=11 Divide unsigned
            Output.next = int(bin(A[32:] // B[32:]),2)
            Zero.next = 0
        elif Control == 12:  # At control= 12 set less than unsigned
            if A[32:] > B[32:]:
                Output.next = 1
                Zero.next = 0
            else:
                Output.next = 0
                Zero.next = 0
        elif Control == 13:  # At control= 13 shift right arithmatic
            C = modbv((A >> B) | (A << (len(A) - B)), min=-2 ** 31, max=2 ** 31-1)
            Output.next = C
            Zero.next = 0
        elif Control == 14:  # At control= 14 multiply high
            Output.next = (A * B )>>32
            Zero.next = 0
        elif Control == 15:  # At control=15 multiply high signed unsigned
            Output.next = (A * (B)[32:])>>32
            Zero.next = 0
        elif Control == 16:  # At control= 16 multiply high unsigned
            Output.next = ((A)[32:] * (B)[32:])>>32
            Zero.next = 0
        elif Control == 17:  # At control= 17 remainder unsigned
            Output.next = A[32:] % B[32:]
            Zero.next = 0
        elif Control == 18:  # At control= 18 Branch if equivalent
            if A == B:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control == 19:  # At control= 19 branch if not equivalent
            if A != B:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control == 20:  # At control= 20 branch less than
            if A < B:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control == 21:  # At control=21 branch greater than
            if A > B:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control == 22:  # At control=22 branch greater than or equal
            if A >= B:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control == 23:  # At control=23 branch greater than or equal unsigned
            if A[32:] >= B[32:]:
                Zero.next = 1
                Output.next = 0
            else:
                Zero.next = 0
                Output.next = 0
        elif Control==24: #At control=24 load upper immediate
            Output.next=B<<12
            Zero.next = 0
        elif Control==25: #At control=25 add upper immediate to pc
            z=(B<<12)+PC
            Output.next= z
            Zero.next = 0
        else:  # At any other control, return 0
            Output.next = 0
            Zero.next = 0

    return calculate



@block
def test_ALU():
    A, B = [Signal(intbv(0, min=-2147483648, max=2147483648)) for i in range(2)]  # setting the inputs as 32 signed signals
    Control, Zero = [Signal(intbv(0)) for i in range(2)]        # setting the control and zero signal
    Output= Signal(modbv(0,min=-2147483648,max=2147483648))     # we used modbv instead of intbv so we can perform the SRA
    ALU1 = ALU(A, B, Control, Output, Zero)                     # a driver from the ALU

    @instance
    def stimulus():
        print("                      A      B     Control        Output")
        A.next, B.next, Control.next = -10, 50, 0  # Testing ADD
        yield delay(10)
        print("the opretion is add:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = -10, 50, 1  # Testing SUB
        yield delay(10)
        print("the opretion is sub:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = -10, 3, 7  # Testing SLL
        yield delay(10)
        print("the opretion is SLL:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = -500, 3, 23  # Testing BGEU
        yield delay(10)
        print("the opretion is BGEU:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = 3, 3, 19  # Testing BNQ
        yield delay(10)
        print("the opretion is BNQ:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = 0, 10, 24  # Testing LUI
        yield delay(10)
        print("the opretion is LUI:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = -20, 10, 9  # Testing DIV
        yield delay(10)
        print("the opretion is DIV:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A), int(B), int(Control), int(Output), int(Zero)))
        A.next, B.next, Control.next = -int(429496/2), 10, 11  # Testing DIVU
        yield delay(10)
        print(bin(A.unsigned()))
        print("the opretion is DIVU:  A= %s B= %s Control= %s Ans=%s Zero=%s" % (int(A.unsigned()), int(B), int(Control), int(Output), int(Zero)))


    return stimulus, ALU1

# tb = test_ALU()
# tb.run_sim()



if __name__ == '__main__':
    Z=Signal(intbv(0, min=-2147483648, max=2147483648))
    X=Signal(intbv(0, min=-2147483648, max=2147483648))
    Control1=Signal(intbv(0)[5:])
    Output1=Signal(intbv(0, min=-2147483648, max=2147483648))
    Zero1=Signal(bool(0))
    PC = Signal(intbv(0, min=-2147483648, max=2147483648))

    tb = ALU(Z, X, Control1, Output1, Zero1,PC)  # type: Module
    tb.run_sim()
    tb.convert(hdl='verilog')

# tb.run_sim()