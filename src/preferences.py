from src.classes import *


class Preferences:
    def __init__(self):
        # List of tuples: [dayNr](startHour: float, endHour: float)
        self.preferredHours: list[tuple] = [(8, 18)] * 5
        self.requiredGroupList = []
        self.requiredFreeDays = []


pref = Preferences()
