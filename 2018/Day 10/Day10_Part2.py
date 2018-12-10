'''
Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?
'''

import string

class Particle(object):
    def __init__(self, pos, vel):
        self.position = pos
        self.velocity = vel

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def backup(self):
        self.position[0] -= self.velocity[0]
        self.position[1] -= self.velocity[1]

    def __repr__(self):
        return "{} : {}".format(self.position, self.velocity)

def getBounds(list):
    topLeft = [0,0]
    bottomRight = [0,0]
    for item in list:
        if item.position[0] < topLeft[0]:
            topLeft[0] = item.position[0]
        if item.position[0] > bottomRight[0]:
            bottomRight[0] = item.position[0]
        if item.position[1] < topLeft[1]:
            topLeft[1] = item.position[1]
        if item.position[1] > bottomRight[1]:
            bottomRight[1] = item.position[1]
    return [topLeft, bottomRight]

file = open("Inputfiles/Day10.dat", "r")

particles = []

for line in file:
    xPos = int(line.split(",")[0].strip(string.ascii_letters + "=<"))
    yPos = int(line.split(",")[1].split(">")[0].strip())
    xVel = int(line.split(",")[1].split("<")[1].strip())
    yVel = int(line.split(",")[2].strip().strip(">"))
    particles.append(Particle([xPos, yPos], (xVel, yVel)))

area = 10000000000000000000000000000000000000000000000000000
sign = -1
time = 0
while sign < 0:
    [particle.update() for particle in particles]
    time += 1
    bounds = getBounds(particles)
    newArea = (bounds[1][0] - bounds[0][0]) * (bounds[1][1] - bounds[0][1])
    sign = newArea - area
    area = newArea

[particle.backup() for particle in particles]

print(time - 1)