class Generator(object):
    def __init__(self, seed, factor):
        self.factor = factor
        self.currentNumber = seed

    def nextNumber(self):
        self.currentNumber = (self.currentNumber * self.factor)  % 2147483647
        return self.currentNumber


file = open("InputFiles/Day15.dat")
A = Generator(int(file.readline().split(" ")[4]), 16807)
B = Generator(int(file.readline().split(" ")[4]), 48271)

count = 0

for _ in range(40000000):
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