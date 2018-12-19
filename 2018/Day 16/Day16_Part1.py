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

    def runOpCode(self, inputRegister, secondArgument, outputRegister, opNumber=None, opName=None):
        op = None
        if opNumber:
            searchResult = [opCode for opCode in self.opCodes if opCode.number == opNumber]
            op = searchResult[0] if searchResult else None
        elif opName:
            searchResult = [opCode for opCode in self.opCodes if opCode.name == opName]
            op = searchResult[0] if searchResult else None

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
fakeSystem.addOpCode(OpCode("setr", -1, (lambda x,y: x + 0)))
#                                        z = x
fakeSystem.addOpCode(OpCode("seti", -1, (lambda x,y: x + 0), False, True))

#                                        z = 1 if x > reg[y] else 0
fakeSystem.addOpCode(OpCode("gtir", -1, (lambda x,y: int(x > y)), True, True))
#                                        z = 1 if reg[x] > y else 0
fakeSystem.addOpCode(OpCode("gtri", -1, (lambda x,y: int(x > y))))
#                                        z = 1 if reg[x] > reg[y] else 0
fakeSystem.addOpCode(OpCode("gtrr", -1, (lambda x,y: int(x > y)), True))

#                                        z = 1 if x == reg[y] else 0
fakeSystem.addOpCode(OpCode("eqir", -1, (lambda x,y: int(x == y)), True, True))
#                                        z = 1 if reg[x] == y else 0
fakeSystem.addOpCode(OpCode("addi", -1, (lambda x,y: int(x == y))))
#                                        z = 1 if reg[x] == reg[y] else 0
fakeSystem.addOpCode(OpCode("eqrr", -1, (lambda x,y: int(x == y)), True))

file = open("InputFiles/Day16.dat", "r")

line = file.readline()
numAmbiguousOpCodes = 0

while "Before" in line:
    initialRegs = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    line = file.readline()
    opArgs = [int(x.strip()) for x in line.split(" ")]
    line = file.readline()
    finalRegs = [int(x.strip()) for x in line.split(":")[1].strip().strip("[").strip("]").split(",")]
    file.readline() # skip blank line
    line = file.readline()

    matchingOps = fakeSystem.getMatchingOps(initialRegs, opArgs[1], opArgs[2], opArgs[3], finalRegs)
    if len(matchingOps) >= 3:
        numAmbiguousOpCodes += 1

print(numAmbiguousOpCodes)
