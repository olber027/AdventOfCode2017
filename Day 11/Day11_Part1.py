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

directions = ["ne", "se","ne", "se","ne", "se","ne", "se","ne", "se","ne", "se","ne", "se","ne", "se", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne", "ne"]

vec = Vector(0, 0)

for direction in directions:
    angle = convert(direction)
    vec.x += math.cos(math.radians(angle))
    vec.y += math.sin(math.radians(angle))

sideLength = math.fabs(vec.x/math.sqrt(3))
longestSide = sideLength*2
total = longestSide + (math.fabs(vec.y) - sideLength)

print(max(round(total), round(longestSide)))
