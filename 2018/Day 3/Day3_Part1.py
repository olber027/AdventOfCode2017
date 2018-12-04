'''
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
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

count = 0
for i in range(maxX + 1):
    for j in range(maxY + 1):
        if len(grid[i][j]) > 1:
            count += 1

print(count)