import sys
from classes import *
from timetable import Schedule, prepareForAdding
from parser import parseHTML
from conflictGraph import checkOverlap
from optimizer import evaluatePlan
from plan import dfs
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, 
                               QPushButton, 
                               QWidget,
                               QHBoxLayout,
                               QLabel,
                               QFormLayout,
                               QGridLayout,
                               QSizePolicy,
                               QMainWindow,
                               QFileDialog)

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.path = ""
        self.planNr = 1
        self.button = QPushButton("Otwórz HTML")
        self.button2 = QPushButton("Prev")
        self.button3 = QPushButton("Next")
        self.planLabel = QLabel(str(self.planNr))
        self.button.setFixedWidth(150)
        self.button2.setFixedWidth(150)
        self.button3.setFixedWidth(150)
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.planLabel)
        
        self.setLayout(layout)

    
    
class Footer(QWidget):
    def __init__(self):
        super().__init__()
        label = QPushButton("MIAAU")
        
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planner")
        self.showMaximized()
        self.schedule = Schedule()
        self.schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()
        self.planNr = 0
        self.menu = Menu()
        self.plan = None
        footer = Footer()
    
        layout.addWidget(self.menu, 0, 0)
        layout.addWidget(self.schedule, 1, 0)
        layout.addWidget(footer, 2, 0)

        self.menu.button.clicked.connect(self.getHTML)
        self.menu.button2.clicked.connect(self.getPrevPlan)
        self.menu.button3.clicked.connect(self.getNextPlan)

        self.setLayout(layout)

    def getHTML(self):
        path = QFileDialog.getOpenFileName()
        parsed = parseHTML(path[0])
        # parsed = parseHTML("plan.html")
        self.plan = dfs(parsed)
        self.plan.sort(key=evaluatePlan)
        firstPlan = self.plan[0]
        listOfGroups = prepareForAdding(firstPlan)
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])

    def getNextPlan(self):
        self.schedule.destroyPlan()
        self.planNr += 1
        self.menu.planNr = self.planNr
        self.menu.planLabel.repaint()
        self.menu.planLabel.update()
        planToShow = self.plan[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])

    def getPrevPlan(self):
        self.schedule.destroyPlan()
        if self.planNr == 0:
            return
        self.planNr -= 1
        self.menu.planNr = self.planNr
        planToShow = self.plan[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])

        

if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    path = mainWindow.menu.path
    
    sys.exit(app.exec())
    