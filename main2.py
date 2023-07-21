import os
import sys
import time

class Memory:
    def __init__(self):
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

        self.LED = [0,0,0,0,0,0]
        self.SEG_LED = 0

        self.PC = 0
        self.SP = 0
        self.FLAG = 0

    def load(self,filepath):
        with open(filepath, "r") as f:
            for index, row in enumerate(f):
                self.memory[index] = int(row.strip("\n"), 16)
        print("loaded")
    
    def fetch(self):
        if self.PC != 0x4F:
            return self.memory[self.PC]
        return False
    
    def decode(self, inst):
        # return opecode and operands
        pass
    
    def scall(self, service_code):
        match service_code:
            case 0x0:
                self.LED = [0,0,0,0,0,0,0]
            case 0x1:
                clean_LED = [0,0,0,0,0,0,0]
                binary = list(map(int, (bin(self.memory[self.Yr])[2:])))
                clean_LED[len(self.LED)-len(binary):] = binary
                self.LED = clean_LED
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
                clean_LED = [0,0,0,0,0,0,0]
                binary = list(map(int, (bin(self.memory[self.Yr])[2:])))
                clean_LED[len(self.LED)-len(binary):] = binary
                self.LED = clean_LED
            case 0x2:
                # ArとBrを入れ替える
                pass
            case 0x3:
                # Arの値をデータメモリ(50+Yr)番地の値をArに代入
                pass
            case 0x4:
                # memory[Yr + 0x50] = Ar
                self.memory[self.Yr + 0x50] = self.memory[self.Ar]
            case 0x5:
                # Ar = memory[Yr + 0x50]
                self.memory[self.Ar] = self.memory[self.Yr + 0x50]
            case 0x6:
                # Ar + memory[Yr + 0x50]
                self.memory[self.Ar] += self.memory[self.Yr + 0x50]
                # 桁上がりを見る
            case 0x7:
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
                self.memory[self.Yr] += operand
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
                self.PC += 1
                operand = self.fetch()
                self.PC = operand

    def main(self):
        while True:
            # fetch
            inst = self.fetch()
            if inst == False:
                break
            # execute
            self.execute(inst)
            self.PC += 1
            msg = "\rLED:{} INST{}".format(self.LED,inst)
            print(msg, end="\n")
            time.sleep(0.2)

if __name__ == "__main__":
    cpu = CPU()
    cpu.load("sample.txt")
    cpu.main()
