from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser

try:
    from src.constants import *
except:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from constants import *
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
        for link_name, url_link in self.parser.items("urls"):
            btn = LinkButton(url_link, link_name.replace("_", " ").upper())
            btn.clicked.connect(self.open_link)
            self.btnslayout.addWidget(btn)
        self.mainlayout.addLayout(self.btnslayout)

    def open_link(self):
        url_link = self.sender().url_link
        webbrowser.open(url_link)
        self.close()

if __name__=="__main__":
    import sys, os
    from configparser import ConfigParser
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    parser = ConfigParser()
    parser.read(LINKS_CONFIG)
    app = QApplication(sys.argv)
    widget = Links(parser)
    widget.show()
    sys.exit(app.exec())