'''
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
'''

def abs(num):
    if num < 0:
        return num*-1
    return num

def getTotalDistance(coordinates, target):
    distance = 0
    for (x, y) in coordinates.values():
        distance += abs(target[0] - x) + abs(target[1] - y)

    return distance

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

area = 0

for x in range(maxX + 1):
    for y in range(maxY + 1):
        distance = getTotalDistance(coordinates, (x,y))
        if distance < 10000:
            area += 1

print(area)