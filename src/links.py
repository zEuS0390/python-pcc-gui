from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser

try:
    from src.constants import *
    from src.linkssettings import LinksSettings
except:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from constants import *
    from linkssettings import LinksSettings
    import rc.resources

class LinkButton(QPushButton):

    def __init__(self, url_link, *args, parent=None):
        super(LinkButton, self).__init__(*args, parent)
        self.url_link = url_link

class Links(QWidget):

    def __init__(self, parser, parent=None):
        super(Links, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.parser = parser
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
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumWidth(320)

    def setup_btns(self):
        self.urllinks_btn = QPushButton("URL LINKS SETTINGS")
        self.urllinks_btn.clicked.connect(self.open_links_settings)
        for link_name, url_link in self.parser.items("urls"):
            btn = LinkButton(url_link, link_name.replace("_", " ").upper())
            btn.clicked.connect(self.open_link)
            self.btnslayout.addWidget(btn)
        self.btnslayout.addWidget(self.urllinks_btn)
        self.mainlayout.addLayout(self.btnslayout)

    def open_link(self):
        url_link = self.sender().url_link
        webbrowser.open(url_link)
        self.close()

    def open_links_settings(self):
        self.linkssettings = LinksSettings(self.parser)
        self.linkssettings.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.linkssettings.close_links.connect(self.close)
        self.linkssettings.show()
        self.hide()

if __name__=="__main__":
    import sys, os
    from configparser import ConfigParser
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    app = QApplication(sys.argv)
    widget = Links(parser)
    widget.show()
    sys.exit(app.exec())