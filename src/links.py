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

    def __init__(self, link_url, *args, parent=None):
        super(LinkButton, self).__init__(*args, parent)
        self.link_url = link_url

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
        self.link_names = [item.strip() for item in self.parser.get("list", "names").split(",")]
        for link_name in self.link_names:
            btn = LinkButton(link_name, link_name.replace("_", " ").upper())
            btn.clicked.connect(self.open_link)
            self.btnslayout.addWidget(btn)
        self.mainlayout.addLayout(self.btnslayout)

    def open_link(self):
        name = self.sender().link_url
        if self.parser.has_option("urls", name):
            if len(self.parser.get("urls", name)) > 0:
                webbrowser.open(self.parser.get("urls", name))
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