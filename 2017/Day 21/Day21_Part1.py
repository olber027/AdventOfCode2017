import math

def rotate(arr):
    if len(arr) == 2:
        temp = arr[0][1]
        arr[0][1] = arr[0][0]
        temp2 = arr[1][1]
        arr[1][1] = temp
        temp = arr[1][0]
        arr[1][0] = temp2
        arr[0][0] = temp
    elif len(arr) == 3:
        temp = arr[0][2]
        arr[0][2] = arr[0][0]
        temp2 = arr[2][2]
        arr[2][2] = temp
        temp = arr[2][0]
        arr[2][0] = temp2
        arr[0][0] = temp

        temp = arr[1][2]
        arr[1][2] = arr[0][1]
        temp2 = arr[2][1]
        arr[2][1] = temp
        temp = arr[1][0]
        arr[1][0] = temp2
        arr[0][1] = temp

def flipHorizontal(arr):
    if len(arr) == 2:
        temp = arr[0][0]
        arr[0][0] = arr[0][1]
        arr[0][1] = temp
        temp = arr[1][0]
        arr[1][0] = arr[1][1]
        arr[1][1] = temp
    else:
        temp = arr[0][0]
        arr[0][0] = arr[0][2]
        arr[0][2] = temp
        temp = arr[1][0]
        arr[1][0] = arr[1][2]
        arr[1][2] = temp
        temp = arr[2][0]
        arr[2][0] = arr[2][2]
        arr[2][2] = temp

def flipVertical(arr):
    if len(arr) == 2:
        temp = arr[0][0]
        arr[0][0] = arr[1][0]
        arr[1][0] = temp
        temp = arr[0][1]
        arr[0][1] = arr[1][1]
        arr[1][1] = temp
    else:
        temp = arr[0][0]
        arr[0][0] = arr[2][0]
        arr[2][0] = temp
        temp = arr[0][1]
        arr[0][1] = arr[2][1]
        arr[2][1] = temp
        temp = arr[0][2]
        arr[0][2] = arr[2][2]
        arr[2][2] = temp

def subdivide(array, squareSize):
    result = []
    numSquares = int(len(array)/squareSize)
    for i in range(numSquares):
        result.append([])
        for j in range(numSquares):
            square = [["_" for x in range(squareSize)] for y in range(squareSize)]
            for k in range(squareSize):
                for l in range(squareSize):
                    square[k][l] = array[i*squareSize + k][j*squareSize + l]
            result[i].append(square)
    return result

class Pattern(object):
    def __init__(self, matchingPattern, resultingPattern):
        self.matchingPattern = []
        numLines = 0
        for line in matchingPattern.split("/"):
            self.matchingPattern.append([])
            for character in line:
                self.matchingPattern[numLines].append(character)
            numLines += 1
        self.resultingPattern = []
        numLines = 0
        for line in resultingPattern.split("/"):
            self.resultingPattern.append([])
            for character in line:
                self.resultingPattern[numLines].append(character)
            numLines += 1

    def __repr__(self):
        return "{0} => {1}".format(self.matchingPattern, self.resultingPattern)

    def matches(self, match):
        if len(match) != len(self.matchingPattern):
            return False
        temp = match.copy()
        count = 0
        while count < 4:
            normal = temp == self.matchingPattern
            flipHorizontal(temp)
            flipH = temp == self.matchingPattern
            flipHorizontal(temp)
            flipVertical(temp)
            flipV = temp == self.matchingPattern
            flipVertical(temp)
            if normal or flipH or flipV:
                return True
            else:
                count += 1
                rotate(temp)
        return False

    def getPattern(self):
        return self.resultingPattern


file = open("InputFiles/Day21.dat")
lines = [line.strip() for line in file.readlines()]

patterns = []

for line in lines:
    splitLine = line.split(" => ")
    patterns.append(Pattern(splitLine[0].strip(), splitLine[1].strip()))

picture = [[".", "#", "."],[".", ".", "#"],["#", "#", "#"]]

iterations = 0

while iterations < 18:
    print("iteration: {0}".format(iterations))
    [print("".join(line)) for line in picture]
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    length = len(picture)
    squares = []
    if length % 2 == 0:
        squares = subdivide(picture, 2)
    else:
        squares = subdivide(picture, 3)

    newSquares = [["X" for x in range(len(squares))] for y in range(len(squares))]
    matchedPatterns = []
    for i in range(len(squares)):
        for j in range(len(squares)):
            print("square {0} of {1}".format(i*len(squares) + j, len(squares)*len(squares)))
            square = squares[i][j]
            for pattern in patterns:
                if pattern.matches(square):
                    newSquares[i][j] = pattern.getPattern().copy()
                    matchedPatterns.append(pattern.matchingPattern.copy())
                    break

    squaresPerSide = len(newSquares)
    squareLength = len(newSquares[0][0])
    newPicture = [["_" for i in range(int(squaresPerSide*squareLength))] for j in range(int(squaresPerSide*squareLength))]

    for i in range(len(newSquares)):
        for j in range(len(newSquares[0])):
            square = newSquares[i][j]
            for k in range(len(square)):
                for l in range(len(square[0])):
                    newPicture[i*squareLength + k][j*squareLength + l] = square[k][l]

    picture = newPicture
    iterations += 1

count = 0
for i in range(len(picture)):
    for j in range(len(picture[0])):
        if picture[i][j] == "#":
            count += 1

print(count)