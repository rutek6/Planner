from src.classes import *
from src.conflictGraph import *


def checkConflict(group: Group, compareList: list[Group], conflictGraph) -> bool:
    if len(compareList) == 0:
        return False
    for group2 in compareList:
        if conflictGraph[group.groupId][group2.groupId] == 1:
            return True
    return False


def DFS_Util(
    courseList: list[Course],
    nr,
    typeNr,
    max,
    visited: list,
    combinedGroups: list,
    conflictGraph,
):
    if len(visited) >= max:
        combinedGroups.append(visited.copy())
        return
    for group in courseList[nr].typeList[typeNr]:
        if not checkConflict(group, visited, conflictGraph):
            visited.append(group)
        else:
            continue
        if typeNr == len(courseList[nr].typeList) - 1:
            DFS_Util(courseList, nr + 1, 0, max, visited, combinedGroups, conflictGraph)
        else:
            DFS_Util(
                courseList, nr, typeNr + 1, max, visited, combinedGroups, conflictGraph
            )
        if len(visited) != 0:
            visited.pop()


def dfs(plan: Plan) -> list[list[Group]]:
    nrOfGroups = plan.howMuchGroups()
    combinedGroups = []
    visited = []
    conflictGraph = createConflictGraph(plan)
    DFS_Util(plan.courseList, 0, 0, nrOfGroups, visited, combinedGroups, conflictGraph)
    return combinedGroups
