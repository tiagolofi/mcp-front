
from PySide6.QtWidgets import QApplication, QTabWidget

import sys

from cache import Cache
from login import Login
from panel import Panel
from response import Response
from tools import Tools

class App(QTabWidget):
    def __init__(self) -> None:
        super().__init__()
        
        # atributos
        self.setWindowTitle('App')

        Cache.insert({"teste": "teste"})

        # telas
        self.login = Login()
        self.addTab(self.login, 'Login')

        self.tools = Tools(self.login)
        self.addTab(self.tools, 'Tools')

        self.panel = Panel(self.login)
        self.addTab(self.panel, 'Painel')

        self.response = Response(self.panel, self.login)
        self.addTab(self.response, 'Resposta')

if __name__ == '__main__':
    qapp = QApplication(sys.argv)

    app = App()
    app.show()

    sys.exit(qapp.exec())
