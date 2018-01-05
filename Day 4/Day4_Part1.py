file = open("InputFiles/Day4.dat")

validPhraseCount = 0
words = []
count = 0

for line in file:
    count += 1
    words = line.split()
    valid = True
    for i in range(len(words)):
        for j in range(len(words)):
            if i is not j and words[i] == words[j]:
                valid = False
                break
    if valid:
        validPhraseCount += 1

print(validPhraseCount)
