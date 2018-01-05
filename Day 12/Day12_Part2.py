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

def getGroup(groupSoFar, pipe):
    groupSoFar.append(pipe)
    for connection in pipe.connections:
        if connection not in groupSoFar:
            groupSoFar.append(connection)
            getGroup(groupSoFar, connection)

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

groups = []
for pipe in pipes:
    alreadyCovered = False
    for group in groups:
        if pipe in group:
            alreadyCovered = True
            break
    if not alreadyCovered:
        group = []
        getGroup(group, pipe)
        groups.append(group)
print(len(groups))