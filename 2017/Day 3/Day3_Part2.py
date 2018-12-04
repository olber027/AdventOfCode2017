def square(x):
    return x*x

def getCoordinates(targetNumber, startX, startY):
    sideLength = 1
    while square(sideLength) < targetNumber:
        sideLength += 2
    distanceFromCenter = int(sideLength/2)
    X = startX + distanceFromCenter
    Y = startY + distanceFromCenter - 1
    number = square(sideLength-2) + 1
    for i in range(sideLength - 2):
        if number >= targetNumber:
            break
        number += 1
        Y -= 1
    for i in range(sideLength - 1):
        if number >= targetNumber:
            break
        number += 1
        X -= 1
    for i in range(sideLength - 1):
        if number >= targetNumber:
            break
        number += 1
        Y += 1
    for i in range(sideLength - 1):
        if number >= targetNumber:
            break
        number += 1
        X += 1
    return (X, Y)

def sumOfNeighbors(array, X, Y):
    total = 0
    total += array[X+1][Y]
    total += array[X+1][Y-1]
    total += array[X][Y-1]
    total += array[X-1][Y-1]
    total += array[X-1][Y]
    total += array[X-1][Y+1]
    total += array[X][Y+1]
    total += array[X+1][Y+1]
    return total

array = []

for i in range(100):
    array.append([])
    for j in range(100):
        array[i].append(0)

array[50][50] = 1
(x,y) = (51, 50)
currentIndex = 2
targetNum = 361527
lastValue = -1

while lastValue < targetNum:
    (x,y) = getCoordinates(currentIndex, 50, 50)
    currentSum = sumOfNeighbors(array, x, y)
    array[x][y] = currentSum
    lastValue = currentSum
    currentIndex += 1

print("({0}, {1}) = {2}".format(x,y,lastValue))