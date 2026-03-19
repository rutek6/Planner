from classes import *
def checkConflict(group: Group, compareList: list[Group]) -> bool:
    if len(compareList) == 0:
         return False
    for groupFromList in compareList:
        for compareSlot in groupFromList.slotList:
            for groupSlot in group.slotList:
                if(groupSlot.day == compareSlot.day and groupSlot.week == compareSlot.week):
                    if(groupSlot.start > compareSlot.start and groupSlot.start < compareSlot.end):
                        return True
                    if(groupSlot.end > compareSlot.start and groupSlot.end < compareSlot.end):
                            return True
    return False 


def DFS_Util(courseList: list[Course], nr, max, visited: list, combinedGroups: list):
    if(nr >= max):
            return
    for group in courseList[nr].groupList:
        if not checkConflict(group, visited):
            visited.append(group)
        else:
             continue
        
        if(len(visited) == max):
            combinedGroups.append(visited.copy())
        else:
            DFS_Util(courseList, nr+1, max, visited, combinedGroups)
        if len(visited) != 0:
             visited.pop()
        

def dfs(plan: Plan) -> list:
    nrOfCourses = plan.howMuchCourses()
    combinedGroups = []
    visited = []
    DFS_Util(plan.courseList, 0, nrOfCourses, visited, combinedGroups)
    return combinedGroups    


def optimize_plan(plan: Plan):
    scheduleList = dfs(plan)
