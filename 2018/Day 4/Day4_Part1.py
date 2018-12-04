'''
As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.
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
guardSleepQuantities = {}

for record in records:
    if record.action == "begin":
        currentID = record.guardID
        if currentID not in guards.keys():
            guards[currentID] = []
            guardSleepQuantities[currentID] = 0
    elif record.action == "sleep":
        record.guardID = currentID
        currentTimeSpan[0] = record.minute
    else:
        record.guardID = currentID
        currentTimeSpan[1] = record.minute
        guards[currentID].append(tuple(currentTimeSpan))
        guardSleepQuantities[currentID] += currentTimeSpan[1] - currentTimeSpan[0]

sleepiestGuard = 0
timeSlept = 0

for (key, value) in guardSleepQuantities.items():
    if value > timeSlept:
        sleepiestGuard = key
        timeSlept = value

histogram = [0] * 60

for nap in guards[sleepiestGuard]:
    for i in range(nap[0], nap[1]):
        histogram[i] += 1

mostCommonMinute = max(histogram)
for i in range(60):
    if histogram[i] == mostCommonMinute:
        print(i*sleepiestGuard)
        exit()