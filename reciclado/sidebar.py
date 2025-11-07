
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout, QGroupBox, QTabWidget, # layout
    QLabel, QTextEdit, QPushButton # inputs
)
from PySide6.QtCore import Qt,Slot

from typing import List, Dict, Any

from mcp import Mcp

class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget(tabsClosable=True, tabPosition=QTabWidget.TabPosition.West)

        self.layout.addWidget(QLabel('Projetos'))
        self.layout.addWidget(self.tabs)

    def create_tabs(self):
        tools = Mcp.get_tools(Mcp.login_no_credentials())

        for i in tools.get('tools'):
            self.tabs.addTab(Tab(i), str(i.get('id')))

class Tab(QWidget):

    def __init__(self, tool: Dict[str, Any]):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.tool = tool
        self.create()

    def create(self):
        self.layout.addWidget(QTextEdit(self.tool.get('description')))
