def traverseList(list):
    index = 0
    count = 0
    while index >= 0 and index < len(list):
        nextIndex = index + list[index]
        list[index] += 1
        count += 1
        index = nextIndex
    return count

list = []
file = open("InputFiles/Day5.dat")

for line in file:
    list.append(int(line.strip()))

stepCount = traverseList(list)

print(stepCount)