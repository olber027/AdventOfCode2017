# import string
# import queue as q
#
# class Register(object):
#     def __init__(self, name, value=0):
#         self.name = name
#         self.value = value
#     def __eq__(self, other):
#         return self.name == other
#     def __repr__(self):
#         return "{0} - {1}".format(self.name, self.value)
#
#     def set(self, other):
#         self.value = other
#     def add(self, other):
#         self.value += other
#     def mult(self, other):
#         self.value *= other
#     def mod(self, other):
#         self.value = (self.value % other)
#
# def doAction(action, register, value):
#     increment = 1
#     if action == "set":
#         register.set(value)
#     elif action == "add":
#         register.add(value)
#     elif action == "mul":
#         register.mult(value)
#     elif action == "mod":
#         register.mod(value)
#     elif action == "jgz":
#         if type(register) is not int:
#             if register.value != 0:
#                 increment = value
#         else:
#             if register != 0:
#                 increment = value
#     return increment
#
# def parseLine(line, registers, pid):
#     parts = line.split(" ")
#     action = parts[0]
#     registerName = parts[1]
#     value = None
#     if action == "snd":
#         if registerName in registers:
#             value = registers[registers.index(registerName)].value
#         else:
#             value = int(registerName)
#         if pid == "0":
#             q1.put(value)
#         else:
#             sendCount.put(value)
#             q0.put(value)
#         return 1
#     elif action == "rcv":
#         if pid == "0":
#             if q0.qsize() != 0:
#                 value = q0.get()
#         else:
#             if q1.qsize() != 0:
#                 value = q1.get()
#         if value is not None:
#             registers[registers.index(registerName)].set(value)
#             return 1
#         else:
#             return 0
#     if len(parts) > 2:
#         value = parts[2]
#     register = None
#     if registerName in registers:
#         register = registers[registers.index(registerName)]
#     else:
#         register = int(registerName)
#     if value is not None:
#         if value in registers:
#             value = registers[registers.index(value)].value
#         else:
#             value = int(value)
#     return doAction(action, register, value)
#
#
# registers0 = []
# registers1 = []
#
# q0 = q.Queue()
# q1 = q.Queue()
# sendCount = q.Queue()
#
# file = open("InputFiles/Day18.dat")
# lines = [line.strip() for line in file.readlines()]
# for line in lines:
#     name = line.split(" ")[1]
#     if name not in registers0 and name[0] in string.ascii_lowercase:
#         if name == "p":
#             registers0.append(Register(name, 0))
#             registers1.append(Register(name, 1))
#         else:
#             registers0.append(Register(name))
#             registers1.append(Register(name))
#
# index0 = 0
# index1 = 0
#
# count = 0
# iterations = 0
# deadlock = False
#
# while index0 >= 0 and index0 < len(lines) and index1 >= 0 and index1 < len(lines) and iterations < 5000:
#     newindex0 = parseLine(lines[index0], registers0, "0")
#     newindex1 = parseLine(lines[index1], registers1, "1")
#
#     print("({2}) {0} || ({3}) {1}".format(lines[index0], lines[index1], index0+1, index1+1))
#     for i in range(len(registers0)):
#         print("{0} || {1}".format(registers0[i], registers1[i]))
#     print("   ({0}) || ({1})".format(q0.qsize(), q1.qsize()))
#     print("----------------------")
#
#     if not sendCount.empty():
#         sendCount.get()
#         count += 1
#     if newindex0 == 0 and newindex1 == 0:
#         deadlock = True
#         break
#     index0 += newindex0
#     index1 += newindex1
#     iterations += 1
#
# if deadlock:
#     print("deadlock!")
# print(count)
# print(index0)
# print(index1)
# print(iterations)

from collections import defaultdict

f=open("InputFiles/Day18.dat")
instr = [line.split() for line in f.read().strip().split("\n")]
f.close()

d1 = defaultdict(int) # registers for the programs
d2 = defaultdict(int)
d2['p'] = 1
ds = [d1,d2]

def get(s):
    if s in "qwertyuiopasdfghjklzxcvbnm":
        return d[s]
    return int(s)

tot = 0

ind = [0,0]         # instruction indices for both programs
snd = [[],[]]       # queues of sent data (snd[0] = data that program 0 has sent)
state = ["ok","ok"] # "ok", "r" for receiving, or "done"
pr = 0     # current program
d = ds[pr] # current program's registers
i = ind[0] # current program's instruction index
while True:
    if instr[i][0]=="snd": # send
        if pr==1: # count how many times program 1 sends
            tot+=1
        snd[pr].append(get(instr[i][1]))
    elif instr[i][0]=="set":
        d[instr[i][1]] = get(instr[i][2])
    elif instr[i][0]=="add":
        d[instr[i][1]] += get(instr[i][2])
    elif instr[i][0]=="mul":
        d[instr[i][1]] *= get(instr[i][2])
    elif instr[i][0]=="mod":
        d[instr[i][1]] %= get(instr[i][2])
    elif instr[i][0]=="rcv":
        if snd[1-pr]: # other program has sent data
            state[pr] = "ok"
            d[instr[i][1]] = snd[1-pr].pop(0) # get data
        else: # wait: switch to other prog
            if state[1-pr]=="done":
                break # will never recv: deadlock
            if len(snd[pr])==0 and state[1-pr]=="r":
                break # this one hasn't sent anything, other is recving: deadlock
            ind[pr] = i   # save instruction index
            state[pr]="r" # save state
            pr = 1 - pr   # change program
            i = ind[pr]-1 # (will be incremented back)
            d = ds[pr]    # change registers
    elif instr[i][0]=="jgz":
        if get(instr[i][1]) > 0:
            i+=get(instr[i][2])-1
    i+=1
    if not 0<=i<len(instr):
        if state[1-pr] == "done":
            break # both done
        state[pr] = "done"
        ind[pr] = i  # swap back since other program's not done
        pr = 1-pr
        i = ind[pr]
        d = ds[pr]

print(tot)