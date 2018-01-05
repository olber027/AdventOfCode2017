class TuringMachine(object):
    def __init__(self):
        self.arr = [0]
        self.state = "A"
        self.index = 0

    def __repr__(self):
        result = ""
        if self.index < 0:
            result += "[0] "
        for i in range(len(self.arr)):
            if i != self.index:
                result += "{0} ".format(self.arr[i])
            else:
                result += "[{0}] ".format(self.arr[i])
        if self.index >= len(self.arr):
            result += "[0] "
        result += self.state
        return result

    def step(self):
        if self.index < 0:
            temp = [0]
            temp.extend(self.arr)
            self.arr = temp
            self.index = 0
        elif self.index >= len(self.arr):
            self.arr.append(0)

        if self.state == "A":
            if self.arr[self.index] == 0:
                self.arr[self.index] = 1
                self.index += 1
                self.state = "B"
            else:
                self.arr[self.index] = 0
                self.index -= 1
                self.state = "C"
        elif self.state == "B":
            if self.arr[self.index] == 0:
                self.arr[self.index] = 1
                self.index -= 1
                self.state = "A"
            else:
                self.index += 1
                self.state = "D"
        elif self.state == "C":
            if self.arr[self.index] == 0:
                self.index -= 1
                self.state = "B"
            else:
                self.arr[self.index] = 0
                self.index -= 1
                self.state = "E"
        elif self.state == "D":
            if self.arr[self.index] == 0:
                self.arr[self.index] = 1
                self.index += 1
                self.state = "A"
            else:
                self.arr[self.index] = 0
                self.index += 1
                self.state = "B"
        elif self.state == "E":
            if self.arr[self.index] == 0:
                self.arr[self.index] = 1
                self.index -= 1
                self.state = "F"
            else:
                self.index -= 1
                self.state = "C"
        elif self.state == "F":
            if self.arr[self.index] == 0:
                self.arr[self.index] = 1
                self.index += 1
                self.state = "D"
            else:
                self.index += 1
                self.state = "A"

    def getCheckSum(self):
        count = 0
        for x in self.arr:
            count += x
        return count

machine = TuringMachine()
for _ in range(12481997):
    machine.step()

print(machine.getCheckSum())

