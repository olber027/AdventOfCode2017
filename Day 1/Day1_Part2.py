file = open("InputFiles/Day1.dat", "r")
str = file.read().strip()
sum = 0

gap = len(str) / 2

for i in range(len(str)-1):
    comp = int(i + gap)
    if comp >= len(str):
        comp -= len(str)
    if str[i] == str[comp]:
        sum += int(str[i])
print(sum)