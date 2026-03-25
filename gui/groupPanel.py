from src.classes import *
from gui.timetable import Schedule, prepareForAdding
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class GroupPanel(QWidget):
    def __init__(self, plan):
        super().__init__()
        self.plan = plan  # Plan()
        self.time = QTimeEdit()
        self.view = QTreeView()
        self.model = QStandardItemModel()
        self.applyButton = QPushButton("Zastosuj")
        self.checkboxDict = {}  # [courseName]: (QStandardItem, Group)
        self.chosenGroups = []

    def makeCourseList(self):
        fullPlan = {}
        if len(self.plan):
            for group in self.plan[0]:
                if group.course.name not in fullPlan.keys():
                    fullPlan[group.course.name] = []
                fullPlan[group.course.name].append(group)

            return fullPlan
        return None

    def printGroups(self):
        self.model.setHorizontalHeaderLabels(["Wybierz grupy:"])
        for course in self.plan.courseList:
            courseName = QStandardItem(course.name)
            self.checkboxDict[course.name] = []
            for type in course.typeList:
                type.sort(key=lambda x: int(x.number))
                for group in type:
                    child = QStandardItem(group.giveKey())
                    child.setCheckable(True)
                    self.checkboxDict[course.name].append((child, group))
                    courseName.appendRow(child)
            self.model.appendRow(courseName)
        self.view.setModel(self.model)
        layout = QVBoxLayout(self)
        layout.addWidget(self.time)
        layout.addWidget(self.view)
        layout.addWidget(self.applyButton)
        self.setLayout(layout)

    def giveChosenGroups(self):
        for course, list in self.checkboxDict.items():
            for tuple in list:
                if tuple[0].checkState() == Qt.Checked:
                    self.chosenGroups.append(tuple[1])
        return self.chosenGroups

    def destroyGroupPanel(self):
        self.model.clear()
        self.checkboxDict.clear()
        self.setLayout(None)
