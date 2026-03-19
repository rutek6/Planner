from classes import *
def checkConflict(group: Group, compareList: list[Group]) -> bool:
    if len(compareList) == 0:
         return False
    for groupFromList in compareList:
        for compareSlot in groupFromList.slotList:
            for groupSlot in group.slotList:
                if(groupSlot.day == compareSlot.day and groupSlot.week == compareSlot.week):
                    if(groupSlot.start >= compareSlot.start and groupSlot.start <= compareSlot.end):
                        return True
                    if(groupSlot.end >= compareSlot.start and groupSlot.end <= compareSlot.end):
                            return True
    return False 


def DFS_Util(courseList: list[Course], nr, typeNr, max, visited: list, combinedGroups: list):
    print(f"{nr} - {typeNr} \n")
    if(nr >= max):
            return
    for group in courseList[nr].typeList[typeNr]:
        if not checkConflict(group, visited):
            visited.append(group)
        else:
             continue
        
        if(len(visited) == max):
            combinedGroups.append(visited.copy())
        else:
            if typeNr == len(courseList[nr].typeList) - 1:
                DFS_Util(courseList, nr+1, 0, max, visited, combinedGroups)
            else:
                DFS_Util(courseList, nr, typeNr + 1, max, visited, combinedGroups)
        if len(visited) != 0:
             visited.pop()
        

def dfs(plan: Plan) -> list:
    nrOfGroups = plan.howMuchGroups()
    combinedGroups = []
    visited = []
    print(nrOfGroups)
    DFS_Util(plan.courseList, 0, 0, nrOfGroups, visited, combinedGroups)
    return combinedGroups    


