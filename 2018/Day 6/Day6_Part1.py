'''
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
'''
import copy

def abs(num):
    if num < 0:
        return num*-1;
    return num

def getEdgeIDs(grid):
    IDs = set()
    for x in range(len(grid)):
        IDs.add(grid[x][0])
        IDs.add(grid[x][-1])
    for y in range(len(grid[0])):
        IDs.add(grid[0][y])
        IDs.add(grid[-1][y])
    return IDs

def getClosestCoordinates(coordinates, target):
    distances = {}
    for (id, (x, y)) in coordinates.items():
        distances[id] = abs(target[0] - x) + abs(target[1] - y)
    IDs = sorted(distances, key=distances.__getitem__)
    smallestIDs = [IDs[0]]
    i = 1
    while distances[IDs[i]] == distances[IDs[0]]:
        smallestIDs.append(IDs[i])
        i += 1
    return smallestIDs

def createGrid(width, height, init):
    result = []
    [result.append([]) for x in range(width)]
    [[x.append(init) for y in range(height)] for x in result]
    return result

file = open("InputFiles/Day6.dat", "r")

coordinates = {}
maxX = 0
maxY = 0
ID = 0

for line in file:
    coords = (int(line.split(",")[0].strip()), int(line.split(",")[1].strip()))
    coordinates[ID] = coords
    if coords[0] > maxX:
        maxX = coords[0]
    if coords[1] > maxY:
        maxY = coords[1]
    ID += 1

grid = createGrid(maxX + 1, maxY + 1, ".")
for (id, (x, y)) in coordinates.items():
    grid[x][y] = id

markedGrid = copy.deepcopy(grid)
counts = {}

for x in range(maxX + 1):
    for y in range(maxY + 1):
        closest = getClosestCoordinates(coordinates, (x,y))
        if len(closest) == 1:
            markedGrid[x][y] = closest[0]
            if closest[0] not in counts.keys():
                counts[closest[0]] = 0
            counts[closest[0]] += 1

edges = getEdgeIDs(markedGrid)

IDs = [id for id in sorted(counts, key=counts.__getitem__, reverse=True) if id not in edges]
print(IDs[0])
print(counts[IDs[0]])


# for y in range(maxY + 1):
#     line = ""
#     for x in range(maxX + 1):
#         line += str(markedGrid[x][y])
#     print(line)
#
# print("{}x{}".format(len(grid), len(grid[0])))
# print(edges)