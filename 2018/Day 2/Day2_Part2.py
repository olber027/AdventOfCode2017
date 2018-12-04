'''
Confident that your list of box IDs is complete, you're ready to find the boxes full of prototype fabric.

The boxes will have IDs which differ by exactly one character at the same position in both strings. For example, given the following box IDs:

abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
The IDs abcde and axcye are close, but they differ by two characters (the second and fourth). However, the IDs fghij and fguij differ by exactly one character, the third (h and u). Those must be the correct boxes.

What letters are common between the two correct box IDs? (In the example above, this is found by removing the differing character from either ID, producing fgij.)
'''
from collections import deque

def getNumDifferences(first, second):
    differences = 0
    for i in range(len(first)):
        if first[i] != second[i]:
            differences += 1
            if differences > 1:
                return differences
    return differences


file = open("InputFiles/Day2.dat", "r")

IDs = deque()
for line in file:
    IDs.append(line)

for ID in IDs:
    for other in IDs:
        numDifferences = getNumDifferences(ID, other)
        if numDifferences == 1:
            print(ID)
            print(other)
            exit()

print("none found...")