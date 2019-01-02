'''
Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
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
instructionNames = [inst.name for inst in fakeSystem.getAllInstructions()]

instructionMatchings = {}
for id in range(fakeSystem.instructionSet.getNumInstructions()):
    instructionMatchings[id] = set(instructionNames)

while "Before" in line:
    initialRegisterValues = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    line = file.readline()
    instructionID = [int(x) for x in line.split()][0]
    instructionArguments = [int(x) for x in line.split()][1:]
    line = file.readline()
    finalRegisterValues = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]

    matchingInstructions = set()

    for instruction in fakeSystem.getAllInstructions():
        fakeSystem.setRegisters(zip(registerIDs, initialRegisterValues))
        fakeSystem.run(instructionArguments, instruction.name)

        if fakeSystem.checkRegisters(zip(registerIDs, finalRegisterValues)):
            matchingInstructions.add(instruction.name)

    instructionMatchings[instructionID].intersection_update(matchingInstructions)

    #read blank line
    line = file.readline()
    line = file.readline()

changed = True

while changed:
    changed = False
    for (key, value) in instructionMatchings.items():
        if len(value) == 1:
            name = instructionMatchings[key].pop()
            itemToRemove = set([name])
            fakeSystem.instructionSet.updateInstructionID(key, name)
            for matchings in instructionMatchings.values():
                matchings.difference_update(itemToRemove)
            changed = True

# read blank lines
line = file.readline()
line = file.readline()

fakeSystem.setRegisters(zip(registerIDs, [0 for _ in range(numRegisters)]))

while line:
    instructionID = [int(x) for x in line.split()][0]
    instructionArguments = [int(x) for x in line.split()][1:]
    fakeSystem.run(instructionArguments, None, instructionID)
    line = file.readline()

[print(register) for register in fakeSystem.getAllRegisters()]