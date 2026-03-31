from src.classes import *

from src.parser import parseHTML
from src.conflictGraph import checkOverlap
from src.optimizer import evaluatePlan, optimize
from src.plan import dfs
from src.preferences import *

from gui.groupPanel import GroupPanel
from gui.timetable import Schedule, prepareForAdding
from gui.menu import Menu

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
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
    QFileDialog,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Original list of plans with all possible combinations
        self.plan = None

        # Optimized list of plans with some combinations removed
        self.planOptimized = None
        self.planNr = 0

        self.preferences = Preferences()

        self.schedule = Schedule()
        self.menu = Menu()
        self.groupPanel = GroupPanel(self.plan)
        layout = QGridLayout()

        self.setWindowTitle("Planner")
        self.schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.menu, 0, 0, 1, 1)
        layout.addWidget(self.schedule, 1, 0, 1, 1)
        layout.addWidget(self.groupPanel, 0, 1, 2, 1)

        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 1)

        self.menu.button.clicked.connect(self.getHTML)
        self.menu.button2.clicked.connect(self.getPrevPlan)
        self.menu.button3.clicked.connect(self.getNextPlan)
        self.menu.numberPicker.valueChanged.connect(self.getPlanFromNr)

        self.groupPanel.applyButton.clicked.connect(self.applyPrefs)

        self.setLayout(layout)
        self.showMaximized()

    def getHTML(self):
        path = QFileDialog.getOpenFileName()
        parsed = parseHTML(path[0])
        self.groupPanel.plan = parsed
        self.groupPanel.destroyGroupPanel()
        self.groupPanel.printGroups()
        self.plan = dfs(parsed)

        self.planOptimized = self.plan.copy()
        self.planOptimized = optimize(self.planOptimized)

        self.menu.nrOfPlans = len(self.planOptimized)
        self.menu.numberPicker.setValue(1)
        firstPlan = self.planOptimized[0]
        listOfGroups = prepareForAdding(firstPlan)
        self.schedule.destroyPlan()

        self.planNr = 0
        self.menu.planNr = 1
        self.menu.updateMenu()

        for item in listOfGroups:
            self.schedule.addEvent(item[0], item[1], item[2], item[3], item[4], item[5])

    def getNextPlan(self):
        self.schedule.destroyPlan()
        self.planNr += 1
        self.menu.planNr = self.planNr + 1
        self.menu.numberPicker.setValue(self.planNr + 1)
        self.menu.updateMenu()
        planToShow = self.planOptimized[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0], item[1], item[2], item[3], item[4], item[5])

    def getPrevPlan(self):
        if self.planNr == 0:
            return
        self.schedule.destroyPlan()
        self.planNr -= 1
        self.menu.planNr = self.planNr + 1
        self.menu.numberPicker.setValue(self.planNr + 1)
        self.menu.updateMenu()

        planToShow = self.planOptimized[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0], item[1], item[2], item[3], item[4], item[5])

    def getPlanFromNr(self):
        self.schedule.destroyPlan()
        shownPlanNr = self.menu.numberPicker.value()
        self.planNr = shownPlanNr - 1
        self.menu.planNr = self.planNr + 1
        self.menu.updateMenu()
        planToShow = self.planOptimized[self.planNr]
        listOfGroups = prepareForAdding(planToShow)
        for item in listOfGroups:
            self.schedule.addEvent(item[0], item[1], item[2], item[3], item[4], item[5])

    def applyPrefs(self):
        self.groupPanel.chosenGroups.clear()
        self.preferences.requiredGroupList = self.groupPanel.giveChosenGroups()
        self.planOptimized = self.plan.copy()
        self.planOptimized = optimize(self.planOptimized, self.preferences)

        self.menu.nrOfPlans = len(self.planOptimized)
        self.menu.numberPicker.setValue(1)
        firstPlan = self.planOptimized[0]
        listOfGroups = prepareForAdding(firstPlan)
        self.schedule.destroyPlan()

        self.planNr = 0
        self.menu.planNr = 1
        self.menu.updateMenu()

        for item in listOfGroups:
            self.schedule.addEvent(item[0], item[1], item[2], item[3], item[4], item[5])


if __name__ == "__main__":
    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    path = mainWindow.menu.path

    sys.exit(app.exec())
