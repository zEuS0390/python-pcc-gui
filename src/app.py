from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
    QLabel, QHBoxLayout, 
    QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont
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

        self.setup_btns()

        self.btnslayout.setContentsMargins(50, 50, 50, 50)

        self.mainlayout.addLayout(self.contentlayout)
        self.mainlayout.addLayout(self.sidebarlayout)

    def setup_btns(self):
        self.btns_conf = {
            "Handled Classes": self.open_classes,
            "Registered Courses": self.open_courses,
            "List of Students": self.open_students,
            "URL Links": self.open_links,
            "Preferences": self.open_settings
        }
        self.btns = []
        font = QFont()
        font.setPointSize(18)
        font.setFamily("Roboto Mono")
        for name, func in self.btns_conf.items():
            btn = QPushButton(name)
            btn.clicked.connect(func)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            self.btnslayout.addWidget(btn)
            self.btns.append(btn)
        self.sidebarlayout.addLayout(self.btnslayout)

    def open_classes(self):
        self.classes = HandledClasses(self.db)
        self.classes.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.classes.showMaximized()

    def open_settings(self):
        self.preferences = Preferences(self.parser)
        self.preferences.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.preferences.apply_preferences.connect(self.apply_preferences)
        self.preferences.show()

    def apply_preferences(self):
        self.parser.read(APP_CONFIG)
        self.setWindowTitle(self.parser.get("application", "title"))

    def open_links(self):
        self.links = Links(self.db)
        self.links.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.links.showMaximized()

    def open_students(self):
        self.students = Students(self.db)
        self.students.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.students.showMaximized()
    
    def open_courses(self):
        self.courses = Courses(self.db)
        self.courses.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.courses.showMaximized()