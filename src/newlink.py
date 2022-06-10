from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QVBoxLayout, QApplication,
    QLineEdit, QLabel,
    QHBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import logging

try:
    from src.constants import *
    import rc.resources
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    import rc.resources

class NewLink(QWidget):

    open_link_settings = pyqtSignal()
    update_url_list = pyqtSignal()

    def __init__(self, parser, parent=None):
        super(NewLink, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.parser = parser
        self.setup_UI()

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key.Key_Return:
            self.add()
        elif key_event.key() == Qt.Key.Key_Escape:
            self.close()
        return super().keyPressEvent(key_event)
    
    def setup_UI(self):
        self.setWindowTitle("Add New Link")
        self.setWindowIcon(QIcon(":/hyperlink.png"))
        self.mainlayout = QVBoxLayout()
        self.inputslayout = QGridLayout()
        self.btnslayout = QHBoxLayout()
        self.setLayout(self.mainlayout)

        self.setup_inputs()
        self.setup_btns()

        self.resize(self.mainlayout.sizeHint())
        self.setMinimumWidth(640)

    def setup_inputs(self):
        self.inputs_conf = {
            "link_name": ("Link Name:", QLineEdit),
            "url_link": ("URL Link:", QLineEdit)
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

    def setup_btns(self):
        self.btns_conf = {
            "cancel": ("Cancel", self.cancel),
            "submit": ("Add", self.add)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def cancel(self):
        self.open_link_settings.emit()
        self.close()

    def add(self):
        link_name = self.inputs["link_name"][1].text()
        url_link = self.inputs["url_link"][1].text()
        self.parser.set("urls", link_name.replace(" ", "_").lower(), url_link)
        with open(APP_CONFIG, "w") as cfgfile:
            self.parser.write(cfgfile)
        self.update_url_list.emit()
        self.open_link_settings.emit()
        self.close()

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    app = QApplication(sys.argv)
    widget = NewLink(parser)
    widget.show()
    sys.exit(app.exec())