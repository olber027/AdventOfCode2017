'''
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
'''

class Step(object):
    def __init__(self, id):
        self.nextSteps = []
        self.prereqs = []
        self.id = id

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

    def update(self, requirementMet):
        if requirementMet in self.prereqs:
            self.prereqs.remove(requirementMet)

    def numPrereqs(self):
        return len(self.prereqs)

file = open("InputFiles/Day7.dat", "r")

steps = {}

for line in file:
    first = line.split("must be finished before step")[0].split(" ")[1].strip()
    second = line.split("must be finished before step")[1].split(" ")[1].strip()

    if first not in steps.keys():
        steps[first] = Step(first)
    steps[first].addNextStep(second)

    if second not in steps.keys():
        steps[second] = Step(second)
    steps[second].addPrereq(first)

stepList = ""
for i in range(len(steps)):
    availableSteps = [step for step in steps.values() if step.numPrereqs() == 0]
    availableSteps.sort()
    currentStep = availableSteps[0]
    stepList += currentStep.id
    [steps[stepID].update(currentStep.id) for stepID in steps.keys()]
    del steps[currentStep.id]

print(stepList)


