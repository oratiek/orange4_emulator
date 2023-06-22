import os
import sys
import time

class Register:
    def __init__(self):
        pass

class Register:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.Y = 0
        self.Z = 0
        self.A_ = 0
        self.B_ = 0
        self.Y_ = 0
        self.Z_ = 0
        self.PC = 0x0
        self.SP = 0 # stack pointer
        self.FLAG = 0

class Memory:
    def __init__(self):
        self.PRG_range = range(0x0, 0x4f)
        self.DT_range = range(0x50, 0x5f)
        self.SYS_range = range(0x60, 0x7f)
        self.PRG_STK_range = range(0x80, 0xef)
        self.STK_range = range(0xf0, 0xff)

        self.__program = []
        self.__data = []
        self.__system = []
        self.__program_stack = []
        self.__stack = []

        self.__data = []
        for i in range(int(0xFF)):
            self.__data.append(0x0)

    def store(self, data):
        self.__program.append(data)

    def load(self, pc):
        return self.__program[pc]
 
register = Register()
memory = Memory()
memory = [0x0 for i in range(0xff)]
LED = [0, 0, 0, 0, 0, 0, 0]
OUTPUT_BIT = 7

def service_call(code):
    # get hex
    match code:
        case 0x0:
            pass
        case 0x1:
            binary = list(map(int, (bin(register.Y)[2:])))
            LED[len(binary)-1:] = binary
        case 0x2:
            pass
        case 0x3:
            pass
        case 0x4:
            pass
        case 0x5:
            pass
        case 0x6:
            pass
        case 0x7:
            pass
        case 0x8:
            pass
        case 0x9:
            pass
        case 0xA:
            pass
        case 0xB:
            pass
        case 0xC:
            pass
        case 0xD:
            pass
        case 0xE:
            pass
        case 0xF:
            pass

def execute(mnemonic, operands):
    match mnemonic:
        case "inc":
            pass
        case "outn":
            pass
        case "abyz":
            tmp = register.A
            register.A = register.B
            register.B = tmp
            tmp = register.Y
            register.Y = register.Z
            register.Z = tmp
        case "ay":
            tmp = register.A
            register.A = register.Y
            register.Y = tmp
        case "st":
            memory[0x50 + register.Y] = register.A
        case "ld":
            register.A = memory[0x50 + register.Y]
        case "add":
            register.A += memory[0x50 + register.Y]
            # 桁上がりを確認
        case "sub":
            register.A -= memory[0x50 + register.Y]
            # 負数になるか確認
        case "ldi":
            register.A = operands[0]
        case "addi":
            register.A += operands[0]
            # 桁上がりを確認
        case "ldyi":
            register.Y = operands[0] 
        case "addyi":
            register.Y += operands[0]
            # 桁上がり確認
        case "cpi":
            if register.A == operands[0]:
                register.FLAG = 0
            else:
                register.FLAG = 1
        case "cpyi":
            if register.Y == operands[0]:
                register.FLAG = 0
            else:
                register.FLAG = 1
        case "scall":
            service_call(operands[0])
        case "jmpf":
            register.PC =  operands[0]
        case "call":
            pass
        case "ret":
            pass
        case "pushA":
            pass
        case "popA":
            pass
        case "pushB":
            pass
        case "popB":
            pass
        case "pushY":
            pass
        case "popY":
            pass
        case "pushZ":
            pass
        case "popZ":
            pass
        case "ioctrl":
            pass
        case "out":
            pass
        case "in":
            pass

assembly = [
        "ldyi 0x1",
        "scall 1",
        "ldyi 0x0",
        "scall 1",
        "jmpf 0x0"
        ]
for i in range(len(assembly)):
    memory[i] = assembly[i]

print("=====Assembly=====")
for row in assembly:
    print(row)
print("==================")

def convert_to_hex(val):
    return int(val, 16)

while True:
    time.sleep(1)

    #########
    # FETCH #
    #########
    try:
        instruction = memory[register.PC]
    except IndexError:
        break

    ##########
    # DECODE #
    ##########
    instruction = memory[register.PC]
    print(register.PC, instruction)
    opecode, *operands = instruction.split(" ")
    operands = list(map(convert_to_hex, operands))

    #################
    # LOAD OPERANDS #
    #################

    ###########
    # EXECUTE #
    ###########
    register.PC += 1
    execute(opecode, operands)


    ##############
    # WRITE BACK #
    ##############
    print(LED)

