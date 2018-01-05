file = open("InputFiles/Day9.dat")
text = file.readline()

score = 0
nesting = 0
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
    elif text[i] == "{" and not isGarbage:
        nesting += 1
    elif text[i] == "}" and not isGarbage:
        score += nesting
        nesting -= 1
    i += 1

print(score)
