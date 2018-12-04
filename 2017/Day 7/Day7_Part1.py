class Node(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self.children = []
        self.parent = ""

    def addChildren(self, list):
        for child in list:
            self.children.append(child)

    def hasChild(self, childName):
        if childName in self.children:
            return True
        return False

    def addParent(self, parent):
        self.parent = parent

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return "{0} : {3} ({1}) -> {2}".format(self.name, self.weight, self.children, self.parent)

file = open("InputFiles/Day7.dat")
nodes = []

for line in file:
    parts = line.split("->")
    nodeInfo = parts[0].strip()
    children = []
    if len(parts) > 1:
        children = [x.strip() for x in parts[1].split(",")]
    node = Node(nodeInfo.split(" ")[0], nodeInfo.split(" ")[1].strip("()"))
    node.addChildren(children)
    nodes.append(node)

for node in nodes:
    children = node.getChildren()
    for childNode in children:
        index = nodes.index(childNode)
        nodes[index].addParent(node.name)

index = 0
parent = nodes[index].getParent()
while parent is not "":
    index = nodes.index(parent)
    parent = nodes[index].getParent()
print(nodes[index].name)