from myhdl import block, always, instances, intbv, instance, now, bin, Signal, delay, now, StopSimulation, concat
from InstructionMemorey import inst_memory
from decoder import decoder
from ControlUnit import ControlUnit
from ALU import ALU
from RegistersFile import RegisterFile
from Memory import MainMemory
from utilities import adder,BranchAdder,mux,pc

@block
def CPU():  # the main block which will connect all of our blocks

    ''' creating the nessecry signal to connect the blocks '''

    enable, enable2, clock, RestClk, MEMread, MEMwrite, REGwrite, PCSrc, ALUMUXsig, MEMtoREG, zero, Branch = [
        Signal(bool(0)) for i in range(12)]
    instructionIN = Signal(intbv(0)[32:])
    PCsignal = Signal(intbv(0, min=-1024))
    PC_Mux_result = Signal(intbv(0, min=-1024))
    PC_Branch_result = Signal(intbv(0, min=-1024))
    PC_adder_result = Signal(intbv(0, min=-1024))
    instruction = Signal(intbv(0))
    rs1OUT, rs2OUT = [Signal(intbv(0, min=-2 ** 31, max=2 ** 31)) for i in range(2)]
    rd, rs1, rs2, ALUsig, MEMsignal = [Signal(intbv(0)[5:]) for i in range(5)]
    Mux_RB_result = Signal(intbv(0, min=-2 ** 31, max=2 ** 31))
    imm = Signal(intbv(0, min=-2 ** 31, max=2 ** 31))
    Mux_ALUsrc_result = Signal(intbv(0, min=-2 ** 31, max=2 ** 31))
    ALUoutput = Signal(intbv(0, min=-2 ** 31, max=2 ** 31))
    MEMoutput = Signal(intbv(0, min=-2 ** 31, max=2 ** 31))
    PCclk = Signal(bool(0))
    counter=Signal(intbv(0))

    '''a clock specified for the PC to slow the process of sending an instruction (to prevent pipelining )'''
    @always(delay(25))
    def clockGENpc():
        PCclk.next = not PCclk

    '''a faster clock for the instructions '''
    @always(delay(5))
    def clockGEN():
        if counter==4:
            RestClk.next=1
            counter.next=0
            enable2.next=1
        else:
            RestClk.next=0
            counter.next=counter+1
        clock.next = not clock
        PCSrc.next = (Branch & zero)    # an and gate updated by each clock to determine if the branch is taken or not

    '''<----------------------------connecting the blocks----------------------->'''

    PC_driver = pc(PCclk, PC_Mux_result, enable, PCsignal)

    Adder = adder(PCsignal, PC_adder_result)

    Adder_Branch = BranchAdder(PCsignal, imm, PC_Branch_result)

    Mux_pc = mux(PC_Mux_result, PC_adder_result, PC_Branch_result, PCSrc)

    Instruction_MEM = inst_memory(clock, enable, PCsignal, instructionIN, instruction,RestClk)

    DECODE = decoder(instruction, rs1, rs2, rd, imm)

    CONTROL = ControlUnit(instruction, ALUsig, ALUMUXsig, REGwrite, Branch, MEMwrite, MEMtoREG, MEMread, MEMsignal,
                          clock, enable2,RestClk)

    Regsters = RegisterFile(rs1, rs2, rd, rs1OUT, rs2OUT, REGwrite, Mux_RB_result, clock, enable2,RestClk)

    Mux_ALUsrc = mux(Mux_ALUsrc_result, rs2OUT, imm, ALUMUXsig)

    Perform_operations = ALU(rs1OUT, Mux_ALUsrc_result, ALUsig, ALUoutput, zero, PCsignal)

    MEMaccess = MainMemory(ALUoutput, rs2OUT, MEMoutput, MEMwrite, MEMread, MEMsignal, clock,RestClk)

    Mux_RB = mux(Mux_RB_result, ALUoutput, MEMoutput, MEMtoREG)

    @instance
    def stimulate():

        '''<---------------------start load the instructions into the instruction memory-------------------->'''
        enable.next = 0

        # 1
        instructionIN.next = 0b00011111010000000000001110010011
        yield PCclk.posedge

        # 2
        instructionIN.next = 0b00000000000000000000010110010011
        yield PCclk.posedge

        # 3
        instructionIN.next = 0b00000000000100000000011000010011
        yield PCclk.posedge

        # 4
        instructionIN.next = 0b00011111010000000000001100010011
        yield PCclk.posedge

        # 5
        instructionIN.next = 0b00000000101101100000011000110011
        yield PCclk.posedge

        # 6
        instructionIN.next = 0b00000000110000110010001000100011
        yield PCclk.posedge

        # 7
        instructionIN.next = 0b00000000010000110000001100010011
        yield PCclk.posedge
        # 8
        instructionIN.next = 0b00000000000101011000010110010011
        yield PCclk.posedge
        # 9
        instructionIN.next = 0b11111110011101011100100011100011
        yield PCclk.posedge
        # 10
        instructionIN.next = 0b00011111010000000000001100010011
        yield PCclk.posedge
        # 11
        instructionIN.next = 0b00000000110000110010000000100011
        yield PCclk.posedge
        # 12
        instructionIN.next = 0b00000000000000110010010100000011
        yield PCclk.posedge

        '''<------------------------done loading the instructions ------------------------>'''

        enable.next = 1         # enable the the instructions memory and the PC to start running
        yield clock.negedge

        while True:            # a while loop to print each instruction when it's executing
            print('time: ', now(), 'PC---->', int(PCsignal))
            print(
                '_________________________________________________________________'
                '_______________________________________________________________________________')
            print('\nthe instruction is : %s ||operands: rd: x%d , rs1: x%d , rs2: x%d , imm: %d ' % (
                bin(instruction, 32), int(rd), int(rs1), int(rs2), int(imm)))
            print('the signals are : ALUsignal: %s | ALUMUXsig: %s | REGwrite: %s | PCSrc: %s '
                  '| MEMwrite: %s | MEMtoREG: %s | MEMread: %s | MEMsignal: %s ' % (
                      bin(ALUsig, 5), bin(ALUMUXsig, 1), bin(REGwrite, 1), bin(PCSrc, 1), bin(MEMwrite, 1),
                      bin(MEMtoREG, 6), bin(MEMread, 1), bin(MEMsignal, 3)))

            print('PC Equals: ', int(PCsignal))
            print(
                '______________________________________________________________________________________'
                '__________________________________________________________')

            yield PCclk.negedge

    return instances()


tb = CPU()
tb.run_sim(125951)





