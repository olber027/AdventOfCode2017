import math

def rotate(coordinates, angle):
    angle = math.radians(angle)
    temp = []
    temp.append(coordinates[0]*math.cos(angle) - coordinates[1]*math.sin(angle))
    temp.append(coordinates[1]*math.cos(angle) + coordinates[0]*math.sin(angle))
    coordinates[0] = round(temp[0])
    coordinates[1] = round(temp[1])

def expandGrid(grid, coords):
    quarterSize = int(len(grid)/2)
    newSize = int(len(grid) + 2*quarterSize)
    newGrid = [[] for x in range(newSize)]
    newCoordsSet = False
    index = 0
    for i in range(quarterSize):
        newGrid[i].extend("."*newSize)
        index += 1
    for i in range(len(grid)):
        newGrid[i+quarterSize].extend("."*quarterSize)
        for j in range(len(grid)):
            if i == coords[0] and j == coords[1] and not newCoordsSet:
                coords[0] = i+quarterSize
                coords[1] = len(newGrid[i+quarterSize])
                newCoordsSet = True
            newGrid[i+quarterSize].append(grid[i][j])
        newGrid[i+quarterSize].extend("."*quarterSize)
        index += 1
    for i in range(quarterSize):
        newGrid[index].extend("."*newSize)
        index += 1
    return newGrid

def inBounds(x,y, array):
    if x < 0 or y < 0:
        return False
    if x >= len(array) or y >= len(array[0]):
        return False
    return True

file = open("InputFiles/Day22.dat")

lines = [line.strip() for line in file.readlines()]
grid = [list(line) for line in lines]

middle = int((len(grid) - 1)/2)

direction = [0,-1]
coordinates = [middle, middle]

iterations = 0
numIterations = 10000
infectionCount = 0

while iterations < numIterations:
    x = coordinates[0]
    y = coordinates[1]
    if grid[x][y] == "#":
        rotate(direction, 90)
        grid[x][y] = "."
    else:
        rotate(direction, -90)
        grid[x][y] = "#"
        infectionCount += 1
    if not inBounds(x+direction[1],y+direction[0], grid):
        grid = expandGrid(grid, coordinates)
    coordinates[0] += direction[1]
    coordinates[1] += direction[0]
    iterations += 1

print(infectionCount)
