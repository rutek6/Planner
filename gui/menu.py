from src.classes import *
from src.parser import parseHTML
from src.conflictGraph import checkOverlap
from src.optimizer import evaluatePlan
from src.plan import dfs

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


class Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.path = ""
        self.planNr = 1
        self.nrOfPlans = None
        self.button = QPushButton("Otwórz HTML")
        self.button2 = QPushButton("Prev")
        self.button3 = QPushButton("Next")
        self.numberPicker = QSpinBox()
        self.planLabel = QLabel(f"{str(self.planNr)} / {self.nrOfPlans}")

        self.numberPicker.setMinimum(1)

        self.button.setFixedWidth(150)
        self.button2.setFixedWidth(150)
        self.button3.setFixedWidth(150)
        self.numberPicker.setMaximumWidth(250)
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.numberPicker)
        layout.addWidget(self.planLabel)

        self.setLayout(layout)

    def updateMenu(self):
        self.planLabel.setText(f"{str(self.planNr)} / {self.nrOfPlans}")
        self.numberPicker.setMaximum(self.nrOfPlans)
        self.planLabel.repaint()
