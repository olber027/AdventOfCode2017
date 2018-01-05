def increment(size, currentPosition, amount):
    newPosition = currentPosition + amount
    while newPosition >= size:
        newPosition -= size
    return newPosition

file = open("InputFiles/Day17.dat")
numSteps = int(file.readline().strip())

totalSize = 50000000
# totalSize = 2017

num = 0
currentPosition = 0
count = 1
currentSize = 1

for _ in range(totalSize):
    newPosition = increment(currentSize, currentPosition, numSteps)
    if newPosition == 0:
        num = count
        print(num)
    count += 1
    currentPosition = newPosition + 1
    currentSize += 1

print(num)