from PyQt5.QtWidgets import (
    QMainWindow, QPushButton,
    QVBoxLayout, QWidget,
    QLabel
)
from PyQt5.QtCore import Qt
from .settings import Settings

class MainWindow(QMainWindow):

    def __init__(self, parser, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.parser = parser
        self.setup_UI()

    def setup_UI(self):
        self.setWindowTitle(self.parser.get("application", "title"))
        self.resize(640, 480)

        self.mainwidget = QWidget()
        self.mainlayout = QVBoxLayout()
        self.mainwidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainwidget)

        self.btnslayout = QVBoxLayout()
        self.hdrlayout = QVBoxLayout()

        self.setup_hdr()
        self.setup_btns()

    def setup_hdr(self):
        hdr_title = QLabel(self.parser.get("application", "header_title"))
        self.hdrlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hdrlayout.addWidget(hdr_title)
        self.mainlayout.addStretch()
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
        self.mainlayout.addStretch()
        self.mainlayout.addLayout(self.btnslayout)
        self.mainlayout.addStretch()

    def open_settings(self):
        self.settings = Settings(self.parser)
        self.settings.show()