import string

def spin(array, num):
    newArray = []
    i = len(array) - num
    while i < len(array):
        newArray.append(array[i])
        i += 1
    i = 0
    while i < (len(array) - num):
        newArray.append(array[i])
        i += 1
    array = newArray.copy()
    return array

def swapByPos(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp

def swapByContents(arr, a, b):
    swapByPos(arr, arr.index(a), arr.index(b))

def getInputs(command):
    if command.startswith("s"):
        return int(command[1:])
    elif command.startswith("x"):
        result = command[1:].split("/")
        result = [int(x) for x in result]
        return result
    else:
        result = command[1:].split("/")
        return result

letters = string.ascii_lowercase
array = []
for i in range(16):
    array.append(letters[i])

file = open("InputFiles/Day16.dat")
commands = file.readline().strip().split(",")

for command in commands:
    input = getInputs(command)
    if command.startswith("s"):
        array = spin(array, input)
    elif command.startswith("x"):
        swapByPos(array, input[0], input[1])
    else:
        swapByContents(array, input[0], input[1])

print("".join(array))