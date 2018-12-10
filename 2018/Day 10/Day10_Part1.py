'''
It's no use; your navigation system simply isn't capable of providing walking directions in the arctic circle, and certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue operations will arrange points of light in the sky to guide missing Elves back to base. Unfortunately, the message is easy to miss: the points move slowly enough that it takes hours to align them, but have so much momentum that they only stay aligned for a second. If you blink at the wrong time, it might be hours before another message appears.

You can see these points of light floating in the distance, and record their position in the sky and their velocity, the relative change in position per second (your puzzle input). The coordinates are all given from your perspective; given enough time, those positions and velocities will move the points into a cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
Each line represents one point. Positions are given as <X, Y> pairs: X represents how far left (negative) or right (positive) the point appears, while Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. If this point's initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................
After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer and will take many more seconds to appear.

What message will eventually appear in the sky?
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

def translate(bounds, coords):
    return (coords[0] + bounds[0][0], coords[1] + bounds[0][1])

def plot(bounds, particles):
    array = []
    for i in range(bounds[1][1] - bounds[0][1] + 1):
        array.append([])
        for j in range(bounds[1][0] - bounds[0][0] + 1):
            array[i].append(" ")

    for particle in particles:
        coords = translate(bounds, particle.position)
        array[coords[1]][coords[0]] = "*"

    [print("".join(x)) for x in array]


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
while sign < 0:
    [particle.update() for particle in particles]
    bounds = getBounds(particles)
    newArea = (bounds[1][0] - bounds[0][0]) * (bounds[1][1] - bounds[0][1])
    sign = newArea - area
    area = newArea

[particle.backup() for particle in particles]

plot(getBounds(particles), particles)