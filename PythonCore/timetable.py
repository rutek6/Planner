import sys
from classes import *
from parser import parseHTML
from plan import dfs
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, 
                               QDialog, 
                               QLineEdit, 
                               QPushButton, 
                               QVBoxLayout, 
                               QTableWidget, 
                               QTableWidgetItem,
                               QLabel,
                               QListWidget,
                               QListWidgetItem,
                               QWidget,
                               QHBoxLayout)
class TimetableEntry(QLabel):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""background-color: {color};
                            border-radius: 12px;
                            padding: 5px;
                            color: white;
                            font-size: 11px;""")
        self.setWordWrap(True)
        


class Schedule(QWidget):
    def __init__(self):
        super().__init__()
        self.topMargin = 10
        self.leftMargin = 60
        self.rightMargin = 60
        #self.dayWidth = 175
        self.dayWidth = 250
        self.verticalSpace = 50
        self.start = 7
        self.end = 20
        self.setStyleSheet("""
                           background-color: #761F21;
                           """)
        self.resize(1200, 800)
        self.days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]

        self.drawGrid()
        self.testEvents()
        

    def drawGrid(self):
        for i, day in enumerate(self.days):
            label = QLabel(day, self)
            label.move(self.leftMargin + i*self.dayWidth + 2*self.dayWidth/5 - 5, #TO-DO: FIX DAY NAME ALIGNMENT
                        self.topMargin)
            
            hLine = QLabel(self)
            hLine.setStyleSheet("""
                                background-color: #C4C4C4;
                                """)
            hLine.setGeometry(self.leftMargin + i*self.dayWidth,
                            self.topMargin,
                            1, 
                            (self.end - self.start)*self.verticalSpace)

        for i in range(self.start, self.end + 1):
            y = self.topMargin + 5 + (i-self.start+1)*self.verticalSpace

            hourLabel = QLabel(f"{i}:00", self)
            hourLabel.move(15, y) 

            vLine = QLabel(self)
            vLine.setStyleSheet("""
                                background-color: #C4C4C4;
                                """)
            vLine.setGeometry(self.leftMargin, y, len(self.days)*self.dayWidth, 1)

    def addEvent(self, day, start, end, text, color, overlap):
        x = self.leftMargin + self.dayWidth*day
        y = self.topMargin + 5 + (start - self.start + 1)*self.verticalSpace + 2
        width = self.dayWidth - 10
        if overlap == 1:
            width /= 2
        elif overlap == 2:
            width /= 2
            x += self.dayWidth/2
        height = (end-start)*self.verticalSpace - 2
        block = TimetableEntry(text, color, self)
        block.setGeometry(x, y, width, height)
        

    def testEvents(self):
        self.addEvent(0, 12, 13, "AM1", "#3E445C", 2)


        

if __name__ == "__main__":
    app = QApplication()
    schedule = Schedule()
    
    parsed = parseHTML()
    plan = dfs(parsed)

    firstPlan = plan[0]
    listOfGroups = []
    for group in firstPlan:
        for slot in group.slotList:
            name = group.course.name
            day = slot.day
            start = slot.start / 60
            end = slot.end / 60
            if group.type == "CW":
                color = "#3E445C"
            elif group.type == "WYK":
                color = "#7D9447"
            else:
                color = "#C805E2"
            listOfGroups.append([day, start, end, name, color])
    
    for item in listOfGroups:
        schedule.addEvent(item[0],item[1],item[2],item[3], item[4], True)
    schedule.show()
    sys.exit(app.exec())