def square(x):
    return x*x

targetNum = 361527
sideLength = 1

while square(sideLength) <= targetNum:
    sideLength += 2

targetNum -= square(sideLength - 2)
corner = sideLength - 1
while targetNum > corner:
    corner += sideLength - 1
distanceToCorner = corner - targetNum
totalDistance = int(sideLength/2) + (int(sideLength/2) - distanceToCorner)

print(totalDistance)


