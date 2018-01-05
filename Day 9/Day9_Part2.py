file = open("InputFiles/Day9.dat")
text = file.readline()

numCharacters = 0
isGarbage = False

i = 0

while i < len(text):
    if text[i] == "!":
        i += 2
        continue
    elif text[i] == "<" and not isGarbage:
        isGarbage = True
    elif text[i] == ">":
        isGarbage = False
    elif isGarbage:
        numCharacters += 1
    i += 1

print(numCharacters)