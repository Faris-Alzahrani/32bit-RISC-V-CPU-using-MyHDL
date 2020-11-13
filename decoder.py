from myhdl import block, always_comb, instances, instance, Signal, intbv, \
    delay, bin, concat


@block
def decoder(inst, rs1, rs2, rd, imm):  # take the instruction as an input and outputs rs1,rs2,rd and immediate

    @always_comb  # using always_comb because it's combinational logic
    def decode():
        op = inst[7:]  # slicing the opcode to determine the type of the instruction
        func3 = inst[15:12]  # slicing the function 3 to differentiate between \
        # the diffrent instruction that has the same opcode

        if op == 0b0110011:  # R_type
            rd.next = inst[12:7]  # slicing the rd address from the instruction
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            rs2.next = inst[25:20]  # slicing the rs2 address from the instruction
            imm.next = 0  # setting the immediate so it doesnt mix with previous values
            print('decoder: R type --> confirmed')
            # func3.next=inst[15:12]
            # func7.next=inst[:25]


        elif op == 0b0000011:  ### Load instructions
            rd.next = inst[12:7]  # slicing the rd address from the instruction
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            immediate = intbv(inst[32:20], min=-2 ** 31, max=2 ** 31)
            imm.next = immediate  # slicing the immediate from the instruction
            rs2.next = 0  # setting the rs2 so it doesnt mix with previous values
            print('decoder: Load instruction --> confirmed')

        elif op == 0b1100111:  ##JALR
            rd.next = inst[12:7]  # slicing the rd address from the instruction
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            imm.next = inst[32:20]  # slicing the immediate from the instruction
            rs2.next = 0  # setting the rs2 so it doesnt mix with previous values
            print('decoder: JALR instruction --> confirmed')

        elif op == 0b0010011:  # I_type

            rd.next = inst[12:7]  # slicing the rd address from the instruction
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            rs2.next = 0  # setting the rs2 so it doesnt mix with previous values

            if func3 == 0b001 or func3 == 0b101:  # shift immediate instructions
                imm.next = inst[25:20]  # slicing the immediate of the shift amount
                print('decoder: I_type :Shift instruction --> confirmed')
            else:  # if it's not the shift instruction
                print('decoder: I type --> confirmed')
                immediate = intbv(concat(inst[32:20]), min=-2 ** 31, max=2 ** 31)

                imm.next = immediate  # slice the immediate value

        elif op == 0b0100011:  ## S_type
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            rs2.next = inst[25:20]  # slicing the rs1 address from the instruction
            immediate = intbv(concat(inst[32:25], inst[12:7]), min=-2 ** 31, max=2 ** 31)
            imm.next = immediate  # Bit concatination using concat method from myhdl
            rd.next = 0b0  # setting the rd to zero so it doesn't mix with the previous values
            print('decoder: S type --> confirmed')

        elif op == 0b0010111 or op == 0b0110111:  # U_type
            rd.next = inst[12:7]  # slicing the rd address from the instruction
            imm.next = inst[:12]  # slicing the immediate from the instruction
            rs1.next = 0b0  # setting the rs1 to zero so it doesn't mix with the previous values
            rs2.next = 0b0  # setting the rs2 to zero so it doesn't mix with the previous values
            print('decoder: U type --> confirmed')

        elif op == 0b1100011:  # SB_type
            rs1.next = inst[20:15]  # slicing the rs1 address from the instruction
            rs2.next = inst[25:20]  # slicing the rs2 address from the instruction
            immediate = intbv(concat(inst[31], inst[7], inst[31:25], inst[12:8]).signed(), min=-2 ** 31, max=2 ** 31)
            imm.next = immediate  # Bit concatination using concat method from myhdl
            rd.next = 0b0  # setting the rd to zero so it doesn't mix with the previous values
            print('decoder: SB type --> confirmed')

        elif op == 0b1101111:  # UJ type

            rd.next = inst[11:7]  # slicing the rd address from the instruction
            imm.next = intbv(concat(inst[31], inst[20:12], inst[20],
                                    inst[31:21]))  # concat method for concatination
            # and using bin so the zeroes are represented coreectlly
            rs1.next = 0b0  # setting the rs1 to zero so it doesn't mix with the previous values
            rs2.next = 0b0  # setting the rs2 to zero so it doesn't mix with the previous values

            print('decoder: UJ type --> confirmed')


        else:  # empty instruction (bubble)
            print('invalid instruction --> send bubbles')
            rs1.next = 0
            rs2.next = 0
            imm.next = 0
            func3.next = 0

    return instances()


@block
def test_decoder():  # a test bench for the decoder
    instruction = Signal(intbv(0)[32:])  # representing the instruction in 32 bits
    rs1, rs2, rd = [Signal(intbv(0)[5:]) for i in range(3)]  # representing the rs1,rs2 and rd addresses in 5 bits
    imm = Signal(intbv(0, min=-222222222,
                       max=2222222222))  # representing the immediate value in 20 bits which is the highest value it needs (U instructions)
    Decoder_1 = decoder(instruction, rs1, rs2, rd, imm)  # a driver from the decoder

    @instance
    def run():
        yield delay(1)

        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, 5), 'rs1:', bin(rs1, 5), 'rs2', bin(rs2, 5), 'imm:', bin(imm, 5))
        print("_________________________________________")

        # R_type instruction
        instruction.next = 0b00000000010100010000001000110011  # setting a R_type instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   rs2: x%d  ' % (int(rd), int(rs1), int(rs2)))
        print("_________________________________________")

        # I_type instruction
        instruction.next = 0b00000000010100000000000100010011  # setting a I_type instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   imm: %d  ' % (int(rd), int(rs1), int(imm)))
        print("_________________________________________")

        # Load instruction
        instruction.next = 0b00000011001001001010010000000011  # setting a Load instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   imm: %d  ' % (int(rd), int(rs1), int(imm)))
        print("_________________________________________")

        # S_type instruction
        instruction.next = 0b00000110001000100010001000100011  # setting a S_type instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   imm: %d  ' % (int(rs1), int(rs2), int(imm)))
        print("_________________________________________")

        # SB_type instruction
        instruction.next = 0b11111110011101011100100011100011  # setting a SB_type instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   imm: %d  ' % (int(rs1), int(rs2), int(imm)))
        print("_________________________________________")

        # U_type instruction
        instruction.next = 0b00000000000011001000001010110111  # setting a U_type instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d     imm: %d  ' % (int(rd), int(imm)))
        print("_________________________________________")

        # Jump and link register instruction
        instruction.next = 0b00000000101000000000000011100111  # setting a Jump and link register instruction
        yield delay(10)
        print('the instruction :', bin(instruction, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'imm:', bin(imm, width=5))
        print(' rd: x%d   rs1: x%d   imm: %d  ' % (int(rd), int(rs1), int(imm)))
        print("_________________________________________")

    return instances()


# tb= test_decoder()
# tb.run_sim()
#

################## this is the assembly code for this test bench
'''addi x2,x0,5
lui x5,200
add x4,x2,x5
beq x2,x5,label
sw x2,100(x4)
label:lw x8,50(x9)
jalr x1,x0,10
'''
