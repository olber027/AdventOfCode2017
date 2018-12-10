'''
Amused by the speed of your answer, the Elves are curious:

What would the new winning Elf's score be if the number of the last marble were 100 times larger?
'''

class Node(object):
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def __repr__(self):
        return "{0} <- {1} -> {2}".format(self.left.value, self.value, self.right.value)

def initialSetup():
    zero = Node(0)
    one = Node(1, left=None, right=zero)
    zero.setLeft(one)
    two = Node(2, left=zero, right=one)
    zero.setRight(two)
    one.setLeft(two)
    return two

def addNumber(num, node):
    left = node.getRight()
    right = node.getRight().getRight()
    newNode = Node(num, left, right)
    left.setRight(newNode)
    right.setLeft(newNode)
    return newNode

def removeNode(nodeToRemove):
    '''
    :param nodeToRemove:
    :return: the node to the right of the one being removed
    '''
    nodeToReturn = nodeToRemove.getRight()
    nodeToRemove.getLeft().setRight(nodeToReturn)
    return nodeToReturn

file = open("InputFiles/Day9.dat", "r")
input = file.readline().split(" ")

numPlayers = int(input[0])
endingNumber = int(input[6]) * 100
currentNumber = 3
currentNode = None

playerScores = [0] * numPlayers

currentNode = initialSetup()

while currentNumber <= endingNumber:
    if currentNumber % 23 == 0:
        playerIndex = currentNumber % numPlayers
        playerScores[playerIndex] += currentNumber
        nodeToRemove = currentNode
        for _ in range(7):
            nodeToRemove = nodeToRemove.getLeft()
        playerScores[playerIndex] += nodeToRemove.value
        currentNode = removeNode(nodeToRemove)
    else:
        currentNode = addNumber(currentNumber, currentNode)

    currentNumber += 1

print(max(playerScores))