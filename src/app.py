from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
    QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .settings import Settings
from db.manager import Manager
from .constants import CONFIG_NAME

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
            "Class": lambda: print(True),
            "Settings": self.open_settings
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

    def open_settings(self):
        self.settings = Settings(self.parser)
        self.settings.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.settings.apply_settings.connect(self.apply_settings)
        self.settings.show()

    def apply_settings(self):
        self.parser.read(CONFIG_NAME)
        self.setWindowTitle(self.parser.get("application", "title"))
        self.hdr_title.setText(self.parser.get("application", "header_title"))