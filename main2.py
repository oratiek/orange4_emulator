import os
import sys
import time

class Memory:
    def __init__(self):
        self.memory = [0x0 for i in range(0xFF)]
    
    def Ar(self):
        self.Ar = self.memory[0x6F]

    def Br(self):
        self.Br = self.memory[0x6C]

    def Yr(self):
        self.Yr = self.memory[0x6E]
    
    def Zr(self):
        self.Zr = self.memory[0x6D]
    
    def Ar_(self):
        self.Ar_ = self.memory[0x69]

    def Br_(self):
        self.Br_ = self.memory[0x67]

    def Yr_(self):
        self.Yr_ = self.memory[0x68]

    def Zr_(self):
        self.Zr_ = self.memory[0x66]
    
    def store(self, val, index):
        self.memory[index] = val
    
    def load(self, val, index):
        return self.memory[index]
    
    def pop(self):
        pass

    def push(self):
        pass



class CPU:
    def __init__(self):
        self.memory = [0x0 for i in range(0x6F)]
        self.Ar = 0x66
        self.Br = 0x6C
        self.Yr = 0x6E
        self.Zr = 0x6D
        self.Adr = 0x69
        self.Bdr = 0x67
        self.Ydr = 0x68
        self.Zdr = 0x69

        self.LED = [0,0,0,0,0,0,0]
        self.SEG_LED = 0

        self.DATA_BASE = 0x50

        self.PC = 0
        self.SP = 0
        self.FLAG = 0
        self.STACKSIZE = 10
    
    def push(val):
        if self.SP > self.SP + self.STACKSIZE-1:
            return False
        self.memory[self.SP] = val
        return True
    
    def pop():
        if self.SP < 0:
            return False
        val = self.memory[self.SP]
        self.memory[self.SP] = 0
        self.memory[self.SP:]  = self.memory[self.SP+1:] + [0]
        return val

    def load(self,filepath):
        with open(filepath, "r") as f:
            for index, row in enumerate(f):
                self.memory[index] = int(row.strip("\n"), 16)
        print("loaded")
    
    def fetch(self):
        if self.PC < 0x4F:
            return self.memory[self.PC]
        else:
            raise Exception("Memory Overflow")

    def decode(self, inst):
        # return opecode and operands
        pass
    
    def scall(self, service_code):
        match service_code:
            case 0x0:
                self.LED = [0,0,0,0,0,0,0]
            case 0x1:
                if self.memory[self.Yr] > 127:
                    pass
                else:
                    val = int(self.memory[self.Yr])
                    binary = list(map(int, (bin(val)[2:])))
                    self.LED = [0 for i in range(7-len(binary))] + binary
            case 0x2:
                clean_LED = [0,0,0,0,0,0,0]
                binary = list(map(int, bin(self.memory[self.Yr])[2:]))
                clean_LED[len(self.LED)-len(binary):] = binary
                clean_LED = [1 - bit for bit in clean_LED]
                self.LED = clean_LED

    def execute(self, machine_code):
        match machine_code:
            case 0x0:
                # 押されたキーをArに代入
                pass
            case 0x1:
                # Arの値を数字LEDに点灯する
                if self.memory[self.Ar] > 127:
                    pass
                else:
                    val = int(self.memory[self.Ar])
                    binary = list(map(int, (bin(val)[2:])))
                    self.LED = [0 for i in range(7-len(binary))] + binary
            case 0x2:
                # ArとBrを入れ替える
                tmp = self.memory[self.Ar]
                self.memory[self.Ar] = self.memory[self.Yr]
                self.memory[self.Yr] = tmp
            case 0x3:
                # Arの値をデータメモリ(0x50+Yr)番地の値をArに代入
                addr = self.memory[self.Yr] + 0x50
                self.memory[addr] = self.memory[self.Ar]
            case 0x4: #st
                # memory[Yr + 0x50] = Ar
                self.memory[self.Yr + 0x50] = self.memory[self.Ar]
            case 0x5: # ld
                # Ar = memory[Yr + 0x50]
                self.memory[self.Ar] = self.memory[self.Yr + 0x50]
            case 0x6: # add
                # Ar + memory[Yr + 0x50]
                self.memory[self.Ar] += self.memory[self.Yr + 0x50]
                # 桁上がり確認
            case 0x7: # sub
                # Ar + memory[Yr + 0x50]
                self.memory[self.Ar] -= self.memory[self.Yr + 0x50]
                # 負数確認
            case 0x8: # 1 operand
                self.PC += 1 
                operand = self.fetch()
                self.memory[self.Ar] = operand
            case 0x9:
                # Ar += operand
                self.PC += 1
                operand = self.fetch()
                self.memory[self.Ar] += operand
                # 桁上がり(?)でフラグ
            case 0xA:
                # Yr = operand
                self.PC += 1
                operand = self.fetch()
                self.memory[self.Yr] = operand
            case 0xB:
                # Yr += operand
                self.PC += 1
                operand = self.fetch()
                self.memory[self.Yr] -= operand
                # 桁上がり(?)を確認
            case 0xC:
                # Ar == operand 
                self.PC += 1
                operand = self.fetch()
                if self.memory[self.Ar] == operand:
                    self.FLAG = 0
                else:
                    self.FLAG= 1
            case 0xD:
                # Yr == operand
                self.PC += 1
                operand = self.fetch()
                if self.memory[self.Yr] == operand:
                    self.FLAG = 0
                else:
                    self.FLAG = 1
            case 0xE:
                # scall
                self.PC += 1
                operand = self.fetch()
                self.scall(operand)
            case 0xF:
                if self.FLAG == 1:
                    self.PC += 1
                    operand = self.fetch()
                    self.PC = operand
            case 0xF60:
                # call
                self.PC += 1
                operand = self.fetch() # put this address to stack
                self.PC = operand - 1
            case 0xF61:
                # ret
                # get call address from stack
                pass

    def main(self):
        print(self.memory)
        while True:
            # fetch
            try:
                inst = self.fetch()
            except Exception:
                print("done")
                break
            # execute
            self.execute(inst)
            self.PC += 1
            msg = "\rLED:{} PC{} INST{} Yr{} Ar{}".format(self.LED, self.PC, inst, self.memory[self.Yr], self.memory[self.Ar])
            print(msg, end="")
            time.sleep(0.05)

if __name__ == "__main__":
    cpu = CPU()
    cpu.load("night_rider.txt")
    cpu.main()
