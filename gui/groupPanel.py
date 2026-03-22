from src.classes import *
from gui.timetable import Schedule, prepareForAdding
import sys
from PySide6.QtCore import  *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
class EntryPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.text = None
        self.label = QLabel(self.text)
        self.button = QPushButton("MIAU")
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        


class GroupPanel(QWidget):
    def __init__(self, plan):
        super().__init__()
        self.plan = plan #Plan()

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
        view = QTreeView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Wybierz grupy:"])
        for course in self.plan.courseList:
            courseName = QStandardItem(course.name)
            for type in course.typeList:
                type.sort(key=lambda x: int(x.number))
                for group in type:
                    child = QStandardItem(group.giveKey())
                    child.setCheckable(True)
                    courseName.appendRow(child)
            model.appendRow(courseName)
        view.setModel(model)

        layout = QVBoxLayout(self)
        layout.addWidget(view)
        self.setLayout(layout)
           
        
        
        