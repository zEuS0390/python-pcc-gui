from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QPushButton,
    QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from src.constants import *
from src.linkssettings import LinksSettings
from db.manager import *
import webbrowser

class LinkButton(QPushButton):

    def __init__(self, url_link, *args, parent=None):
        super(LinkButton, self).__init__(*args, parent)
        self.url_link = url_link

class Links(QWidget):

    def __init__(self, db: Manager, parent=None):
        super(Links, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(Links._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("Links instance deleted.")

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/hyperlink.png"))
        self.setWindowTitle("Links")
        self.mainlayout = QVBoxLayout()
        self.btnslayout = QVBoxLayout()
        self.setup_btns()
        self.setLayout(self.mainlayout)
        self.btnslayout.setContentsMargins(50, 50, 50, 50)
        self.setMinimumWidth(320)

    def setup_btns(self):
        font = QFont()
        font.setPointSize(18)
        font.setFamily("Roboto Mono")
        self.urllinks_btn = QPushButton("URL LINKS SETTINGS")
        self.urllinks_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.urllinks_btn.clicked.connect(self.open_links_settings)
        self.urllinks_btn.setFont(font)
        for link in get_app_links(self.db):
            btn = LinkButton(link.url, link.name.replace("_", " ").upper())
            btn.clicked.connect(self.open_link)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            self.btnslayout.addWidget(btn)
        self.btnslayout.addWidget(self.urllinks_btn)
        self.mainlayout.addLayout(self.btnslayout)

    def open_link(self):
        url_link = self.sender().url_link
        webbrowser.open(url_link)
        self.close()

    def open_links_settings(self):
        self.linkssettings = LinksSettings(self.db)
        self.linkssettings.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.linkssettings.close_links.connect(self.close)
        self.linkssettings.showMaximized()
        self.hide()