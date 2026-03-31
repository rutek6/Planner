# @day: 1-5 (Mon - Fri)
# @start, @end: h*60 + min
# @week: 0 - all, 1 - odd, 2 - even


class TimeSlot:
    def __init__(self, day, start, end, week):
        self.day = day
        self.start = start
        self.end = end
        self.week = week

    def __repr__(self):
        return f"{(int)(self.start / 60)}:{self.start % 60} - {(int)(self.end / 60)}:{self.end % 60}, day: {self.day}"

    def giveTime(self):
        return f"{(int)(self.start / 60)}:{self.start % 60} - {(int)(self.end / 60)}"


class Group:
    def __init__(self, type, number, person, course, groupId):
        self.slotList = []
        self.type = type
        self.number = number
        self.person = person
        self.course = course
        self.groupId = groupId

    def __str__(self):
        return f"{self.type}-{self.number}, {self.person}: {self.slotList}"

    def __repr__(self):
        return f"{self.course.name}: {self.type}-{self.number}, {self.person} \n"

    def giveKey(self):
        return f"{self.type}-{self.number}"


class Course:
    def __init__(self, name):
        self.name = name
        self.typeList = []  # list[list[Group]]


class Plan:
    def __init__(self):
        self.courseList = []

    def __str__(self):
        s = ""
        for course in self.courseList:
            s = s + f"\n{course.name}"
            for type in course.typeList:
                for group in type:
                    s = s + f"\n{group.type} - {group.number}   ID: {group.groupId}"
        return s

    def howMuchGroups(self):
        i = 0
        for course in self.courseList:
            i = i + len(course.typeList)
        return i
