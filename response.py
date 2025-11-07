
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,  # layout
    QLabel, QTextEdit, QPushButton # inputs
)

from typing import List, Dict

from mcp import Mcp


class Response(QWidget):

    def __init__(self, panel: QWidget):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.panel = panel


        self.main()

    def main(self):

        self.layout.addWidget(QLabel('Resposta'))
        # resposta_mcp = QTextEdit()
        # resposta_mcp.setReadOnly(True)
        # self.layout.addWidget(resposta_mcp)

        # btn_perguntar = QPushButton('Perguntar')
        # self.layout.addWidget(btn_perguntar)

        # def fazer_pergunta():
        #     print(self.panel.get_dados())
        #     resposta_mcp.setPlainText(
        #         Mcp.to_string(Mcp.post_mcp(self.panel.get_tool_id(), self.login.get_contexto().get('token', ''), self.panel.get_dados()))
        #     )

        # btn_perguntar.clicked.connect(fazer_pergunta)
