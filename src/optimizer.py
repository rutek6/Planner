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
        if slot.start < preferences.preferredHours[slot.day][0]*60:
            return False
        if slot.end > preferences.preferredHours[slot.day][1]*60:
            return False
        
    return True

def checkRequiredGroups(plan: list[Group], preferences: Preferences):
    prefDict = {} #course.name: (dict[type]: list[Group])
    for group in preferences.requiredGroupList:
        if group.course.name not in prefDict.keys():
            prefDict[group.course.name] = {}
        if group.type not in prefDict[group.course.name].keys():
            prefDict[group.course.name][group.type] = []
        prefDict[group.course.name][group.type].append(group)

    for _, typeDict in prefDict.items():
        for _, groupList in typeDict.items():
            if not groupList:
                continue
            else:
                isPlanCorrect = False
                for group in groupList:
                    if group in plan:
                        isPlanCorrect = True
                        break
                if not isPlanCorrect:
                    return False
    return True





def evaluatePlan(plan: list[Group]):
    slots = getSlotList(plan) #list[TimeSlot]
    conflictNr = countConflicts(slots)
    gapLength = countGapLength(slots)
    return conflictNr*150 + gapLength

def optimize(planList: list[list[Group]], preferences = Preferences()):
    toRemove = []
    
    for plan in planList:
        slots = getSlotList(plan) #list[TimeSlot]
        if checkPrefferedHours(slots, preferences) is False:
            toRemove.append(plan)
            continue
        if checkRequiredGroups(plan, preferences) is False:
            toRemove.append(plan)
            continue
    
    for plan in toRemove:
        planList.remove(plan)
        
    
    planList.sort(key=evaluatePlan)
    return planList