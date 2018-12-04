class KnotHash(object):
    def __init__(self, seed):
        self.seed = seed
        self.knotHash = ""

    def toHex(self, num):
        return hex(num)[2:].zfill(2)

    def increment(self, array, currentPosition, amount):
        length = len(array)
        newPosition = currentPosition + amount
        while newPosition >= length:
            newPosition -= length
        return newPosition

    def getSubArray(self, array, start, end):
        subArray = []
        i = start
        while i != end:
            subArray.append(array[i])
            i = self.increment(array, i, 1)
        return subArray

    def reverseElements(self, array, start, end):
        subArray = self.getSubArray(array, start, end)
        subArray.reverse()
        index = start
        subArrayIndex = 0
        while index != end:
            array[index] = subArray[subArrayIndex]
            index = self.increment(array, index, 1)
            subArrayIndex += 1

    def calculateHash(self):
        lengths = [ord(x) for x in self.seed]
        [lengths.append(x) for x in [17, 31, 73, 47, 23]]
        array = [x for x in range(256)]
        currentPosition = 0
        skipSize = 0

        for _ in range(64):
            for length in lengths:
                self.reverseElements(array, currentPosition, self.increment(array, currentPosition, length))
                currentPosition = self.increment(array, currentPosition, length + skipSize)
                skipSize += 1

        denseHash = []
        for i in range(16):
            val = array[i*16]
            for j in range(1,16):
                val = val ^ array[i*16 + j]
            denseHash.append(val)

        for subHash in denseHash:
            self.knotHash += self.toHex(subHash)

def inBounds(array, x, y):
    if x < 0 or y < 0:
        return False
    if x >= len(array) or y >= len(array[0]):
        return False
    return True

def markRegion(grid, i, j, regionNumber):
    if not inBounds(grid, i, j) or grid[i][j] != "1":
        return False
    grid[i][j] = str(regionNumber)
    markRegion(grid, i+1, j, regionNumber)
    markRegion(grid, i, j+1, regionNumber)
    markRegion(grid, i-1, j, regionNumber)
    markRegion(grid, i, j-1, regionNumber)
    return True


file = open("InputFiles/Day14.dat")
baseSeed = file.readline().strip()

grid = []
for i in range(128):
    rowSeed = baseSeed + "-{0}".format(i)
    rowHash = KnotHash(rowSeed)
    rowHash.calculateHash()
    binaryString = []
    for letter in rowHash.knotHash:
        [binaryString.append(x) for x in bin(int(letter, 16))[2:].zfill(4)]
    grid.append(binaryString)

regionNumber = 2

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if markRegion(grid, i, j, regionNumber):
            regionNumber += 1

print(regionNumber - 2)
