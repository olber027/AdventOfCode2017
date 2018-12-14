'''
A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/
After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/
In this example, the location of the first crash is 7,3.
'''
import math
import os

class Cart(object):
    def __init__(self, x, y, vx, vy, track):
        self.velocity = [vx, vy]
        self.position = [x, y]
        self.intersection = "l"
        self.trackCharacter = track

    def __repr__(self):
        if self.velocity[1] == -1:
            return "^"
        elif self.velocity[1] == 1:
            return "v"
        elif self.velocity[0] == -1:
            return "<"
        else:
            return ">"

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

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

file = open("InputFiles/test.dat", "r")

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

while True:
    for cart in carts:
        prevX = cart.position[0]
        prevY = cart.position[1]
        prevTrackCharacter = cart.trackCharacter
        cart.update()
        x = cart.position[0]
        y = cart.position[1]
        nextCharacter = tracks[y][x]
        if nextCharacter in "/":
            if cart.velocity[0] != 0:
                cart.turnLeft()
            else:
                cart.turnRight()
        elif nextCharacter in "\\":
            if cart.velocity[0] != 0:
                cart.turnRight()
            else:
                cart.turnLeft()
        elif nextCharacter in "|-":
            pass
        elif nextCharacter in "+":
            cart.doIntersection()
        elif isCart(nextCharacter):
            tracks[y][x] = "X"
            print("a crash occured at: ({}, {})".format(x,y))
            exit()
        tracks[prevY][prevX] = prevTrackCharacter
        cart.trackCharacter = tracks[y][x]
        tracks[y][x] = str(cart)
    [print("".join(x).rstrip()) for x in tracks]