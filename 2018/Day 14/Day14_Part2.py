'''
As it turns out, you got the Elves' plan backwards. They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

51589 first appears after 9 recipes.
01245 first appears after 5 recipes.
92510 first appears after 18 recipes.
59414 first appears after 2018 recipes.
How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?
20220950
'''

def splitDigits(num):
    return [int(x) for x in list(str(num))]

def makeNewRecipes(firstScore, secondScore):
    newScore = firstScore + secondScore
    return splitDigits(newScore)

target = [int(x) for x in list(open("InputFiles/Day14.dat", "r").readline().strip())]
scoreboard = [3, 7]
first = 0
second = 1
targetIndex = 0

while targetIndex < len(target):
    newScores = makeNewRecipes(scoreboard[first], scoreboard[second])
    scoreboard.extend(newScores)
    first = (first + scoreboard[first] + 1) % len(scoreboard)
    second = (second + scoreboard[second] + 1) % len(scoreboard)
    newScoreIndex = 0
    while newScoreIndex < len(newScores):
        if newScores[newScoreIndex] == target[targetIndex]:
            targetIndex += 1
            if targetIndex >= len(target):
                break
        else:
            targetIndex = 0
            if newScores[newScoreIndex] == target[targetIndex]:
                targetIndex = 1
        newScoreIndex += 1

# not sure why the -1 needs to be there...
print(len(scoreboard) - len(target) - 1)