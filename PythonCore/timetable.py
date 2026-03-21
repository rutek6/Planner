import sys
from classes import *
from parser import parseHTML
from conflictGraph import checkOverlap
from optimizer import evaluatePlan
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
        self.setStyleSheet(f"""QLabel{{ background-color: {color};
                            border-radius: 12px;
                            padding: 5px;
                            color: #EAEAEA;
                            font-size: 11px;}}
                            QLabel::hover{{
                            border: 1px solid black;
                            }}"""
                            )
        self.setWordWrap(True)
        self.setToolTip(f"{text}")
    
    


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
                           background-color: #2A2A2A;
                           """)
        self.resize(1350, 800)
        self.days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        self.drawGrid()

    def drawGrid(self):
        for i, day in enumerate(self.days):
            label = QLabel(day, self)
            label.move(self.leftMargin + i*self.dayWidth + 2*self.dayWidth/5 - 5, #TO-DO: FIX DAY NAME ALIGNMENT
                        self.topMargin)
            
            vLine = QLabel(self)
            vLine.setStyleSheet("""
                                background-color: #C4C4C4;
                                """)
            vLine.setGeometry(self.leftMargin + i*self.dayWidth,
                            self.topMargin,
                            1, 
                            (self.end - self.start + 2)*self.verticalSpace)

        for i in range(self.start, self.end + 1):
            y = self.topMargin + 5 + (i-self.start+1)*self.verticalSpace

            hourLabel = QLabel(f"{i}:00", self)
            hourLabel.move(15, y) 

            hLine = QLabel(self)
            hLine.setStyleSheet("""
                                background-color: #C4C4C4;
                                """)
            hLine.setGeometry(self.leftMargin, y, len(self.days)*self.dayWidth, 1)

    def addEvent(self, day, start, end, text, color, overlap):
        x = self.leftMargin + self.dayWidth*day + 5
        y = self.topMargin + 5 + (start - self.start + 1)*self.verticalSpace + 2
        width = self.dayWidth - 10
        if overlap == 1:
            width /= 2
        elif overlap == 2:
            width /= 2
            x += self.dayWidth/2 - 2.5
        height = (end-start)*self.verticalSpace - 2
        block = TimetableEntry(text, color, self)
        block.setGeometry(x, y, width, height)
        
def prepareForAdding(firstPlan):
    listOfGroups = []
    for group in firstPlan:
        for slot in group.slotList:
            
            day = slot.day
            start = slot.start / 60
            end = slot.end / 60
            name = f"""{group.course.name} \n {group.giveKey()} \n {(slot.start // 60)}:{slot.start % 60:02d} - {(slot.end // 60)}:{slot.end % 60:02d}"""
            if group.type == "CW":
                color = "#E05555"
            elif group.type == "WYK":
                color = "#6F6F6F"
            else:
                color = "#99582A"
            overlap = 0
            for compareSlot in listOfGroups:
                if not day == compareSlot[0]:
                    continue
                if start >= compareSlot[1] and start <= compareSlot[2]:
                    compareSlot[5] = 1
                    overlap = 2
                if end >= compareSlot[1] and end <= compareSlot[2]:
                    compareSlot[5] = 1
                    overlap = 2
            listOfGroups.append([day, start, end, name, color, overlap])
    return listOfGroups        


if __name__ == "__main__":
    app = QApplication()
    schedule = Schedule()
    
    parsed = parseHTML()
    plan = dfs(parsed)
    plan.sort(reverse=False, key=evaluatePlan)
    firstPlan = plan[10]
    listOfGroups = prepareForAdding(firstPlan)
    for item in listOfGroups:
        schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])
    schedule.show()
    sys.exit(app.exec())