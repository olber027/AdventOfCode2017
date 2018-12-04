class Node(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self.children = []
        self.parent = None

    def addChildren(self, list):
        for child in list:
            self.children.append(child)

    def addParent(self, parent):
        self.parent = parent

    def getChildren(self):
        return self.children

    def getUnbalancedChild(self):
        childWeights = []
        for child in self.children:
            childWeights.append(child.getTotalWeight())
        differentWeights = set(childWeights)
        if len(differentWeights) <= 1:
            return None
        for weight in differentWeights:
            if childWeights.count(weight) == 1:
                for child in self.children:
                    if child.getTotalWeight() == weight:
                        return child
        return None

    def getTotalWeight(self):
        total = self.weight
        for child in self.children:
            total += child.getTotalWeight()
        return total

    def getParent(self):
        return self.parent

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return "{0} ({1}) -> {2}".format(self.name, self.weight, self.children)

file = open("InputFiles/Day7.dat")
lines = file.read().splitlines()
nodes = []

for line in lines:
    parts = line.split("->")
    nodeInfo = parts[0].strip()
    node = Node(nodeInfo.split(" ")[0], nodeInfo.split(" ")[1].strip("()"))
    nodes.append(node)

for line in lines:
    parts = line.split("->")
    node = nodes[nodes.index(parts[0].strip().split(" ")[0])]
    childNames = []
    children = []
    if len(parts) > 1:
        childNames = [x.strip() for x in parts[1].split(",")]
    for child in childNames:
        childIndex = nodes.index(child)
        children.append(nodes[childIndex])
        nodes[childIndex].addParent(node)
    node.addChildren(children)

rootNode = nodes[0]
while rootNode.getParent() is not None:
    rootNode = rootNode.getParent()

unbalancedNode = rootNode.getUnbalancedChild()
while unbalancedNode.getUnbalancedChild() is not None:
    unbalancedNode = unbalancedNode.getUnbalancedChild()

print(unbalancedNode.weight)

