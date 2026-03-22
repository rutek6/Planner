from src.classes import *
from gui.timetable import Schedule, prepareForAdding
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, 
                               QPushButton, 
                               QWidget,
                               QHBoxLayout,
                               QVBoxLayout,
                               QLabel,
                               QCheckBox,
                               QComboBox,
                               QFrame,
                               QFormLayout,
                               QGridLayout,
                               QSizePolicy,
                               QSpinBox,
                               QMainWindow,
                               QFileDialog)
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
        layout = QVBoxLayout()
        for course in self.plan.courseList:
            courseName = QLabel(course.name)
            courseDropdown = QComboBox()
            
            for type in course.typeList:
                for group in type:
                    # group = QCheckBox(group.giveKey())
                    # layout.addWidget(group)
                    courseDropdown.addItem(group.giveKey())
            layout.addWidget(courseName)
            layout.addWidget(courseDropdown)
        
        self.setLayout(layout)
        