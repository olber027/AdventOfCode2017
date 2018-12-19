'''
Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
'''

import string

class System(object):
    def __init__(self, numRegisters=4):
        self.registers = [0 for _ in range(numRegisters)]
        self.opCodes = []

    def addOpCode(self, opCode):
        self.opCodes.append(opCode)
        self.opCodes.sort(key=(lambda x: x.number))

    def updateRegisters(self, newVals):
        if len(newVals) != len(self.registers):
            return False
        for i in range(len(self.registers)):
            self.registers[i] = newVals[i]
        return True

    def updateRegister(self, registerNum, newVal):
        if registerNum < 0 or registerNum > len(self.registers):
            return False
        self.registers[registerNum] = newVal
        return True

    def getOp(self, opNum=None, opName=None):
        op = None
        if opNum:
            searchResult = [opCode for opCode in self.opCodes if opCode.number == opNum]
            op = searchResult[0] if searchResult else None
        elif opName:
            searchResult = [opCode for opCode in self.opCodes if opCode.name == opName]
            op = searchResult[0] if searchResult else None
        return op

    def runOpCode(self, inputRegister, secondArgument, outputRegister, opNumber=None, opName=None):
        op = self.getOp(opNumber, opName)

        if op:
            op.run(self.registers, inputRegister, secondArgument, outputRegister)
            return True
        return False

    def getMatchingOps(self, initialRegisters, firstArg, secondArg, thirdArg, finalRegisters):
        results = []
        for op in self.opCodes:
            self.updateRegisters(initialRegisters)
            op.run(self.registers, firstArg, secondArg, thirdArg)
            matched = False not in [self.registers[i] == finalRegisters[i] for i in range(len(self.registers))]
            if matched:
                results.append(op)

        return results

    def updateOpNumber(self, opName, newNumber):
        for op in self.opCodes:
            if op.name == opName:
                op.number = newNumber
                self.opCodes.sort(key=(lambda x: x.number))
                return True
        return False

class OpCode(object):
    def __init__(self, opName, opNumber, operation, registerAsSecondInput=False, valueAsFirstInput=False):
        self.name = opName
        self.number = opNumber
        self.registerAsSecondInput = registerAsSecondInput
        self.valueAsFirstInput = valueAsFirstInput
        self.operation = operation

    def run(self, registers, firstArgument, secondArgument, outputRegister):
        firstArg = registers[firstArgument] if not self.valueAsFirstInput else firstArgument
        secondArg = secondArgument if not self.registerAsSecondInput else registers[secondArgument]
        registers[outputRegister] = self.operation(firstArg, secondArg)

    def setName(self, newName):
        self.name = newName

    def setNumber(self, newNum):
        self.number = newNum

    def __repr__(self):
        return "{} : {}".format(self.name, self.number)
        # return self.name

fakeSystem = System()
#                                        z = reg[x] + reg[y]
fakeSystem.addOpCode(OpCode("addr", -1, (lambda x,y: x + y), True))
#                                        z = reg[x] + y
fakeSystem.addOpCode(OpCode("addi", -1, (lambda x,y: x + y)))

#                                        z = reg[x] * reg[y]
fakeSystem.addOpCode(OpCode("mulr", -1, (lambda x,y: x * y), True))
#                                        z = reg[x] * y
fakeSystem.addOpCode(OpCode("muli", -1, (lambda x,y: x * y)))

#                                        z = reg[x] & reg[y]
fakeSystem.addOpCode(OpCode("banr", -1, (lambda x,y: x & y), True))
#                                        z = reg[x] & y
fakeSystem.addOpCode(OpCode("bani", -1, (lambda x,y: x & y)))

#                                        z = reg[x] | reg[y]
fakeSystem.addOpCode(OpCode("borr", -1, (lambda x,y: x | y), True))
#                                        z = reg[x] | y
fakeSystem.addOpCode(OpCode("bori", -1, (lambda x,y: x | y)))

#                                        z = reg[x]
fakeSystem.addOpCode(OpCode("setr", -1, (lambda x,y: x)))
#                                        z = x
fakeSystem.addOpCode(OpCode("seti", -1, (lambda x,y: x), False, True))

#                                        z = 1 if x > reg[y] else 0
fakeSystem.addOpCode(OpCode("gtir", -1, (lambda x,y: int(x > y)), True, True))
#                                        z = 1 if reg[x] > y else 0
fakeSystem.addOpCode(OpCode("gtri", -1, (lambda x,y: int(x > y))))
#                                        z = 1 if reg[x] > reg[y] else 0
fakeSystem.addOpCode(OpCode("gtrr", -1, (lambda x,y: int(x > y)), True))

#                                        z = 1 if x == reg[y] else 0
fakeSystem.addOpCode(OpCode("eqir", -1, (lambda x,y: int(x == y)), True, True))
#                                        z = 1 if reg[x] == y else 0
fakeSystem.addOpCode(OpCode("eqri", -1, (lambda x,y: int(x == y))))
#                                        z = 1 if reg[x] == reg[y] else 0
fakeSystem.addOpCode(OpCode("eqrr", -1, (lambda x,y: int(x == y)), True))

file = open("InputFiles/Day16.dat", "r")

line = file.readline()
numAmbiguousOpCodes = 0

possibleOps = {}

for i in range(len(fakeSystem.opCodes)):
    possibleOps[i] = set([op for op in fakeSystem.opCodes])

while "Before" in line:
    initialRegs = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    line = file.readline()
    opArgs = [int(x.strip()) for x in line.split(" ")]
    line = file.readline()
    finalRegs = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    file.readline() # skip blank line
    line = file.readline()

    matchingOps = set(fakeSystem.getMatchingOps(initialRegs, opArgs[1], opArgs[2], opArgs[3], finalRegs))
    possibleOps[opArgs[0]].intersection_update(matchingOps)

certainOps = set()

changed = True
while changed:
    changed = False
    for opNum, ops in possibleOps.items():
        ops.difference_update(certainOps)
        if len(ops) == 1:
            fakeSystem.updateOpNumber(list(ops)[0].name, opNum)
            certainOps.update(ops)
            changed = True

[print(x) for x in fakeSystem.opCodes]
fakeSystem.updateRegisters([0,0,0,0])

while line in string.whitespace:
    line = file.readline().strip()

print(fakeSystem.registers)
while line:
    opArgs = [int(x.strip()) for x in line.split(" ")]
    print("{} : {} {} {}".format(fakeSystem.getOp(opNum=opArgs[0]), opArgs[1], opArgs[2], opArgs[3]))
    fakeSystem.runOpCode(opArgs[1], opArgs[2], opArgs[3], opArgs[0])
    print(fakeSystem.registers)
    line = file.readline()