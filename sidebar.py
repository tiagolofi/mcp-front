
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout, QGroupBox, QTabWidget, # layout
    QLabel, QTextEdit, QPushButton # inputs
)
from PySide6.QtCore import Qt

from typing import List, Dict

from mcp import Mcp

class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget(tabsClosable=True, tabPosition=QTabWidget.TabPosition.West)

        self.tabs.addTab(QWidget(), 'Projeto 1')
        self.tabs.addTab(QWidget(), 'Projeto 2')
        self.tabs.addTab(QWidget(), 'Projeto 3')

        self.layout.addWidget(QLabel('Projetos'))
        self.layout.addWidget(self.tabs)

