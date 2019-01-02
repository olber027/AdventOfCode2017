'''
As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this device on your wrist works. You have a little while before you reach your next destination, and with a bit of trial and error, you manage to pull up a programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:

addr (add register) stores into register C the result of adding register A and register B.
addi (add immediate) stores into register C the result of adding register A and value B.
Multiplication:

mulr (multiply register) stores into register C the result of multiplying register A and register B.
muli (multiply immediate) stores into register C the result of multiplying register A and value B.
Bitwise AND:

banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
Bitwise OR:

borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
Assignment:

setr (set register) copies the contents of register A into register C. (Input B is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)
Greater-than testing:

gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
Equality testing:

eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.
None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?
'''

class Register(object):
    def __init__(self, id, initialValue=0):
        self.value = initialValue
        self.id = id

    def getValue(self):
        return self.value

    def set(self, newVal):
        self.value = newVal

    def __repr__(self):
        return "{} : {}".format(self.id, self.value)


class RegisterSet(object):
    def __init__(self, registerIDs):
        self.registers = {}
        for id in registerIDs:
            self.registers[id] = Register(id)

    def getRegister(self, id):
        if id in self.registers:
            return self.registers[id]
        return None

    def addRegister(self, register):
        self.registers[register.id] = register

    def update(self, id, value):
        self.registers[id].set(value)

    def updateMultiple(self, ids, values):
        for id, value in zip(ids, values):
            self.registers[id].set(value)

    def getRegisterIDs(self):
        return self.registers.keys()

    def getRegisters(self, ids):
        return [self.getRegister(id) for id in ids]

    def getAllRegisters(self):
        return sorted(self.registers.values(), key=(lambda x: x.id))


class Instruction(object):
    def __init__(self, func, id=None, name=None):
        self.function = func
        self.id = id
        self.name = name

    def run(self, firstArg, secondArg, thirdArg, registerSet):
        self.function(firstArg, secondArg, thirdArg, registerSet)

    def __repr__(self):
        return "{} : {}".format(self.name, self.id)


class InstructionSet(object):
    def __init__(self):
        self.instructions = []

    def addInstruction(self, instruction):
        self.instructions.append(instruction)

    def getInstructionByName(self, name):
        for instruction in self.instructions:
            if instruction.name == name:
                return instruction
        return None

    def getInstructionByID(self, id):
        for instruction in self.instructions:
            if instruction.id == id:
                return instruction
        return None

    def getAllInstructions(self):
        return self.instructions

    def updateInstructionName(self, id, newName):
        for instruction in self.instructions:
            if instruction.id == id:
                instruction.name = newName

    def updateInstructionID(self, newID, name):
        for instruction in self.instructions:
            if instruction.name == name:
                instruction.id= newID

    def getNumInstructions(self):
        return len(self.instructions)

    def __repr__(self):
        result = ""
        for inst in sorted(self.instructions, key=(lambda x: x.id)):
            result += "{}\n".format(inst)
        return result


class System(object):
    def __init__(self, instructionSet, registerSet):
        self.registerSet = registerSet
        self.instructionSet = instructionSet

    def run(self, args, instructionName=None, instructionID=None):
        instructionToRun = None
        if instructionName is not None:
            instructionToRun = self.instructionSet.getInstructionByName(instructionName)
        if instructionID is not None:
            instructionToRun = self.instructionSet.getInstructionByID(instructionID)
        instructionToRun.run(args[0], args[1], args[2], self.registerSet)

    def getAllRegisters(self):
        return self.registerSet.getAllRegisters()

    def getAllInstructions(self):
        return self.instructionSet.getAllInstructions()

    def setRegisters(self, id_value_pairs):
        for pair in id_value_pairs:
            self.registerSet.update(pair[0], pair[1])

    def checkRegisters(self, id_value_pairs):
        for pair in id_value_pairs:
            if self.registerSet.getRegister(pair[0]).getValue() != pair[1]:
                return False
        return True

def addr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(firstVal + secondVal)

def addi(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(firstVal + secondVal)

def mulr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(firstVal * secondVal)

def muli(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(firstVal * secondVal)

def banr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(firstVal & secondVal)

def bani(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(firstVal & secondVal)

def borr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(firstVal | secondVal)

def bori(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(firstVal | secondVal)

def setr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    registers.getRegister(third).set(firstVal)

def seti(first, second, third, registers):
    firstVal = first
    registers.getRegister(third).set(firstVal)

def gtir(first, second, third, registers):
    firstVal = first
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(int(firstVal > secondVal))

def gtri(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(int(firstVal > secondVal))

def gtrr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(int(firstVal > secondVal))

def eqir(first, second, third, registers):
    firstVal = first
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(int(firstVal == secondVal))

def eqri(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = second
    registers.getRegister(third).set(int(firstVal == secondVal))

def eqrr(first, second, third, registers):
    firstVal = registers.getRegister(first).getValue()
    secondVal = registers.getRegister(second).getValue()
    registers.getRegister(third).set(int(firstVal == secondVal))

instructions = InstructionSet()
instructions.addInstruction(Instruction(addr, name="addr"))
instructions.addInstruction(Instruction(addi, name="addi"))
instructions.addInstruction(Instruction(mulr, name="mulr"))
instructions.addInstruction(Instruction(muli, name="muli"))
instructions.addInstruction(Instruction(banr, name="banr"))
instructions.addInstruction(Instruction(bani, name="bani"))
instructions.addInstruction(Instruction(borr, name="borr"))
instructions.addInstruction(Instruction(bori, name="bori"))
instructions.addInstruction(Instruction(setr, name="setr"))
instructions.addInstruction(Instruction(seti, name="seti"))
instructions.addInstruction(Instruction(gtir, name="gtir"))
instructions.addInstruction(Instruction(gtri, name="gtri"))
instructions.addInstruction(Instruction(gtrr, name="gtrr"))
instructions.addInstruction(Instruction(eqir, name="eqir"))
instructions.addInstruction(Instruction(eqri, name="eqri"))
instructions.addInstruction(Instruction(eqrr, name="eqrr"))

numRegisters = 4
registerIDs = [id for id in range(numRegisters)]
registers = RegisterSet(registerIDs)

fakeSystem = System(instructions, registers)

file = open("InputFiles/Day16.dat", "r")

line = file.readline()
numAmbiguousInstructions = 0

while "Before" in line:
    initialRegisterValues = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    line = file.readline()
    instructionID = [int(x) for x in line.split()][0]
    instructionArguments = [int(x) for x in line.split()][1:]
    line = file.readline()
    finalRegisterValues = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]

    matchingInstructions = 0

    for instruction in fakeSystem.getAllInstructions():
        fakeSystem.setRegisters(zip(registerIDs, initialRegisterValues))
        fakeSystem.run(instructionArguments, instruction.name)

        if fakeSystem.checkRegisters(zip(registerIDs, finalRegisterValues)):
            matchingInstructions += 1

    if matchingInstructions >= 3:
        numAmbiguousInstructions += 1

    #read blank line
    line = file.readline()
    line = file.readline()

print(numAmbiguousInstructions)
