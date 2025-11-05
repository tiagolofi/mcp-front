#!/usr/bin/env python3
"""
Floating pulsing circular widget using PySide6.
Includes login dialog, main input dialog with Tool ID, and live JSON preview.

Requirements:
    pip install PySide6 requests

Run:
    python3 floating_pulse_widget.py
"""

from PySide6.QtCore import (Qt, QPropertyAnimation, Property, QEasingCurve, QPoint)
from PySide6.QtGui import QPainter, QColor, QRegion
from PySide6.QtWidgets import (QApplication, QWidget, QDialog, QLabel, QVBoxLayout,
QPushButton, QLineEdit, QFormLayout, QHBoxLayout,
QComboBox, QTextEdit, QSplitter)

import sys, json, requests

class PulseWidget(QWidget):
    def __init__(self, diameter=120, min_scale=0.85, max_scale=1.25, parent=None):
        super().__init__(parent)

        self.token = None
        self.tools = None

        self._diameter = diameter
        self._scale = 1.0
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Pulse")

        self.resize(diameter, diameter)
        self._update_mask()

        self.anim = QPropertyAnimation(self, b'scale')
        self.anim.setStartValue(min_scale)
        self.anim.setEndValue(max_scale)
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QEasingCurve.InOutSine)
        self.anim.setLoopCount(-1)
        self.anim.start()

        self._drag_active = False
        self._drag_pos = QPoint(0, 0)

        # Login dialog at start
        QTimer = __import__('PySide6.QtCore').QtCore.QTimer
        QTimer.singleShot(200, self.open_login_dialog)

    def _get_scale(self):
        return self._scale

    def _set_scale(self, val):
        self._scale = float(val)
        self.update()

    scale = Property(float, _get_scale, _set_scale)

    def _update_mask(self):
        r = self.rect()
        region = QRegion(r, QRegion.Ellipse)
        self.setMask(region)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        center = self.rect().center()

        base_color = QColor(50, 130, 255)
        scale_radius = (min(w, h) / 2) * self._scale

        alpha = int(100 + 80 * abs(self._scale - 1))
        color = QColor(base_color)
        color.setAlpha(alpha)

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, int(scale_radius), int(scale_radius))

        core_color = QColor(base_color)
        core_color.setAlpha(230)
        painter.setBrush(core_color)
        painter.drawEllipse(center, int((min(w, h) / 2) * 0.4), int((min(w, h) / 2) * 0.4))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.MiddleButton:
            QApplication.quit()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            new_pos = event.globalPosition().toPoint() - self._drag_pos
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._drag_active:
                self._drag_active = False
            self.open_dialog()

    def open_login_dialog(self):
        global token

        login_dialog = QDialog(self)
        login_dialog.setWindowTitle("Login")
        login_dialog.resize(200, 200)
        login_layout = QVBoxLayout(login_dialog)

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        login_layout.addWidget(QLabel("Username"))
        login_layout.addWidget(username_input)
        login_layout.addWidget(QLabel("Password"))
        login_layout.addWidget(password_input)

        login_btn = QPushButton("Login")
        login_layout.addWidget(login_btn)

        def do_login():
            data = {"username": username_input.text(), "password": password_input.text()}
            try:
                r = requests.post("https://mcp-server-client-4dc341cd8433.herokuapp.com/login", json=data, timeout=5)
                if r.status_code == 200:
                    self.token = r.text.strip().replace('"', '')
                    login_dialog.accept()
                    self.get_tools()
                else:
                    QLabel(f"Erro: {r.status_code}").show()
            except Exception as e:
                QLabel(f"Erro: {e}").show()

        login_btn.clicked.connect(do_login)

        login_dialog.exec()

    def get_tools(self):
        try:
            headers_req = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            tools_resp = requests.get("https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp/tools", headers=headers_req, timeout=5)
            if tools_resp.status_code == 200:
                self.tools = json.dumps(tools_resp.json(), indent=2, ensure_ascii=False)
            else:
                self.tools = f"Erro ao carregar tools: {tools_resp.status_code}"
        except Exception as e:
            self.tools = f"Erro: {e}"

    def open_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configurações do MCP")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.resize(600, 900)

        splitter = QSplitter()

        # --- Painel lateral de tools disponíveis ---
        tools_box = QTextEdit()
        tools_box.setReadOnly(True)
        tools_box.setMinimumWidth(300)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Tool ID input
        main_layout.addWidget(QLabel("Tool ID"))
        tool_id_input = QLineEdit()
        main_layout.addWidget(tool_id_input)

        headers, params, paths = [], [], []

        # Headers
        main_layout.addWidget(QLabel("Headers"))
        h_key, h_val = QLineEdit(), QLineEdit()
        h_layout = QHBoxLayout()
        h_layout.addWidget(h_key)
        h_layout.addWidget(h_val)
        btn_add_header = QPushButton("Salvar Header")
        main_layout.addLayout(h_layout)
        main_layout.addWidget(btn_add_header)

        # Params
        main_layout.addWidget(QLabel("Params"))
        p_key, p_val = QLineEdit(), QLineEdit()
        p_layout = QHBoxLayout()
        p_layout.addWidget(p_key)
        p_layout.addWidget(p_val)
        btn_add_param = QPushButton("Salvar Param")
        main_layout.addLayout(p_layout)
        main_layout.addWidget(btn_add_param)

        # Paths
        main_layout.addWidget(QLabel("Paths"))
        path_input = QLineEdit()
        btn_add_path = QPushButton("Salvar Path")
        main_layout.addWidget(path_input)
        main_layout.addWidget(btn_add_path)

        # Prompt
        main_layout.addWidget(QLabel("Prompt"))
        prompt_input = QTextEdit()
        main_layout.addWidget(prompt_input)

        # Type
        main_layout.addWidget(QLabel("Type"))
        type_select = QComboBox()
        type_select.addItems(["PROMPT", "WEB_SEARCH"])
        main_layout.addWidget(type_select)

        # JSON Preview
        main_layout.addWidget(QLabel("Prévia do JSON"))
        json_preview = QTextEdit()
        json_preview.setReadOnly(True)
        main_layout.addWidget(json_preview)

        # Response box
        main_layout.addWidget(QLabel("Resposta do servidor"))
        response_box = QTextEdit()
        response_box.setReadOnly(True)
        main_layout.addWidget(response_box)

        btn_send = QPushButton("Perguntar")
        main_layout.addWidget(btn_send)

        def update_preview():
            data = {
                "headers": headers,
                "params": params,
                "paths": paths,
                "prompt": prompt_input.toPlainText(),
                "type": type_select.currentText(),
            }
            json_preview.setPlainText(json.dumps(data, indent=2, ensure_ascii=False))

        def add_header():
            if h_key.text() and h_val.text():
                headers.append({h_key.text(): h_val.text()})
                h_key.clear(); h_val.clear(); update_preview()

        def add_param():
            if p_key.text() and p_val.text():
                params.append({p_key.text(): p_val.text()})
                p_key.clear(); p_val.clear(); update_preview()

        def add_path():
            if path_input.text():
                paths.append(path_input.text())
                path_input.clear(); update_preview()

        btn_add_header.clicked.connect(add_header)
        btn_add_param.clicked.connect(add_param)
        btn_add_path.clicked.connect(add_path)
        prompt_input.textChanged.connect(update_preview)
        type_select.currentIndexChanged.connect(update_preview)

        def send_request():
            tool_id = tool_id_input.text().strip()
            data = {
                "headers": headers,
                "params": params,
                "paths": paths,
                "prompt": prompt_input.toPlainText(),
                "type": type_select.currentText(),
            }
            update_preview()

            try:
                headers_req = {"Authorization": f"Bearer {self.token}" if self.token else ""}
                r = requests.post(f"https://mcp-server-client-4dc341cd8433.herokuapp.com/mcp?toolId={tool_id}", json=data, headers=headers_req)
                response_box.setPlainText(json.dumps(r.json(), indent=2, ensure_ascii=False))
            except Exception as e:
                response_box.setPlainText(f"Erro: {e}")

        btn_send.clicked.connect(send_request)

        tools_box.setPlainText(self.tools)

        splitter.addWidget(main_widget)
        splitter.addWidget(tools_box)

        layout = QVBoxLayout(dialog)
        layout.addWidget(splitter)
        dialog.setLayout(layout)


        dialog.exec()


def main():
    app = QApplication(sys.argv)

    w = PulseWidget(diameter=120)
    screen = app.primaryScreen().availableGeometry()
    start_x = screen.right() - w.width() - 40
    start_y = screen.top() + 80
    w.move(start_x, start_y)
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
