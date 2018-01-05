def increment(index, array):
    if index + 1 < len(array):
        return index + 1
    return 0

def nextConfig(array):

    newArray = array.copy()
    index = newArray.index(max(newArray))
    numBlocks = array[index]
    newArray[index] = 0

    index = increment(index, newArray)
    while numBlocks > 0:
        newArray[index] += 1
        numBlocks -= 1
        index = increment(index, newArray)

    return newArray


file = open("InputFiles/Day6.dat")
banks = [int(x) for x in file.readline().split("\t")]
seenConfigs = [banks]
next = nextConfig(banks)

while next not in seenConfigs:
    seenConfigs.append(next)
    next = nextConfig(next)

firstIndex = seenConfigs.index(next)
print(len(seenConfigs) - firstIndex)