from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QVBoxLayout, QApplication,
    QLineEdit, QLabel,
    QHBoxLayout, QPushButton,
    QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import logging

try:
    from db.manager import *
    from db.tables import *
    from src.constants import *
    import rc.resources
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    from db.manager import *
    from db.tables import *
    import rc.resources

class NewCourse(QWidget):

    update_list = pyqtSignal()

    def __init__(self, db: Manager, parent=None):
        super(NewCourse, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(NewCourse._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("NewCourse instance deleted.")

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key.Key_Return:
            self.add()
        elif key_event.key() == Qt.Key.Key_Escape:
            self.close()
        return super().keyPressEvent(key_event)
    
    def setup_UI(self):
        self.setWindowTitle("Add New Course")
        self.setWindowIcon(QIcon(":/book_icon.png"))
        self.mainlayout = QVBoxLayout()
        self.inputslayout = QGridLayout()
        self.btnslayout = QHBoxLayout()
        self.setLayout(self.mainlayout)
        self.setup_inputs()
        self.setup_btns()
        self.resize(self.mainlayout.sizeHint())

    def setup_inputs(self):
        self.inputs_conf = {
            "course_title": ("Course Title:", QLineEdit),
            "course_part": ("Course Part:", QComboBox),
            "course_desc": ("Course Description", QLineEdit)
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
            elif val[1] == QComboBox:
                obj = val[1]()
            self.inputslayout.addWidget(label, row, col)
            col += 1
            self.inputslayout.addWidget(obj, row, col)
            self.inputs[name] = (label, obj)
            row += 1
        self.mainlayout.addLayout(self.inputslayout)

        self.update_combobox()

    def setup_btns(self):
        self.btns_conf = {
            "cancel": ("Cancel", self.close),
            "submit": ("Add", self.add)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def add(self):
        add_new_course(
            self.db,
            name=self.inputs["course_title"][1].text(),
            part=self.inputs["course_part"][1].currentText(),
            desc=self.inputs["course_desc"][1].text()
        )
        self.update_list.emit()
        self.close()

    def update_combobox(self):
        self.inputs["course_part"][1].clear()
        course_parts = ["101", "102", "103"]
        self.inputs["course_part"][1].addItems(course_parts)

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = NewCourse(manager)
    widget.show()
    sys.exit(app.exec())