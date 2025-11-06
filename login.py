
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,  # layout
    QLabel, QLineEdit, QPushButton # inputs
)

from typing import List, Dict

from mcp import Mcp

class Login(QWidget):

    def __init__(self) -> None:
        super().__init__()    

        self.token = None
        self.username = None

        self.layout = QVBoxLayout(self)
        
        self.main()

    def __addWidget(self, widgets: List[QWidget]) -> None:
        for i in widgets:
            self.layout.addWidget(i)

    def main(self):
        user_label = QLabel('Username')
        self.username = QLineEdit()
        pwd_label = QLabel('Password')
        password = QLineEdit()
        password.setEchoMode(QLineEdit.EchoMode.Password)
        btn_login = QPushButton('Login')

        self.__addWidget([user_label, self.username, pwd_label, password, btn_login])

        def do_login():
            self.token = Mcp.login({'username': self.username.text(), 'password': password.text()})
            password.clear()
            print(self.get_contexto())

        btn_login.clicked.connect(do_login)


    def get_contexto(self) -> Dict[str, str]:
        return {
            'username': self.username.text().strip(),
            'token': self.token
        }
