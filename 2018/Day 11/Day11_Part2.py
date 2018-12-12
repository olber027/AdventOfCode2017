'''
You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.
What is the X,Y,size identifier of the square with the largest total power?
'''

def getHundredsDigit(num):
    if num < 100:
        return 0
    return int(str(num)[-3])

def calculatePower(x, y, serial):
    rackID = x + 10
    powerLevel = rackID * y
    powerLevel += serial
    powerLevel = powerLevel * rackID
    return getHundredsDigit(powerLevel) - 5

def calculateCellSum(x, y, grid, size):
    sum = 0
    for i in range(size):
        for j in range(size):
           sum += grid[y + i][x + j]
    return sum

file = open("InputFiles/Day11.dat", "r")
serialNumber = int(file.readline().strip())
gridSize = 300

grid = [[0] * gridSize for _ in range(gridSize)]

for i in range(gridSize):
    for j in range(gridSize):
        grid[i][j] = calculatePower(j+1, i+1, serialNumber)

#      val, x, y, n
max = (-10, 0, 0, 0)
for i in range(gridSize):
    for j in range(gridSize):
        print("({}, {})".format(j, i))
        x = j + 1
        y = i + 1
        tempGrid = [line.copy() for line in grid]
        tempMax = (grid[i][j], j, i, 1)
        while x < gridSize and y < gridSize:
            for m in range(j, x):
                tempGrid[y][x] += grid[y][m]
            for n in range(i, y):
                tempGrid[y][x] += grid[n][x]
            tempGrid[y][x] += tempGrid[y-1][x-1]
            if tempGrid[y][x] > tempMax[0]:
                tempMax = (tempGrid[y][x], j+1, i+1, (x - j + 1))
            x += 1
            y += 1
        if tempMax[0] > max[0]:
            max = tempMax
print(max)