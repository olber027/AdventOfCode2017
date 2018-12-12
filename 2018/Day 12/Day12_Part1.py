'''
The year 518 is significantly more underground than your history books implied. Either that, or you've arrived in a vast cavern network under the North Pole.

After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right. A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots. Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation. These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.
It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3
       0         0         0         0
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.
The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right. Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34. Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?
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
numGenerations = 20

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

result = 0
for pot in generations[-1]:
    if pot.hasPlant:
        result += pot.num

print(result)



