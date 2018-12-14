'''
There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\
|   |
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\
|   |
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\
|   |
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/
After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?
'''

import math

class Cart(object):
    def __init__(self, x, y, vx, vy, track):
        self.velocity = [vx, vy]
        self.position = [x, y]
        self.intersection = "l"
        self.trackCharacter = track

    def __repr__(self):
        return "{} : {}".format(self.position, self.velocity)

    def __lt__(self, other):
        if self.position[1] < other.position[1]:
            return True
        elif self.position[1] > other.position[1]:
            return False
        if self.position[0] < other.position[0]:
            return True
        return False

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def getNextPosition(self):
        return (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def doIntersection(self):
        if self.intersection == "l":
            self.turnLeft()
            self.intersection = "s"
        elif self.intersection == "s":
            self.intersection = "r"
        elif self.intersection == "r":
            self.turnRight()
            self.intersection = "l"

    def turnLeft(self):
        theta = math.pi / -2.0
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = self.velocity[0]
        y = self.velocity[1]
        self.velocity[0] = int(x * cs - y * sn)
        self.velocity[1] = int(x * sn + y * cs)

    def turnRight(self):
        theta = math.pi / 2.0
        cs = math.cos(theta)
        sn = math.sin(theta)
        x = self.velocity[0]
        y = self.velocity[1]
        self.velocity[0] = int(x * cs - y * sn)
        self.velocity[1] = int(x * sn + y * cs)

def isCart(char):
    if char in "<>^v":
        return True
    return False

def findCart(carts, x, y):
    for cart in carts:
        if cart.position[0] == x and cart.position[1] == y:
            return cart
    return None

file = open("InputFiles/Day13.dat", "r")

tracks = []
carts = []
y = 0
for line in file:
    track = []
    for x in range(len(line)):
        if isCart(line[x]):
            vx = 0
            vy = 0
            if line[x] == "^":
                vy = -1
            elif line[x] == "v":
                vy = 1
            elif line[x] == "<":
                vx = -1
            else:
                vx = 1
            trackCharacter = "-" if line[x] in "<>" else "|"
            carts.append(Cart(x, y, vx, vy, trackCharacter))
            track.append(trackCharacter)
        else:
            track.append(line[x])

    tracks.append(track)
    y += 1

while len(carts) > 1:
    crashedCarts = set()
    carts.sort()
    for cart in carts:
        (x, y) = cart.getNextPosition()
        otherCart = findCart(carts, x ,y)
        if otherCart:
            crashedCarts.add(otherCart)
            crashedCarts.add(cart)
            # print((x,y))
            # exit()
        nextCharacter = tracks[y][x]
        if nextCharacter in "/":
            cart.update()
            if cart.velocity[0] != 0:
                cart.turnLeft()
            else:
                cart.turnRight()
        elif nextCharacter in "\\":
            cart.update()
            if cart.velocity[0] != 0:
                cart.turnRight()
            else:
                cart.turnLeft()
        elif nextCharacter in "|-":
            cart.update()
        elif nextCharacter in "+":
            cart.update()
            cart.doIntersection()

    for cart in crashedCarts:
        carts.remove(cart)

    if crashedCarts:
        print(len(carts))

print(carts[0].position)
print(carts[0].velocity)