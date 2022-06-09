from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QGridLayout, QLabel,
    QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from configparser import ConfigParser
import sys

class Settings(QWidget):

    def __init__(self, parser, parent=None):
        super(Settings, self).__init__(parent)
        self.parser = parser
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setup_UI()
        self.destroyed.connect(Settings._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("Settings instance deleted.")

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/gear_icon.png"))
        self.setWindowTitle("Settings")
        self.mainlayout = QVBoxLayout()
        self.inputslayout = QGridLayout()
        self.btnslayout = QHBoxLayout()
        self.setup_inputs()
        self.setup_btns()
        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())

    def setup_inputs(self):
        self.inputs_conf = {
            "app_title": ("App Title:\t", QLineEdit),
            "header_title": ("Header Title:\t", QLineEdit)
        }
        self.inputs = {}
        row = 0
        col = 0
        for name, val in self.inputs_conf.items():
            obj = None
            col = 0
            label = QLabel(val[0])
            col += 1
            if val[1] == QLineEdit:
                obj = val[1]()
            self.inputslayout.addWidget(label, row, col)
            col += 1
            self.inputslayout.addWidget(obj, row, col)
            self.inputs[name] = (label, obj)
            row += 1
        self.mainlayout.addLayout(self.inputslayout)

        self.inputs["app_title"][1].setText(self.parser.get("application", "title"))
        self.inputs["header_title"][1].setText(self.parser.get("application", "header_title"))

    def setup_btns(self):
        self.btns_conf = {
            "cancel": ("Cancel", self.close),
            "submit": ("Submit", lambda: None)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

if __name__=="__main__":
    parser = ConfigParser()
    parser.read("cfg/app.cfg")
    app = QApplication(sys.argv)
    widget = Settings(parser)
    widget.show()
    sys.exit(app.exec())