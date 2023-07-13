import sys
import time
import tkinter as tk

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

register = Register()
memory = [0x0 for i in range(0xff)]
stack_index = 0
stack_size = 10
LED = [0, 0, 0, 0, 0, 0, 0]
PORT_MAX = 5
PORTS = [0 for i in range(PORT_MAX)]
SEG_LED = 0
OUTPUT_BIT = 7
def push(val):
    global stack_index
    if stack_index > stack_size-1:
        return False
    memory[stack_index] = val 
    stack_index += 1
    return True

def pop():
    if stack_index < 0:
        return False
    val = memory[0]
    memory[0] = 0
    memory[0:] = memory[1:] + [0]
    return val

# Lチカ
assembly = [
        "ldyi 0x0",
        "scall 1",
        "ldi 0x9",
        "scall 0xC",
        "scall 2",
        "ldi 9",
        "scall 0xC",
        "call 0x0"
        ]


for i in range(len(assembly)):
    memory[i] = assembly[i]

print("=====Assembly=====")
for row in assembly:
    print(row)
print("==================")

def convert_to_hex(val):
    return int(val, 16)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("350x300")
        master.title("Orange4")

        # First Row
        first_row_y = 80
        self.ButtonC = tk.Button(master, text="C", font=("serif",30), height=1, width=2)
        self.ButtonC.place(x=20, y=first_row_y)
        self.ButtonD = tk.Button(master, text="A", font=("serif",30), height=1, width=2)
        self.ButtonD.place(x=80, y=first_row_y)
        self.ButtonE = tk.Button(master, text="E", font=("serif",30), height=1, width=2)
        self.ButtonE.place(x=140, y=first_row_y)
        self.ButtonF = tk.Button(master, text="F", font=("serif",30), height=1, width=2)
        self.ButtonF.place(x=200, y=first_row_y)
        self.ButtonADR = tk.Button(master, text="ADR", font=("serif",30), height=1, width=3)
        self.ButtonADR.place(x=260, y=first_row_y)

        # Second row 
        second_row_y = 130
        self.Button8 = tk.Button(master, text="8", font=("serif",30), height=1, width=2)
        self.Button8.place(x=20, y=second_row_y)
        self.Button9 = tk.Button(master, text="9", font=("serif",30), height=1, width=2)
        self.Button9.place(x=80, y=second_row_y)
        self.ButtonA = tk.Button(master, text="A", font=("serif",30), height=1, width=2)
        self.ButtonA.place(x=140, y=second_row_y)
        self.ButtonB = tk.Button(master, text="B", font=("serif",30), height=1, width=2)
        self.ButtonB.place(x=200, y=second_row_y)
        self.ButtonADR = tk.Button(master, text="INC", font=("serif",30), height=1, width=3)
        self.ButtonADR.place(x=260, y=second_row_y)

        # Third row
        third_row_y = 180
        self.Button4 = tk.Button(master, text="4", font=("serif",30), height=1, width=2)
        self.Button4.place(x=20, y=third_row_y)
        self.Button5 = tk.Button(master, text="5", font=("serif",30), height=1, width=2)
        self.Button5.place(x=80, y=third_row_y)
        self.Button6 = tk.Button(master, text="6", font=("serif",30), height=1, width=2)
        self.Button6.place(x=140, y=third_row_y)
        self.Button7 = tk.Button(master, text="7", font=("serif",30), height=1, width=2)
        self.Button7.place(x=200, y=third_row_y)
        self.ButtonADR = tk.Button(master, text="RUN", font=("serif", 30), height=1, width=3)
        self.ButtonADR.place(x=260, y=third_row_y)

        # Forth row
        forth_row_y = 230
        self.Button0 = tk.Button(master, text="0", font=("serif",30), height=1, width=2)
        self.Button0.place(x=20, y=forth_row_y)
        self.Button1 = tk.Button(master, text="1", font=("serif",30), height=1, width=2)
        self.Button1.place(x=80, y=forth_row_y)
        self.Button2 = tk.Button(master, text="2", font=("serif",30), height=1, width=2)
        self.Button2.place(x=140, y=forth_row_y)
        self.Button3 = tk.Button(master, text="3", font=("serif",30), height=1, width=2)
        self.Button3.place(x=200, y=forth_row_y)
        self.ButtonADR = tk.Button(master, text="RST", font=("serif", 30), height=1, width=3)
        self.ButtonADR.place(x=260, y=forth_row_y)

        # 
        self.register = Register()
        self.memory = [0x0 for i in range(0xff)]
        self.stack_index = 0
        self.stack_size = 10
        self.LED = [0, 0, 0, 0, 0, 0, 0]
        self.LED_R = 12
        self.PORT_MAX = 5 
        self.PORTS = [0 for i in range(PORT_MAX)] 
        self.SEG_LED = 0
        self.OUTPUT_BIT = 7

        # 7 segment LED
        self.seg_led = tk.Label(master, text=self.SEG_LED, font=("serif",50))
        self.seg_led.place(x=20, y=10)

        # binary LED
        self.led_canvas = tk.Canvas(master, width=220, height=50)
        #led_canvas.configure(bg="blue")
        self.led_canvas.place(x=100, y=15)
        for i in range(1,8):
            x1, y1 = 25*i, 20
            self.led_canvas.create_oval(x1,y1,x1+self.LED_R*2,y1+self.LED_R*2)


        # load assembly to memory
        # Lチカ
        assembly = [
            "ldyi 0x0",
            "scall 1",
            "ldi 0x9",
            "scall 0xC",
            "scall 2",
            "ldi 9",
            "scall 0xC",
            "call 0x0"
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
        for i in range(len(assembly)):
            self.memory[i] = assembly[i]

        # clock cycle
        self.freq = 100
        self.interval = int(1/self.freq*1000)
        self.after(self.interval, self.update)

    def service_call(self, code):
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
                self.LED = clean_LED
            case 0x2:
                clean_LED = [0,0,0,0,0,0,0]
                binary = list(map(int, bin(register.Y)[2:]))
                #LED[len(LED)-len(binary):] = binary
                clean_LED[len(LED)-len(binary):] = binary
                clean_LED = [1 - bit for bit in clean_LED]
                self.LED = clean_LED
            case 0x3:
                pass
            case 0x4:
                # Aレジスタの全ビットを反転する
                #if register.FLAG == 1:
                binary = list(map(int, bin(register.A)[2:]))
                reversed_binary = [1 - bit for bit in binary]
                self.register.A = int("0b"+"".join(map(str,reversed_binary)),2)
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
                pass
            case 0xD:
                pass
            case 0xE:
                pass
            case 0xF:
                pass

    def execute(self, mnemonic, operands):
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
                self.service_call(operands[0])
            case "jmpf":
                if register.FLAG == 1:
                    register.PC =  operands[0]
                else:
                    register.FLAG = 1
            case "call":
                register.PC = operands[0]
            case "ret": #呼び出し元に制御を戻す
                # callしたときのアドレスをどっかに残しておく
                pass
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

    def update(self):
        #########
        # FETCH #
        #########
        try:
            instruction = self.memory[self.register.PC]
            if instruction == 0x00:
                sys.exit(0)
        except IndexError:
            sys.exit(0)

        ##########
        # DECODE #
        ##########
        instruction = self.memory[register.PC]
        #print(register.PC, instruction)
        opecode, *operands = instruction.split(" ")
        operands = list(map(convert_to_hex, operands))

        #################
        # LOAD OPERANDS #
        #################

        ###########
        # EXECUTE #
        ###########
        register.PC += 1
        self.execute(opecode, operands)

        ##############
        # WRITE BACK #
        ##############
        led = ",".join(list(map(str, self.LED)))
        ports = ",".join(list(map(str, self.PORTS)))
        msg = "\rLED:{} PORTS:{} 7SEG:{}".format(led, ports, self.SEG_LED)
        print(msg, end="")
        #print(LED) 
        self.led_canvas.delete("all")
        for i in range(1,8):
            x1, y1 = 25*i, 20
            if self.LED[i-1] == 1:
                self.led_canvas.create_oval(x1,y1,x1+self.LED_R*2,y1+self.LED_R*2, fill="#ff0000")
            else:
                self.led_canvas.create_oval(x1,y1,x1+self.LED_R*2,y1+self.LED_R*2)

        self.after(self.interval, self.update)

 
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

