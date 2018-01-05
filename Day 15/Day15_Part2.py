class Generator(object):
    def __init__(self, seed, factor, criteria):
        self.factor = factor
        self.currentNumber = seed
        self.criteria = criteria

    def nextNumber(self):
        temp = (self.currentNumber * self.factor) % 2147483647
        while temp % self.criteria != 0:
            temp = (temp * self.factor) % 2147483647
        self.currentNumber = temp
        return self.currentNumber


file = open("InputFiles/Day15.dat")
A = Generator(int(file.readline().split(" ")[4]), 16807, 4)
B = Generator(int(file.readline().split(" ")[4]), 48271, 8)

count = 0

for _ in range(5000000):
    Astring = bin(A.nextNumber())[2:].zfill(16)
    Bstring = bin(B.nextNumber())[2:].zfill(16)
    Aindex = len(Astring) - 1
    Bindex = len(Bstring) - 1
    isSame = True
    for i in range(16):
        if Astring[Aindex] != Bstring[Bindex]:
            isSame = False
            break
        Aindex -= 1
        Bindex -= 1
    if isSame:
        count += 1

print(count)