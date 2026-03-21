from classes import *

class weights:
    def __init__(self, start):
        self.start = start

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

def evaluatePlan(plan: list[Group]):
    slots = getSlotList(plan) #list[TimeSlot]
    conflictNr = countConflicts(slots)
    gapLength = countGapLength(slots)
    # print(f"Conflicts: {conflictNr}")
    # print(f"Gap Length: {gapLength}")
    return conflictNr*150 + gapLength