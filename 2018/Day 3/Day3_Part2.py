'''
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
'''
class Rectangle(object):
    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.topRight = (topLeft[0] + width - 1, topLeft[1])
        self.bottomLeft = (topLeft[0], topLeft[1] + height - 1)
        self.bottomRight = (self.topRight[0], self.bottomLeft[1])

    def __repr__(self):
        return "{0}, {1}, {2}, {3}".format(self.topLeft, self.topRight, self.bottomLeft, self.bottomRight)


class Claim(object):
    def __init__(self, rawDataString):
        self.ID = int(rawDataString.split("@")[0].strip().strip("#"))
        topLeft = rawDataString.split("@")[1].split(":")[0].strip().split(",")
        area = rawDataString.split("@")[1].split(":")[1].strip().split("x")
        self.rect = Rectangle((int(topLeft[0]), int(topLeft[1])), int(area[0]), int(area[1]))

    def __repr__(self):
        return "{0} : {1}".format(self.ID, self.rect)

    def __eq__(self, other):
        return self.ID == other.ID

    def __ne__(self, other):
        return self.ID != other.ID

    def overlaps(self, grid):
        for i in range(self.rect.topLeft[0], self.rect.topRight[0] + 1):
            for j in range(self.rect.topLeft[1], self.rect.bottomRight[1] + 1):
                if len(grid[i][j]) > 1:
                    return True
        return False


file = open("InputFiles/Day3.dat", "r")

claims = []
grid = []
maxX = 0
maxY = 0

for line in file:
    claim = Claim(line)
    claims.append(claim)
    if claim.rect.bottomRight[0] > maxX:
        maxX = claim.rect.bottomRight[0]
    if claim.rect.bottomRight[1] > maxY:
        maxY = claim.rect.bottomRight[1]

[grid.append([]) for col in range(maxX + 1)]
[[col.append([]) for row in range(maxY + 1)] for col in grid]

for claim in claims:
    for i in range(claim.rect.topLeft[0], claim.rect.topRight[0] + 1):
        for j in range(claim.rect.topLeft[1], claim.rect.bottomRight[1] + 1):
            grid[i][j].append(claim.ID)

for claim in claims:
    if not claim.overlaps(grid):
        print(claim.ID)
        exit()