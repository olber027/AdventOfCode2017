import math

class Particle(object):
    def __init__(self, id, accel, vel, pos):
        self.id = id
        self.acceleration = [x for x in accel]
        self.velocity = [x for x in vel]
        self.position = [x for x in pos]

    def __repr__(self):
        return "({0}) p->{1} v->{2} a->{3}".format(self.id, self.position, self.velocity, self.acceleration)

    def advance(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity[2] += self.acceleration[2]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]

    def distanceToOrigin(self):
        return sum([abs(x) for x in self.position])

    def magnitude(self, param):
        if param == "acceleration":
            return math.sqrt((self.acceleration[0]*self.acceleration[0] + self.acceleration[1]*self.acceleration[1] + self.acceleration[2]*self.acceleration[2]))
        elif param == "velocity":
            return math.sqrt((self.velocity[0]*self.velocity[0] + self.velocity[1]*self.velocity[1] + self.velocity[2]*self.velocity[2]))
        elif param == "position":
            return math.sqrt((self.position[0]*self.position[0] + self.position[1]*self.position[1] + self.position[2]*self.position[2]))

file = open("InputFiles/Day20.dat")

lines = [line.split(" ") for line in file.readlines()]
lines = [[l.strip("pva=<>, \n") for l in line] for line in lines]

particles = []
for line in lines:
    pos = [int(x) for x in line[0].split(",")]
    vel = [int(x) for x in line[1].split(",")]
    accel = [int(x) for x in line[2].split(",")]
    particles.append(Particle(len(particles), accel, vel, pos))

lowestMagnitude = math.inf
smallestEnergyParticles = []

for particle in particles:
    magnitude = particle.magnitude("acceleration")
    if magnitude < lowestMagnitude:
        smallestEnergyParticles = []
        smallestEnergyParticles.append(particle)
        lowestMagnitude = magnitude
    elif magnitude == lowestMagnitude:
        smallestEnergyParticles.append(particle)

result = None

for particle in smallestEnergyParticles:
    if result is None or particle.distanceToOrigin() < result.distanceToOrigin():
        result = particle

print(result)
