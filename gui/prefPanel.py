from src.classes import *
from src.parser import parseHTML
from src.conflictGraph import checkOverlap
from src.optimizer import evaluatePlan
from src.plan import dfs

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
                               QFormLayout,
                               QGridLayout,
                               QSizePolicy,
                               QSpinBox,
                               QMainWindow,
                               QFileDialog)


class PrefPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Hej")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)