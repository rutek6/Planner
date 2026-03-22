from src.classes import *

from src.parser import parseHTML
from src.conflictGraph import checkOverlap
from src.optimizer import evaluatePlan
from src.plan import dfs

from gui.prefPanel import PrefPanel
from gui.timetable import Schedule, prepareForAdding
from gui.menu import Menu

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, 
                               QPushButton, 
                               QWidget,
                               QHBoxLayout,
                               QVBoxLayout,
                               QLabel,
                               QFormLayout,
                               QGridLayout,
                               QSizePolicy,
                               QSpinBox,
                               QMainWindow,
                               QFileDialog)


    





class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.schedule = Schedule()
        self.menu = Menu()
        self.prefPanel = PrefPanel()
        layout = QGridLayout()

        self.plan = None
        self.planNr = 0
        
        
        
        self.setWindowTitle("Planner")
        
        self.schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        layout.addWidget(self.menu, 0, 0)
        layout.addWidget(self.schedule, 1, 0)
        layout.addWidget(self.prefPanel, 0, 1)

        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 1)


        self.menu.button.clicked.connect(self.getHTML)
        self.menu.button2.clicked.connect(self.getPrevPlan)
        self.menu.button3.clicked.connect(self.getNextPlan)
        self.menu.numberPicker.valueChanged.connect(self.getPlanFromNr)

        self.setLayout(layout)
        self.showMaximized()

    def getHTML(self):
        path = QFileDialog.getOpenFileName()
        parsed = parseHTML(path[0])
        self.plan = dfs(parsed)
        self.plan.sort(key=evaluatePlan)
        self.menu.nrOfPlans = len(self.plan)
        self.menu.numberPicker.setValue(1)
        firstPlan = self.plan[0]
        listOfGroups = prepareForAdding(firstPlan)
        self.schedule.destroyPlan()
        
        self.planNr = 0
        self.menu.planNr = 1
        self.menu.updateMenu()
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])

    def getNextPlan(self):
        self.schedule.destroyPlan()
        self.planNr += 1
        self.menu.planNr = self.planNr + 1
        self.menu.numberPicker.setValue(self.planNr + 1)
        self.menu.updateMenu()
        planToShow = self.plan[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])

    def getPrevPlan(self):
        if self.planNr == 0:
            return
        self.schedule.destroyPlan()
        self.planNr -= 1 
        self.menu.planNr = self.planNr + 1
        self.menu.numberPicker.setValue(self.planNr + 1)
        self.menu.updateMenu()

        planToShow = self.plan[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0],item[1],item[2],item[3], item[4], item[5])
    
    def getPlanFromNr(self):
        self.schedule.destroyPlan()
        shownPlanNr = self.menu.numberPicker.value()
        self.planNr = shownPlanNr - 1
        self.menu.planNr = self.planNr + 1
        self.menu.updateMenu()
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
    