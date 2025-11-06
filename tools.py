
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,  # layout
    QLabel, QTextEdit, QPushButton # inputs
)

from PySide6.QtCore import QTimer

from typing import List, Dict

from mcp import Mcp


class Tools(QWidget):

    def __init__(self, login: QWidget):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.login = login

        self.main()

    def main(self):

        # Login dialog at start
        QTimer.singleShot(200, self.login.main)

        self.layout.addWidget(QLabel('Tools'))
        resumo_tools = QTextEdit()
        resumo_tools.setReadOnly(True)
        self.layout.addWidget(resumo_tools)

        btn_buscar_tools = QPushButton('Buscar Tools')
        self.layout.addWidget(btn_buscar_tools)

        def buscar_tools():
            resumo_tools.setPlainText(
                Mcp.to_string(
                    Mcp.get_tools(self.login.get_contexto().get('token', ''))
                )
            )

        btn_buscar_tools.clicked.connect(buscar_tools)

