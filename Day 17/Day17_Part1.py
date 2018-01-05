class Node:
    def __init__(self, value, next):
        self.value = value
        self.next = next

    def insert(self, value):
        node = Node(value, self.next)
        self.next = node

    def getNext(self):
        return self.next

    def __repr__(self):
        return "{0}".format(self.value)

file = open("InputFiles/Day17.dat")
numSteps = int(file.readline().strip())

head = Node(0, None)
currentNode = head
count = 1

for _ in range(2017):
    for i in range(numSteps):
        if currentNode.getNext() is None:
            currentNode = head
        else:
            currentNode = currentNode.getNext()
    currentNode.insert(count)
    currentNode = currentNode.getNext()
    count += 1

print(currentNode.getNext())