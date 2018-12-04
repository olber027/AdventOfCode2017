def isAnagram(word1, word2):
    if len(word1) != len(word2):
        return False
    for i in range(len(word1)):
        word2 = word2.replace(word1[i], "")
    if len(word2) > 0:
        return False
    return True

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
            if (i is not j) and isAnagram(words[i], words[j]):
                valid = False
                break
    if valid:
        validPhraseCount += 1

print(validPhraseCount)
