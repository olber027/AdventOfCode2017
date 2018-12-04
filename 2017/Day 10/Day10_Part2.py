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

def toHex(num):
    hexString = hex(num)
    result = ""
    if num < 16:
        result += "0"
        result += hexString[2]
    else:
        result += hexString[2]
        result += hexString[3]
    return result

file = open("InputFiles/Day10.dat")
line = file.readline().strip()
lengths = [ord(x) for x in line]
[lengths.append(x) for x in [17, 31, 73, 47, 23]]
array = [x for x in range(256)]
currentPosition = 0
skipSize = 0

for _ in range(64):
    for length in lengths:
        reverseElements(array, currentPosition, increment(array, currentPosition, length))
        currentPosition = increment(array, currentPosition, length + skipSize)
        skipSize += 1

denseHash = []
for i in range(16):
    val = array[i*16]
    for j in range(1,16):
        val = val ^ array[i*16 + j]
    denseHash.append(val)

result = ""
for hash in denseHash:
    result += toHex(hash)
print(result)

