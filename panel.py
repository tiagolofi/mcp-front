from PySide6.QtWidgets import (
    QWidget, QGroupBox, QFormLayout,  # layout
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox # inputs
)
from PySide6.QtCore import Qt

from typing import List, Tuple, Dict

from mcp import Mcp

class Panel(QGroupBox):
    def __init__(self, login: QWidget) -> None:
        super().__init__()

        self.headers, self.params, self.paths = [], [], []
        self.prompt = None
        self.tipo = None
        self.tool_id = None

        self.dados = None

        self.login = login

        self.layout = QFormLayout(self)

        self.main()
    
    def __addWidget(self, widgets: List[Tuple[QWidget, QWidget]]) -> None:
        for i in widgets:
            self.layout.addRow(*i)

    def get_tool_id(self):
        return int(self.tool_id.text())
    
    def get_dados(self):
        return self.dados

    def main(self):
        self.tool_id = QLineEdit()
        self.layout.addRow(QLabel('Tool Id'), self.tool_id)

        header = QLineEdit()
        header_value = QLineEdit()
        param = QLineEdit()
        param_value = QLineEdit()
        path = QLineEdit()
        prompt = QTextEdit()
        tipo = QComboBox()
        tipo.addItems(['PROMPT', 'WEB_SEARCH'])

        header_widgets = [
            (QLabel('Header'), header),
            (QLabel('Valor do Header'), header_value),
        ]
        self.__addWidget(header_widgets)
        btn_salvar_header = QPushButton('Salvar Header')
        self.layout.addRow(btn_salvar_header)

        param_widgets = [
            (QLabel('Parâmetro'), param),
            (QLabel('Valor do Parâmetro'), param_value),
        ]
        self.__addWidget(param_widgets)
        btn_salvar_param = QPushButton('Salvar Parâmetro')
        self.layout.addRow(btn_salvar_param)

        self.layout.addRow(QLabel('Path'), path)
        btn_salvar_path = QPushButton('Salvar Path')
        self.layout.addRow(btn_salvar_path)

        self.layout.addRow(QLabel('Prompt'), prompt)
        self.layout.addRow(QLabel('Tipo'), tipo)

        self.layout.addRow(QLabel('Prévia'))
        resumo = QTextEdit()
        resumo.setReadOnly(True)
        self.layout.addRow(resumo)

        def set_headers() -> None:
            self.headers.append({header.text(): header_value.text()})
            header.clear()
            header_value.clear()
            update()

        def set_params() -> None:
            self.params.append({param.text(): param_value.text()})
            param.clear()
            param_value.clear()
            update()

        def set_paths() -> None:
            self.paths.append(path.text())
            path.clear()
            update()

        def update() -> None:
            self.prompt = prompt.toPlainText()
            self.tipo = tipo.currentText()

            self.dados = {
                'prompt': self.prompt,
                'type': self.tipo,
                'headers': self.headers,
                'params': self.params,
                'paths': self.paths
            }

            resumo.setPlainText(Mcp.to_string(self.dados))            

        btn_salvar_header.clicked.connect(set_headers)
        btn_salvar_param.clicked.connect(set_params)
        btn_salvar_path.clicked.connect(set_paths)
        prompt.textChanged.connect(update)
        tipo.currentIndexChanged.connect(update)

