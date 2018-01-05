file = open("InputFiles/Day2.dat")
total = 0
for line in file:
    numbers = [int(x) for x in line.split("\t")]
    top = numbers[0]
    bottom = numbers[0]
    for num1 in numbers:
        for num2 in numbers:
            if num1 is not num2 and num1 % num2 == 0:
                top = num1 if num1 > num2 else num2
                bottom = num1 if num1 < num2 else num2
    total += (top/bottom)
print(total)