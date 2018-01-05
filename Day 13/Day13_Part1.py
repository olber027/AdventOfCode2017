class Layer(object):
    def __init__(self, depth, range):
        self.depth = depth
        self.range = range
        if range > 0:
            self.currentPosition = 0
            self.direction = 1
        else:
            self.currentPosition = -1
            self.direction = 0
        self.hasStarted = False

    def __repr__(self):
        return "{0}: {1} [{2}]".format(self.depth, self.range, self.currentPosition)

    def advance(self):
        if not self.hasStarted:
            self.currentPosition += self.direction
            self.hasStarted = True
            return
        if self.currentPosition == 0 or self.currentPosition == (self.range - 1):
            self.direction *= -1
        self.currentPosition += self.direction

    def getScannerPosition(self):
        return self.currentPosition

class FireWall(object):
    def __init__(self):
        self.layers = []

    def addLayer(self, layer):
        self.layers.append(layer)

    def elapseTime(self, numSeconds):
        count = 0
        while count < numSeconds:
            for layer in self.layers:
                layer.advance()
            count += 1

    def isScannerAt(self, position):
        if self.layers[position].getScannerPosition() == 0:
            return True
        return False

    def getSeverityFor(self, position):
        layer = self.layers[position]
        return layer.depth*layer.range

    def reset(self):
        for i in range(len(self.layers)):
            self.layers[i] = Layer(self.layers[i].depth, self.layers[i].range)

file = open("InputFiles/Day13.dat")
lines = [x.strip() for x in file.readlines()]
pairs = [(int(x.split(": ")[0]), int(x.split(": ")[1])) for x in lines]

firewall = FireWall()

pairIndex = 0
numLayers = 0

while pairIndex < len(pairs):
    pair = pairs[pairIndex]
    if pair[0] == numLayers:
        firewall.addLayer(Layer(pair[0], pair[1]))
        pairIndex += 1
    else:
        firewall.addLayer(Layer(numLayers, 0))
    numLayers += 1

severity = 0
position = -1

while position < numLayers-1:
    position += 1
    if firewall.isScannerAt(position):
        severity += firewall.getSeverityFor(position)
    firewall.elapseTime(1)

print(severity)

for layer in firewall.layers:
    print(layer)

firewall.reset()

for layer in firewall.layers:
    print(layer)