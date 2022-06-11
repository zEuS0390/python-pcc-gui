from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
    QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .handledclasses import HandledClasses
from .preferences import Preferences
from .links import Links
from .students import Students
from .courses import Courses
from db.manager import Manager
from .constants import *

class MainWindow(QMainWindow):

    def __init__(self, parser, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.parser = parser
        self.setup_UI()

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key.Key_Escape:
            self.close()
        elif key_event.key() == Qt.Key.Key_S:
            self.open_settings()
        return super().keyPressEvent(key_event)

    def setup_UI(self):

        self.db = Manager(self.parser)

        self.setWindowIcon(QIcon(":/app_icon.png"))
        self.setWindowTitle(self.parser.get("application", "title"))
        self.resize(640, 480)

        self.mainwidget = QWidget()
        self.mainlayout = QVBoxLayout()
        self.mainwidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainwidget)

        self.contentlayout = QHBoxLayout()
        self.sidebarlayout = QVBoxLayout()
        self.btnslayout = QVBoxLayout()
        self.hdrlayout = QVBoxLayout()

        self.setup_hdr()
        self.setup_btns()

        self.mainlayout.addLayout(self.contentlayout)
        self.mainlayout.addLayout(self.sidebarlayout)

    def setup_hdr(self):
        self.hdr_title = QLabel(self.parser.get("application", "header_title"))
        self.hdrlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hdrlayout.addWidget(self.hdr_title)
        self.mainlayout.addLayout(self.hdrlayout)

    def setup_btns(self):
        self.btns_conf = {
            "Handled Classes": self.open_classes,
            "Registered Courses": self.open_courses,
            "List of Students": self.open_students,
            "URL Links": self.open_links,
            "Preferences": self.open_settings
        }
        self.btns = []
        for name, func in self.btns_conf.items():
            btn = QPushButton(name)
            btn.clicked.connect(func)
            self.btnslayout.addWidget(btn)
            self.btns.append(btn)
        self.sidebarlayout.addStretch()
        self.sidebarlayout.addLayout(self.btnslayout)
        self.sidebarlayout.addStretch()

    def open_classes(self):
        self.classes = HandledClasses(self.db)
        self.classes.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.classes.show()

    def open_settings(self):
        self.preferences = Preferences(self.parser)
        self.preferences.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.preferences.apply_preferences.connect(self.apply_preferences)
        self.preferences.show()

    def apply_preferences(self):
        self.parser.read(APP_CONFIG)
        self.setWindowTitle(self.parser.get("application", "title"))
        self.hdr_title.setText(self.parser.get("application", "header_title"))

    def open_links(self):
        self.links = Links(self.parser)
        self.links.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.links.show()

    def open_students(self):
        self.students = Students(self.db)
        self.students.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.students.show()
    
    def open_courses(self):
        self.courses = Courses(self.db)
        self.courses.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.courses.show()