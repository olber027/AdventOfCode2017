'''
You realize that 20 generations aren't enough. After all, these plants will need to last another 1500 years to even reach your timeline, not to mention your future.

After fifty billion (50000000000) generations, what is the sum of the numbers of all pots which contain a plant?
'''

class Pot(object):
    def __init__(self, num, hasPlant, left=None, right=None):
        self.hasPlant = hasPlant
        self.num = num
        self.left = left
        self.right = right

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def leftHasPlant(self):
        if self.left:
            return self.left.hasPlant
        return False

    def twoLeftHasPlant(self):
        if self.left:
            return self.left.leftHasPlant()
        return False

    def rightHasPlant(self):
        if self.right:
            return self.right.hasPlant
        return False

    def twoRightHasPlant(self):
        if self.right:
            return self.right.rightHasPlant()
        return False

    def checkRule(self, rule):
        conditions = [self.twoLeftHasPlant(), self.leftHasPlant(), self.hasPlant, self.rightHasPlant(), self.twoRightHasPlant()]
        return not any([conditions[i] != rule.conditions[i] for i in range(len(conditions))])

    def __repr__(self):
        result = "[{}]".format("#" if self.hasPlant else ".")
        l = self.left
        r = self.right
        while l:
            result = ("#" if l.hasPlant else ".") + result
            l = l.left
        while r:
            result += ("#" if r.hasPlant else ".")
            r = r.right
        return result

class Rule(object):
    def __init__(self, rule, result):
        self.conditions = []
        for i in range(len(rule)):
            if rule[i] == ".":
                self.conditions.append(False)
            else:
                self.conditions.append(True)
        self.result = True if result == "#" else False

    def __repr__(self):
        result = ""
        result += "".join(["#" if cond else "." for cond in self.conditions])
        result += " => "
        result += "#" if self.result else "."
        return result

def connect(generation):
    generation[0].setRight(generation[1])
    generation[-1].setLeft(generation[-2])
    for i in range(1, len(generation)-1):
        generation[i].setLeft(generation[i-1])
        generation[i].setRight(generation[i+1])

def runRules(generation, rules):
    results = []
    for pot in generation:
        for rule in rules:
            if pot.checkRule(rule):
                results.append(Pot(pot.num, rule.result))
                break
    return results



file = open("InputFiles/Day12.dat")
initialState = None
rules = []

for line in file:
    if not initialState:
        initialState = line.split()[2]
        file.readline()
    elif line:
        conditions = line.split(" => ")[0].strip()
        result = line.split(" => ")[1].strip()
        rules.append(Rule(conditions, result))

generations = []
# this was determined analytically
numGenerations = 96

firstGen = []
for i in range(len(initialState)):
    firstGen.append(Pot(i, initialState[i] == "#"))

connect(firstGen)
generations.append(firstGen)

for _ in range(numGenerations):
    previousGeneration = generations[-1]

    # add two empty pots to either end of the list, if necessary
    pots = []
    if previousGeneration[0].hasPlant:
        num = previousGeneration[0].num
        pots.append(Pot(num - 2, False))
        pots.append(Pot(num - 1, False))
    elif previousGeneration[1].hasPlant:
        num = previousGeneration[1].num
        pots.append(Pot(num - 2, False))

    for pot in previousGeneration:
        pots.append(Pot(pot.num, pot.hasPlant))

    if previousGeneration[-1].hasPlant:
        num = previousGeneration[-1].num
        pots.append(Pot(num + 1, False))
        pots.append(Pot(num + 2, False))
    elif previousGeneration[-2].hasPlant:
        num = previousGeneration[-2].num
        pots.append(Pot(num + 2, False))

    connect(pots)
    print(pots[0])
    newGeneration = runRules(pots, rules)

    generations.append(newGeneration)

connect(generations[-1])
print(generations[-1][0])
result = 0
plantCount = 0
for pot in generations[-1]:
    if pot.hasPlant:
        result += pot.num
        plantCount += 1

print(plantCount)
print(result)

print(result + (plantCount * (50000000000 - numGenerations)))