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
        


class PrefPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Hej")
        entry1 = EntryPanel()
        
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(entry1)
        self.setLayout(layout)
        