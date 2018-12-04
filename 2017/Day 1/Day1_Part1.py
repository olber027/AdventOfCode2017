file = open("InputFiles/Day1.dat", "r")
str = file.read().strip()
sum = 0
for i in range(len(str)-2):
    if str[i] == str[i+1]:
        sum += int(str[i])

if str[len(str)-1] == str[0]:
    sum += int(str[len(str)-1])

print(sum)
