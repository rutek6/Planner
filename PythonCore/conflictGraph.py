from classes import *


def checkOverlap(group1: Group, group2: Group):
    for slot1 in group1.slotList:
        for slot2 in group2.slotList:
            if not slot1.day == slot2.day:
                continue
            if not slot1.week == slot2.week:
                continue
            if slot1.start >= slot2.start and slot1.start <= slot2.end:
                return True
            if slot1.end >= slot2.start and slot1.end <= slot2.end:
                return True
    return False

def checkNumberOfGroups(plan: Plan):
    i = 0
    for course in plan.courseList:
        for type in course.typeList:
            for group in type:
                i += 1
    return i

def extractGroups(plan: Plan):
    groups = []
    for course in plan.courseList:
        for type in course.typeList:
            for group in type:
                groups.append(group)

    return groups


# Creates a conflict graph
# Each column and row is defined by a unique group id
# Values: 0 - no conflict between specified groups,
# 1 - conflict,
# 2 - acceptable conflict, do not exclude in DFS 
#
def createConflictGraph(plan: Plan):
    numberOfGroups = checkNumberOfGroups(plan)
    conflictGraph = [[0]*numberOfGroups for _ in range(numberOfGroups)]
    acceptedTypes = ["CWW", "WYK"]
    groupList = extractGroups(plan)
    for group1 in groupList:
        for group2 in groupList:
            if group1 == group2:
                conflictGraph[group1.groupId][group1.groupId] = 1
                continue
            if group1.type in acceptedTypes or group2.type in acceptedTypes:
                conflictGraph[group1.groupId][group2.groupId] = 2
                continue
            if checkOverlap(group1, group2):
                conflictGraph[group1.groupId][group2.groupId] = 1
    return conflictGraph
            


