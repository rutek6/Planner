import classes
from plan import dfs
from parser import parseHTML
from optimizer import evaluatePlan

plan = parseHTML()
list = dfs(plan)
list.sort(reverse=True, key=evaluatePlan)

i = 0
for plan in list:
    for day in range(5):
        print(f"\nDAY: {day}")
        for group in plan:
            for slot in group.slotList:
                if slot.day == day:
                    print(f"{group.course.name} - {group.giveKey()} : {slot.giveTime()}")
    i = i+1
    if i == 1:
        break

# evaluatePlan(list[0])

