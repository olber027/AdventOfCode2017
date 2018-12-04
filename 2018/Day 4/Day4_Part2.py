'''
Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)
'''

class Record(object):
    def __init__(self, recordString):
        self.year = int(recordString.split("-")[0].strip("["))
        self.month = int(recordString.split("-")[1])
        self.day = int(recordString.split("-")[2].split(" ")[0])
        self.hour = int(recordString.split(":")[0].split(" ")[1])
        self.minute = int(recordString.split(":")[1].split("]")[0])
        self.guardID = -1

        self.action = None
        if "begins" in recordString:
            self.action = "begin"
        elif "falls asleep" in recordString:
            self.action = "sleep"
        elif "wakes up" in recordString:
            self.action = "wake"

        if self.action == "begin":
            self.guardID = int(recordString.split("#")[1].split(" ")[0])

    def __repr__(self):
        return "{}-{}-{} {}:{} | #{} | {}".format(self.year, self.month, self.day, self.hour, self.minute, self.guardID, self.action)

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False

        if self.month < other.month:
            return True
        elif self.month > other.month:
            return False

        if self.day < other.day:
            return True
        elif self.day > other.day:
            return False

        if self.hour < other.hour:
            return True
        elif self.hour > other.hour:
            return False

        if self.minute < other.minute:
            return True
        elif self.minute > other.minute:
            return False

        if self.action < other.action:
            return False
        elif self.action > other.action:
            return True

        return False

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month \
               and self.day == other.day and self.minute == other.minute \
               and self.guardID == other.guardID and self.action == other.action


file = open("InputFiles/Day4.dat", "r")

records = []

for line in file:
    records.append(Record(line))

records.sort()
currentID = -1
currentTimeSpan = [0, 0]
guards = {}
guardSleepPatterns = {}

for record in records:
    if record.action == "begin":
        currentID = record.guardID
        if currentID not in guards.keys():
            guards[currentID] = []
            guardSleepPatterns[currentID] = [0] * 60
    elif record.action == "sleep":
        record.guardID = currentID
        currentTimeSpan[0] = record.minute
    else:
        record.guardID = currentID
        currentTimeSpan[1] = record.minute
        guards[currentID].append(tuple(currentTimeSpan))
        for i in range(currentTimeSpan[0], currentTimeSpan[1]):
            guardSleepPatterns[currentID][i] += 1

sleepiestGuard = 0
mostSleptMinute = 0

for (key, value) in guardSleepPatterns.items():
    if max(value) > mostSleptMinute:
        sleepiestGuard = key
        mostSleptMinute = max(value)

for minute in range(60):
    if guardSleepPatterns[sleepiestGuard][minute] == mostSleptMinute:
        print(sleepiestGuard * minute)
        exit()