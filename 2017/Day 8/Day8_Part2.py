class Register(object):
    def __init__(self, name):
        self.value = 0
        self.name = name
    def __lt__(self, other):
        return self.value < other
    def __gt__(self, other):
        return self.value > other
    def __eq__(self, other):
        return self.name == other
    def __repr__(self):
        return "{0} : {1}".format(self.name, self.value)
    def increment(self, val):
        self.value += val
    def decrement(self, val):
        self.value -= val

def condition(register, operator, value):
    val = int(value)
    if operator == "==":
        return register.value == val
    elif operator == "!=":
        return register.value != val
    elif operator == "<":
        return register.value < val
    elif operator == ">":
        return register.value > val
    elif operator == "<=":
        return register.value <= val
    elif operator == ">=":
        return register.value >= val
    return False

file = open("InputFiles/Day8.dat")
lines = file.read().splitlines()
file.close()

registers = []

for line in lines:
    words = line.split(" ")
    registers.append(Register(words[0]))

largestValue = -1

for line in lines:
    words = line.split(" ")
    target = registers[registers.index(words[0])]
    conditionalRegister = registers[registers.index(words[4])]
    operator = words[5]

    if condition(conditionalRegister, operator, words[6]):
        if words[1] == "inc":
            target.increment(int(words[2]))
        else:
            target.decrement(int(words[2]))
    if target.value > largestValue:
        largestValue = target.value

print(largestValue)
