from classes import *

am1 = Group(1, "Moszyński")
slot1 = TimeSlot(2, 60*12, 0)

am1.slots.append(slot1)

print(am1)