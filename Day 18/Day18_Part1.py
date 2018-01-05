import string

class Register(object):
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.lastPlayed = 0
    def __eq__(self, other):
        return self.name == other
    def __repr__(self):
        return "{0} - {1} ({2})".format(self.name, self.value, self.lastPlayed)

    def send(self):
        self.lastPlayed = self.value
    def set(self, other):
        self.value = other
    def add(self, other):
        self.value += other
    def mult(self, other):
        self.value *= other
    def mod(self, other):
        self.value = (self.value % other)
    def recover(self):
        if self.value == 0:
            return None
        else:
            return self.lastPlayed

def doAction(action, register, value):
    increment = 1
    if action == "snd":
        register.send()
    elif action == "set":
        register.set(value)
    elif action == "add":
        register.add(value)
    elif action == "mul":
        register.mult(value)
    elif action == "mod":
        register.mod(value)
    elif action == "rcv":
        if register.recover() is not None:
            print(register.lastPlayed)
    elif action == "jgz":
        if register.value != 0:
            increment = value
    return increment

def parseLine(line, registers):
    parts = line.split(" ")
    action = parts[0]
    registerName = parts[1]
    value = None
    if len(parts) > 2:
        value = parts[2]
    register = registers[registers.index(registerName)]
    if value is not None:
        if value[0] in string.ascii_lowercase:
            value = registers[registers.index(value)].value
        else:
            value = int(value)
    return doAction(action, register, value)


registers = []

file = open("InputFiles/Day18.dat")
lines = [line.strip() for line in file.readlines()]
for line in lines:
    name = line.split(" ")[1]
    if name not in registers:
        registers.append(Register(name))

index = 0

while index >= 0 and index < len(lines):
    index += parseLine(lines[index], registers)