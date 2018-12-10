'''
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
'''

def letterToSeconds(letter):
    return ord(letter) - ord("A") + 1

class Step(object):
    def __init__(self, id):
        self.nextSteps = []
        self.prereqs = []
        self.id = id
        self.stepLength = letterToSeconds(id) + 60
        self.timeSpent = 0
        self.isDone = False

    def __repr__(self):
        return "{0} -> {1} -> {2}".format(self.prereqs, self.id, self.nextSteps)

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        if isinstance(other, Step):
            return self.id == other.id
        else:
            return self.id == other

    def addPrereq(self, prereq):
        self.prereqs.append(prereq)

    def addNextStep(self, next):
        self.nextSteps.append(next)

    def updatePrereq(self, requirementMet):
        if requirementMet in self.prereqs:
            self.prereqs.remove(requirementMet)

    def numPrereqs(self):
        return len(self.prereqs)

    def doWork(self, timeSpent):
        self.timeSpent += timeSpent
        if self.timeSpent >= self.stepLength:
            self.isDone = True

    def inProgress(self):
        return self.timeSpent > 0 and self.timeSpent < self.stepLength

    def done(self):
        return self.isDone

class Worker(object):
    def __init__(self):
        self.working = False
        self.step = None

    def startWork(self, step):
        self.step = step
        self.working = True
        return self.doWork()

    def doWork(self):
        self.step.doWork(1)
        if self.step.done():
            self.working = False
            self.step = None
            return self.step.id
        return ""

    def isWorking(self):
        return self.working

file = open("InputFiles/Day7.dat", "r")

steps = {}
workers = []
for _ in range(5):
    workers.append(Worker())

for line in file:
    first = line.split("must be finished before step")[0].split(" ")[1].strip()
    second = line.split("must be finished before step")[1].split(" ")[1].strip()

    if first not in steps.keys():
        steps[first] = Step(first)
    steps[first].addNextStep(second)

    if second not in steps.keys():
        steps[second] = Step(second)
    steps[second].addPrereq(first)


time = 0
completedSteps = ""
while len(steps) > 0:
    working = [worker for worker in workers if worker.isWorking()]
    needsWork = [worker for worker in workers if not worker.isWorking()]

    availableSteps = [step for step in steps.values() if step.numPrereqs() == 0 and not step.inProgress()]
    availableSteps.sort()

    completedStepList = ""
    for worker in working:
        completedStepList += worker.doWork()

    for worker in needsWork:
        if len(availableSteps) > 0:
            completedStepList += worker.startWork(availableSteps.pop(0))

    for id in completedStepList:
        [steps[stepID].updatePrereq(id) for stepID in steps.keys()]
        del steps[id]

    time += 1

print(time)
