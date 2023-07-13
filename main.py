import os
import sys
import time

# retの実装がわからない
# 実行フラグの具合がわからない
# 書き換え先はCが良さそう

class Register:
    def __init__(self):
        self.A = 0x0
        self.B = 0x0
        self.Y = 0x0
        self.Z = 0x0
        self.A_ = 0x0
        self.B_ = 0x0
        self.Y_ = 0x0
        self.Z_ = 0x0
        self.PC = 0x0
        self.SP = 0xF0 # stack pointer
        self.FLAG = 0

register = Register()
memory = [0x0 for i in range(0xff)]
stack_index = 0xf0
stack_size = 10

def push(val):
    global stack_index
    if register.SP > register.SP+stack_size-1:
        return False
    memory[register.SP] = val 
    #register.SP += 1
    return True

def pop():
    if register.SP < 0:
        return False
    val = memory[register.SP]
    memory[register.SP] = 0
    memory[register.SP:] = memory[register.SP+1:] + [0]
    return val

LED = [0, 0, 0, 0, 0, 0, 0]
PORT_MAX = 5
PORTS = [0 for i in range(PORT_MAX)]
SEG_LED = 0
OUTPUT_BIT = 7

def service_call(code):
    global LED
    # get hex
    match code:
        case 0x0:
            pass
        case 0x1:
            clean_LED = [0,0,0,0,0,0,0]
            binary = list(map(int, (bin(register.Y)[2:])))
            #LED[len(LED)-len(binary):] = binary
            clean_LED[len(LED)-len(binary):] = binary
            LED = clean_LED
        case 0x2: # ちょっと違うかも
            clean_LED = [0,0,0,0,0,0,0]
            binary = list(map(int, bin(register.Y)[2:]))
            #LED[len(LED)-len(binary):] = binary
            clean_LED[len(LED)-len(binary):] = binary
            clean_LED = [1 - bit for bit in clean_LED]
            LED = clean_LED
        case 0x3:
            pass
        case 0x4:
            # Aレジスタの全ビットを反転する
            #if register.FLAG == 1:
            binary = list(map(int, bin(register.A)[2:]))
            reversed_binary = [1 - bit for bit in binary]
            register.A = int("0b"+"".join(map(str,reversed_binary)),2)
        case 0x5: # A,B,Y,Zの値を、裏と交換する
            pass
        case 0x6:
            pass
        case 0x7: # エンド音を鳴らす
            pass
        case 0x8: # エラー音を鳴らす
            pass
        case 0x9: # 「ピッ」という短い音を鳴らす
            pass
        case 0xA: # 「ピー」という長い音を鳴らす
            pass
        case 0xB: # Aレジスタで指定した音階(1~E)の音を鳴らす
            pass
        case 0xC: # Aレジスタで指定した時間だけ処理を待つ A+1*0.1秒:
            time.sleep((register.A + 1)*0.1)
        case 0xD:
            pass
        case 0xE:
            pass
        case 0xF:
            pass

def execute(mnemonic, operands):
    global SEG_LED
    match mnemonic:
        case "inc":
            pass
        case "outn":
            SEG_LED = register.A
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
            before_bits = len(bin(regsiter.A).split("b")[-1])
            register.A += memory[0x50 + register.Y]
            after_bits = len(bin(regsiter.A).split("b")[-1])
            if after_bits > before_bits:
                register.FLAG = 1
            else:
                register.FLAG = 0
        case "sub":
            register.A -= memory[0x50 + register.Y]
            if register.A < 0:
                register.FLAG = 1
            else:
                register.FLAG = 0
        case "ldi":
            register.A = operands[0]
        case "addi":
            before_bits = len(bin(register.A).split("b")[-1])
            register.A += operands[0]
            after_bits = len(bin(register.A).split("b")[-1])
            if after_bits > before_bits:
                register.FLAG = 1
            else:
                register.FLAG = 0
        case "ldyi":
            register.Y = operands[0] 
        case "addyi":
            before_bits = len(bin(register.A).split("b")[-1])
            register.Y += operands[0]
            after_bits = len(bin(register.A).split("b")[-1])
            if after_bits > before_bits:
                register.FLAG = 1
            else:
                register.FLAG = 0
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
            if register.FLAG == 1:
                register.PC =  operands[0]
            else:
                register.FLAG = 1
        case "call":
            push(register.PC)
            register.PC = operands[0]
            #register.PC += 1
        case "ret": #呼び出し元に制御を戻す
            register.PC = pop()
            #print("from ret: debug:{}".format(register.PC))
        case "pushA":
            return push(register.A)
        case "popA":
            return pop()
        case "pushB":
            return push(register.B)
        case "popB":
            return pop()
        case "pushY":
            return push(register.Y)
        case "popY":
            return pop()
        case "pushZ":
            return push(register.Z)
        case "popZ":
            return pop()
        case "ioctrl":
            pass
        case "out":
            #print("PORT:{}".format(register.A))
            PORTS[0] = register.A
        case "in":
            pass
assembly = [
        "ldyi 0x0",
        "scall 1",
        "ldyi 0x1",
        "scall 1",
        "call 0x0"
        ]

assembly = [
        "ldyi 0x0",
        "scall 1",
        "ldyi 0x1",
        "scall 1",
        "ldyi 0x2",
        "scall 1",
        "ldyi 0x3",
        "scall 1",
        "ldyi 0x4",
        "scall 1",
        "call 0x0"
        ]

assembly = [
        "ldyi 0x55", # Yに0xAを入れる
        "scall 1", # Yに対応する値を点灯させる
        "ay", # Yの値がAに入る
        "scall 4", # Aの値をビット反転させる
        "ay", # Aの値をYに入れる
        "scall 1", # Yに対応する値を点灯させる
        "call 0x0"
        ]

assembly = [
        "ldyi 0x1",
        "ldi 0x1",
        "out",
        "ldi 5",
        "scall 0xC",
        "ldi 0x0",
        "out",
        "ldi 5",
        "scall 0xC",
        "call 0x00"]

assembly = [
        "ldyi 0x1",
        "ldi 0x1",
        "out",
        "ldi 5",
        "scall 0xC",
        "ldi 0x0",
        "out",
        "ldi 5",
        "scall 0xC",
        "call 0x00"
        ]

# increment 7SEG
assembly = [
        "ldi 0x0",
        "addi 0x1",
        "outn",
        "call 0x1"
        ]

# Lチカ
assembly = [
        "ldyi 0x0", # store 0 to register Y
        "scall 1",  # turn on LED related to register Y
        "ldi 0x5", # store 9 to register A
        "scall 0xC", # wait for sec which specified by register A
        "scall 2", # turn of LED related to register Y
        "ldi 0x5",  # store 9 to register A
        "scall 0xC", # wait for 1 sec (specified by register A)
        "call 0x0" # back to the first line
        ]

# increment 7SEG by 1 sec
assembly = [
        "ldi 0x0", # register.A = 0
        "addi 0x1", # register A+1
        "outn", # output to segment LED related register A
        "st 0x0", # store memory address to register Y
        "ld", # store value of register A to memory
        "ldi 0xA", # register.A = 0
        "scall 0xC", # wait to 500 milsec
        "ld", # load value of register A from memory
        "call 0x1"
        ]

# increment binary LED by 1 sec
assembly = [
        "ldi 0xA", # register.A = 10 (0xC)
        "ldyi 0x0", # register.Y = 0 
        "addyi 0x1", # register Y+1 
        "scall 0x1", # output to binary LED related register Y
        "scall 0xC",
        "call 0x2"
        ]

# increment binary 桁が溢れた時の対応
assembly = [
        "addi 0x1", # add openrads to register A
        "ay", # change A and Y
        "scall 1", # turn on LED related to reigster Y
        "call 0x0" # jump 0x0 if register FLAG is 1
        ]
assembly = """
_start:
    ldi 0x1
    call increment
_increment:
    addi 0x1
    ay
    scall 1
    ret
"""


assembly = [ 
        "ldyi 0x0", # start        #0
        "call 0xB", # incLoop      #1
        "addyi 0x1",               #2
        "cpyi 0x7",                #3
        "jmpf 0x1",                #4
        "ldyi 0x6",                #5
        "addyi 0xf", # decLoop     #6
        "call 0xB",                #7
        "cpyi 0x1",                #8
        "jmpf 0x6",                #9
        "jmpf 0x0",                #A
        "scall 0x1", # ledOnOff    #B
        "ldi 0x0",                 #C
        "scall 0xc",               #D
        "scall 0x2",               #E
        "ret"                      #F
        ]


for i in range(len(assembly)):
    memory[i] = assembly[i]

print("=====Assembly=====")
for row in assembly:
    print(row)
print("==================")

def convert_to_hex(val):
    return int(val, 16)

freq = 10_000
freq = 50
interval = 1/freq

while True:
    time.sleep(interval)
    #print(register.PC) 

    #########
    # FETCH #
    #########
    try:
        instruction = memory[register.PC]
        if instruction == 0x00:
            break
    except IndexError:
        break

    ##########
    # DECODE #
    ##########
    #print("debug {}".format(register.PC))
    instruction = memory[register.PC]
    #print("   :",register.PC, instruction)
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
    led = ",".join(list(map(str, LED)))
    ports = ",".join(list(map(str, PORTS)))
    msg = "\rLED:{} PORTS:{} 7SEG:{} RA:{},RY:{},PC:{}".format(led, ports, SEG_LED, register.A, register.Y, register.PC)
    #msg = "LED:{} PORTS:{} 7SEG:{} RA:{},RY:{},PC:{} INST:{} stack:{}\n".format(led, ports, SEG_LED, register.A, register.Y, register.PC, instruction,  "".join(list(map(str,memory[240:]))))
    print(msg, end="")
    #print(memory)
    #print(LED)
