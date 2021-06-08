from tkinter import *
import tkinter as tk
import re
from tkinter.filedialog import *
import os.path
import sys

filename = "Untitled"
fileexists = False

Address = { 'SP' : 8040, 'BP' : 8044, 'SI' : 8048, 'DI' : 8052, 'AL' : 8218, 'AH' : 8220, 'BL' : 8222, 'BH' : 8224, 'CL' : 8226, 'CH' : 8228, 'DL' : 8230, 'DH' : 8232 }
GPR_Values = {'AL' : 0, 'AH' : 0, 'BL' : 0, 'BH' : 0, 'CL' : 0, 'CH' : 0, 'DL' : 0, 'DH' : 0}
Opcodes = {'MOV' : 4122, 'XCHG' : 4126, 'ADD' : 4130, 'INC' : 4134, 'SUB' : 4138, 'DEC' : 4142, 'MUL' : 4146, 'NAND' : '4150', 'NOR' : 4154, 'NEG' : 4158, 'SHR' : 4162, 'STC' : 4166, 'CLC' : 4170, 'CMC' : 4174, 'CLD' : 4178, 'NOT' : 7182, 'OR' : 7186, 'AND' : 7190 }
Flage_Registers_Values = { 'CF' : 0, 'PF' : 0, 'AF' : 0, 'ZF' : 0, 'SF' : 0, 'TF' : 0, 'IF' : 0, 'DF' : 0, 'OF' : 0 }

def binary_to_decimal(binary):
    i,integer = 0,0
    size = len(binary)
    while i < len(binary):
        integer += int(binary[size - 1 - i])*pow(2,i)
        i+=1
    return integer

def NOT(A):
    a=str(A)
    temp=["1" if i=="0" else "0" for i in A]
    out=""
    return out.join(temp)
        
def AND(A,B):
    A = bin(int(A))
    B = bin(int(B))
    A = str(A)
    A = A[2:]
    B = str(B)
    B = B[2:]
    output = str((int(A) & int(B)))
    return output;

def OR(A,B):
    A = bin(int(A))
    B = bin(int(B))
    A = str(A)
    A = A[2:]
    B = str(B)
    B = B[2:]
    output = str((int(A) | int(B)))
    return output;

def Code(instructions):
    code_split = re.split(" |, |\(|\)", instructions)
    args = []
    for i in range (len(code_split)):
        if (code_split[i] != ""):
            args.append(code_split[i])
        
    if(len(args) > 3):
        print("Syntax Error")
        
    elif(args[0] in Opcodes):
        opcode = Opcodes.get(args[0])
        opstr = hex(int(opcode))
        if(len(args) >= 2):
            rd = Address.get(args[1])
            rdstr = hex(int(rd))
        if(len(args) == 3):
            if(args[2][0] == '#'):
                rs = args[2][1:-1]
                rsstr = hex(int(rs))
                rsstr = '#' + rsstr[2:]
            
            else:
                rs = Address.get(args[2])
                rsstr = hex(rs)
        elif(len(args) == 2):
            rsstr = ''
        else:
            rsstr = ''
            rdstr = ''
        instruct = opstr + "     " + rdstr + "     " + rsstr
        print(instruct)

        if(args[0] == 'MOV'):
            if(args[2] in GPR_Values):
                GPR_Values[args[1]] = GPR_Values[args[2]]
            else:
                GPR_Values[args[1]] = rs
            print(rd, rs)
        
        elif(args[0] == 'XCHG'):
            temp = GPR_Values[args[1]]
            GPR_Values[args[1]] = GPR_Values[args[2]]
            GPR_Values[args[2]] = temp
        
        elif(args[0] == 'ADD'):
            temp = int(GPR_Values[args[1]])
            temp += int(GPR_Values[args[2]])
            GPR_Values[args[1]] = temp
            
        elif(args[0] == 'INC'):
            temp = int(GPR_Values[args[1]])
            temp += int(rs)
            GPR_Values[args[1]] = temp
            
        elif(args[0] == 'SUB'):
            temp = int(GPR_Values[args[1]])
            temp -= int(GPR_Values[args[2]])
            GPR_Values[args[1]] = temp
            
        elif(args[0] == 'DEC'):
            temp = int(GPR_Values[args[1]])
            temp -= int(rs)
            GPR_Values[args[1]] = temp
            
        elif(args[0] == 'MUL'):
            temp = int(GPR_Values[args[1]])
            temp *= int(GPR_Values[args[2]])
            GPR_Values[args[1]] = temp
            
        elif(args[0] == 'NEG'):
            GPR_Values[args[1]] -= 1 
            GPR_Values[args[1]] = bin(GPR_Values[rd])
            GPR_Values[args[1]] = GPR_Values[args[1]][2:]
            GPR_Values[args[1]] = NOT(GPR_Values[args[1]])
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
               
        elif(args[0] == 'NOT'):
            GPR_Values[args[1]] = bin(int(GPR_Values[args[1]]))
            GPR_Values[args[1]] = GPR_Values[args[1]][2:]
            GPR_Values[args[1]] = NOT(GPR_Values[args[1]])
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            
        elif(args[0] == 'AND'):
            GPR_Values[args[1]] = AND(GPR_Values[args[1]], GPR_Values[args[2]])
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            
        elif(args[0] == 'OR'):
            GPR_Values[args[1]] = OR(GPR_Values[args[1]], GPR_Values[args[2]])
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            
        elif(args[0] == 'NAND'):
            GPR_Values[args[1]] = NOT(AND(GPR_Values[args[1]], GPR_Values[args[2]]))
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            
        elif(args[0] == 'NOR'):
            GPR_Values[args[1]] = NOT(OR(GPR_Values[args[1]], GPR_Values[args[2]]))
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            
        elif(args[0] == 'SHR'): #10111011(BB) => 11101100(EC) 101110(2C)
            GPR_Values[args[1]] = bin(int(GPR_Values[args[1]]))
            GPR_Values[args[1]] = GPR_Values[args[1]][2+int(rs):] + (0*rs)
            GPR_Values[args[1]] = binary_to_decimal(GPR_Values[args[1]])
            GPR_Values[args[1]] = int(GPR_Values[args[1]])
            
        elif(args[0] == 'STC'):
            Flage_Registers_Values['CF'] = 1
    
        elif(args[0] == 'CLC'):
            Flage_Registers_Values['CF'] = 0
        
        elif(args[0] == 'CMC'):
            if(Flage_Registers_Values['CF'] == 0):
                Flage_Registers_Values['CF'] = 1
            else:
                Flage_Registers_Values['CF'] = 0
            
        elif(args[0] == 'CLD'):
            Flage_Registers_Values['DF'] = 0
        return instruct    
    else:
        print("'",args[0],"'", " : No such instruction available !")
        return str(0);

def decode(instructions):
    Machine_Level_Instruction = Code(instructions)
    return Machine_Level_Instruction
    
def openFile():
    global filename
    openfilename = askopenfilename()
    if openfilename is not None:
        filename = openfilename
        asmfile = open(filename, "r")
        asmfile.seek(0)
        asmdata = asmfile.read()
        textArea.delete("1.0", "end - 1c")
        textArea.insert("1.0", asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = NORMAL)
        frame.title("8086 Assembler [" + filename + "]")
        frame.focus()
    
def saveFile():
    global filename
    asmdata = textArea.get("1.0", "end - 1c")
    asmfile = open(filename, "w")
    asmfile.seek(0)
    asmfile.truncate()
    asmfile.write(asmdata)
    asmfile.close()

def saveFileAs():
    global filename
    global fileexists
    saveasfilename = asksaveasfilename()
    if saveasfilename is not None:
        filename = saveasfilename
        fileexists = True
        asmdata = textArea.get("1.0", "end - 1c")
        asmfile = open(filename, "w")
        asmfile.seek(0)
        asmfile.truncate()
        asmfile.write(asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = NORMAL)
        frame.title("8086 Assembler [" + filename + "]")
        frame.focus()
           
def exitApp():
    frame.destroy()
    sys.exit()
    
def compileASM():
    global filename
    cpu_out = ""
    asm_in = textArea.get("1.0", END)
    asmlines = re.split("\n", asm_in)
    for i in range (len(asmlines)):
        if (asmlines[i] != ""):
            #print asmlines[i]
            cpu_out += str(i) + " | " + decode(asmlines[i]) + " | " + asmlines[i] + "\n"
    #print cpu_out
    name, ext = os.path.splitext(filename)
    hexfilename = name + "_hex.txt"
    hexfile = open(hexfilename, "w")
    hexfile.seek(0)
    hexfile.truncate()
    hexfile.write(cpu_out)
    hexfile.close()
  
