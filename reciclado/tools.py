
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,  # layout
    QLabel, QTextEdit, QPushButton # inputs
)

from PySide6.QtCore import QTimer

from typing import List, Dict

from mcp import Mcp


class Tools(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.main()

    def main(self):

        self.layout.addWidget(QLabel('Tools'))


