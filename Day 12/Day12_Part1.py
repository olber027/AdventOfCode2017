class Pipe(object):
    def __init__(self, id):
        self.id = id
        self.connections = []

    def addConnection(self, connection):
        self.connections.append(connection)

    def __eq__(self, other):
        return self.id == other
    def __lt__(self, other):
        return self.id < other.id
    def __repr__(self):
        return "{0} <-> {1}".format(self.id, [x.id for x in self.connections])

def getNumConnections(connectionsSoFar, pipe):
    connectionsSoFar.append(pipe)
    numConnections = 0
    for connection in pipe.connections:
        if connection not in connectionsSoFar:
            numConnections += 1
            connectionsSoFar.append(connection)
            numConnections += getNumConnections(connectionsSoFar, connection)
    return numConnections

file = open("InputFiles/Day12.dat")
lines = file.readlines()
lines = [x.strip() for x in lines]
pipes = []

for line in lines:
    id = line.split("<->")[0].strip()
    pipes.append(Pipe(int(id)))

for line in lines:
    id = line.split("<->")[0].strip()
    pipe = pipes[pipes.index(int(id))]
    connections = line.split("<->")[1].strip().split(", ")
    connections = [int(x) for x in connections]
    for connection in connections:
        pipe.addConnection(pipes[pipes.index(connection)])

pipe0 = pipes[pipes.index(0)]
connections = []

print(getNumConnections(connections, pipe0) + 1)
