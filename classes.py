class TimeSlot:
    def __init__(self, day, time, week):
        self.day = day
        self.time = time
        self.week = week
    def __repr__(self):
        return f"{(int)(self.time / 60)}:{self.time % 60}, day: {self.day}"

class Group:
    def __init__(self, type, number, person):
        self.slotList = []
        self.type = type
        self.number = number
        self.person = person

    def __str__(self):
        return f"{self.type}-{self.number}, {self.person}: {self.slots}"

class Course:
    def __init__(self, name):
        self.name = name
        self.groupList = []

class Plan:
    def __init__(self):
        self.courseList =  []

        
    