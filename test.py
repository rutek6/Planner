import classes
from plan import dfs

am = classes.Course("AM")
akso = classes.Course("AKSO")
fiz = classes.Course("FIZ")


am1 = classes.Group("ĆW", 1, "Moszyński", am)
am2 = classes.Group("ĆW", 2, "Skw", am)
am3 = classes.Group("ĆW", 3, "Gór", am)

am1slot = classes.TimeSlot(1, 12*60, 13*60+30, 0)
akso1slot = classes.TimeSlot(1, 12*60+15, 13*60+45, 0)

akso1 = classes.Group("ĆW", 1, "Zaroda", akso)
akso2 = classes.Group("ĆW", 2, "ZNowak", akso)
akso3 = classes.Group("ĆW", 3, "Goldstein", akso)

fiz1 = classes.Group("ĆW", 1, "Turzyn", fiz)
fiz2 = classes.Group("ĆW", 2, "Twardoch", fiz)
fiz3 = classes.Group("ĆW", 3, "Ktoś", fiz)

akso1.slotList.append(akso1slot)
am1.slotList.append(am1slot)

am.groupList.append(am1)
am.groupList.append(am2)
am.groupList.append(am3)

akso.groupList.append(akso1)
akso.groupList.append(akso2)
akso.groupList.append(akso3)

fiz.groupList.append(fiz1)
fiz.groupList.append(fiz2)
fiz.groupList.append(fiz3)


plan = classes.Plan()
plan.courseList.append(fiz)
plan.courseList.append(akso)
plan.courseList.append(am)

list = dfs(plan)


print(list)