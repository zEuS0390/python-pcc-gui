from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import webbrowser

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
        self.btns_conf = {
            "login": ("LOGIN", self.login_link),
            "logout": ("LOGOUT", self.logout_link),
            "recommendations": ("RECOMMENDATIONS", self.recommendations_link),
            "coach_tracking": ("COACH TRACKING", self.coach_tracking_link)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def login_link(self):
        webbrowser.open(self.parser.get("links", "login"))
        self.close()

    def logout_link(self):
        webbrowser.open(self.parser.get("links", "logout"))
        self.close()

    def recommendations_link(self):
        webbrowser.open(self.parser.get("links", "recommendations"))
        self.close()

    def coach_tracking_link(self):
        webbrowser.open(self.parser.get("links", "coach_tracking"))
        self.close()

if __name__=="__main__":
    import sys, os
    from configparser import ConfigParser
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    parser = ConfigParser()
    parser.read("cfg/app.cfg")
    app = QApplication(sys.argv)
    widget = Links(parser)
    widget.show()
    sys.exit(app.exec())