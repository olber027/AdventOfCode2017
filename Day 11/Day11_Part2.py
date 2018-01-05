import math

def convert(direction):
    if direction == "s":
        return 270
    elif direction == "n":
        return 90
    elif direction == "ne":
        return 30
    elif direction == "nw":
        return 150
    elif direction == "sw":
        return 210
    else:
        return 330

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)
    def magnitude(self):
        return math.sqrt((self.x*self.x) + (self.y*self.y))

file = open("InputFiles/Day11.dat")
directions = file.readline().split(",")

vec = Vector(0, 0)
farthestVec = Vector(1,1)

for direction in directions:
    angle = convert(direction)
    vec.x += math.cos(math.radians(angle))
    vec.y += math.sin(math.radians(angle))
    if vec.magnitude() > farthestVec.magnitude():
        farthestVec.x = vec.x
        farthestVec.y = vec.y

sideLength = math.fabs(farthestVec.x/math.sqrt(3))
longestSide = sideLength*2
total = longestSide + (math.fabs(farthestVec.y) - sideLength)

print(max(round(total), round(longestSide)))
