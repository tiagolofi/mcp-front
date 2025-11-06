
from PySide6.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QSplitter, QGridLayout, QLabel
from PySide6.QtCore import Qt

import sys

from cache import Cache
from login import Login
from request import Request
from response import Response
from sidebar import Sidebar
from tools import Tools

class App(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        # atributos
        self.setWindowTitle('App')

        # telas
        self.login = Login()
        self.resize(700, 700)

        self.layout = QGridLayout(self)
        self.sidebar = Sidebar()

        self.views = QTabWidget()

        self.tools = Tools(self.login)
        self.views.addTab(self.tools, 'Tools')

        self.request = Request(self.login)
        self.views.addTab(self.request, 'Painel')

        self.response = Response(self.request, self.login)
        self.views.addTab(self.response, 'Resposta')

        self.layout.addWidget(self.sidebar, 0, 0)
        self.layout.addWidget(self.views, 0, 1)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)

    app = App()
    app.show()

    sys.exit(qapp.exec())
