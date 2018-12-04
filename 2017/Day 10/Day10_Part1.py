def getSubArray(array, start, end):
    subArray = []
    i = start
    while i != end:
        subArray.append(array[i])
        i = increment(array, i, 1)
    return subArray

def reverseElements(array, start, end):
    subArray = getSubArray(array, start, end)
    subArray.reverse()
    index = start
    subArrayIndex = 0
    while index != end:
        array[index] = subArray[subArrayIndex]
        index = increment(array, index, 1)
        subArrayIndex += 1

def increment(array, currentPosition, amount):
    length = len(array)
    newPosition = currentPosition + amount
    while newPosition >= length:
        newPosition -= length
    return newPosition


file = open("InputFiles/Day10.dat")
lengths = [int(x) for x in file.readline().split(",")]
array = [x for x in range(256)]
currentPosition = 0
skipSize = 0

for length in lengths:
    reverseElements(array, currentPosition, increment(array, currentPosition, length))
    currentPosition = increment(array, currentPosition, length + skipSize)
    skipSize += 1

print(array[0]*array[1])