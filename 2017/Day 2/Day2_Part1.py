file = open("InputFiles/Day2.dat")
total = 0
for line in file:
    numbers = [int(x) for x in line.split("\t")]
    maxNum = numbers[0]
    minNum = numbers[0]
    for num in numbers:
        if num > maxNum:
            maxNum = num
        if num < minNum:
            minNum = num
    total += maxNum - minNum
print(total)