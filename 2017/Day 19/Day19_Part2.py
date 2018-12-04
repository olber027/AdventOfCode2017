import string

def inBounds(pos, map):
    if pos[0] < 0 or pos[1] < 0:
        return False
    if pos[1] >= len(map) or pos[0] >= len(map[0]):
        return False
    return True

def increment(currentDirection, pos):
    if currentDirection == "S":
        pos[1] += 1
    elif currentDirection == "N":
        pos[1] -= 1
    elif currentDirection == "E":
        pos[0] += 1
    else:
        pos[0] -= 1

def changeDirection(map, pos, current):
    temp = pos.copy()
    if current == "S" or current == "N":
        temp[0] += 1
        if inBounds(temp, map) and map[temp[1]][temp[0]] != " ":
            return "E"
        else:
            return "W"
    else:
        temp[1] += 1
        if inBounds(temp, map) and map[temp[1]][temp[0]] != " ":
            return "S"
        else:
            return "N"

file = open("InputFiles/Day19.dat")
map = [[x for x in line.strip("\n")] for line in file.readlines()]

# make each row the same length
maxLength = max([len(row) for row in map])
for row in map:
    while len(row) < maxLength:
        row.append(" ")

# find the index of the starting point
pos = [0, 0]
for i in range(len(map[0])):
    if map[0][i] == "|":
        pos[0] = i
        break

steps = 1
currentDirection = "S"
increment(currentDirection, pos)

while inBounds(pos, map) and map[pos[1]][pos[0]] != " ":
    currentCharacter = map[pos[1]][pos[0]]
    if currentCharacter == "+":
        currentDirection = changeDirection(map, pos, currentDirection)
    steps+=1
    increment(currentDirection, pos)

print(steps)