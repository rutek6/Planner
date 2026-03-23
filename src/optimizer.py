from src.classes import *
from src.preferences import Preferences

def getSlotList(plan: Plan):
    slots = []
    for group in plan:
        for slot in group.slotList:
            slots.append(slot)
    return slots

def countConflicts(slots):
    counter = 0
    for slot1 in slots:
        for slot2 in slots:
            if not slot1.day == slot2.day:
                continue
            if slot1 is slot2:
                continue
            if slot1.start <= slot2.end and slot1.start >= slot2.start:
                counter += 1
                continue
            if slot1.end <= slot2.end and slot1.end >= slot2.start:
                counter += 1
                continue
    return counter            

def countGapLength(slots):
    slotsByDay = {d: [] for d in range(5)}
    for slot in slots:
        slotsByDay[slot.day].append(slot)
    for i in range(5):
        slotsByDay[i].sort(key=lambda x: x.start)
    
    gapCount = 0
    for i in range(5):
        for j, slot in enumerate(slotsByDay[i]):
            if j == 0:
                continue
            add = slot.start - slotsByDay[i][j-1].end
            if add > 0:
                gapCount += add
    return gapCount

#Returns False if slots don't fill the preferences
def checkPrefferedHours(slots, preferences):
    for slot in slots:
        if slot.start < preferences.preferredHours[slot.day][0]:
            return False
        if slot.end > preferences.preferredHours[slot.day][1]:
            return False
    return True

def checkRequiredGroups(plan: Plan, preferences: Preferences):
    print("MIAU")
    for course in plan.courseList:
        for type in course.typeList:
            
            if not type:
                continue
            typeInPrefs = False
            for group in preferences.requiredGroupList:
                if group.course is course and group.type == type[0].type:
                    typeInPrefs = True
            if typeInPrefs:
                requiredInPlan = False
                for group1 in type:
                    for group2 in preferences.requiredGroupList:
                        if group1 is group2:
                            requiredInPlan = True
            else:
                continue

            if requiredInPlan:
                continue
            else:
                return False
    return True



def evaluatePlan(plan: list[Group]):
    slots = getSlotList(plan) #list[TimeSlot]
    conflictNr = countConflicts(slots)
    gapLength = countGapLength(slots)
    return conflictNr*150 + gapLength

def optimize(planList: list[Plan], preferences = Preferences()):
    if not preferences:
        preferences = Preferences()

    for plan in planList:
        slots = getSlotList(plan) #list[TimeSlot]
        if not checkPrefferedHours(slots, preferences):
            planList.remove(plan)
            continue
        if not checkRequiredGroups(plan, preferences):
            planList.remove(plan)
            continue

    planList.sort(key=evaluatePlan)
    return planList