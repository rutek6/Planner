import classes

am1 = classes.Group("ĆW", 1, "Moszyński")
slot1 = classes.TimeSlot(2, 60*12, 0)

am1.slots.append(slot1)

print(am1)