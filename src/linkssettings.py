from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QListWidget,
    QLineEdit, QPushButton,
    QHBoxLayout, QListWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from src.constants import *
    from src.newlink import NewLink
    import rc.resources
except:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    from newlink import NewLink
    import rc.resources

class LinksSettings(QWidget):

    close_links = pyqtSignal()

    def __init__(self, parser, parent=None):
        super(LinksSettings, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.parser = parser
        self.setup_UI()

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/hyperlink.png"))
        self.setWindowTitle("URL Links")
        self.mainlayout = QVBoxLayout()
        self.listlayout = QVBoxLayout()
        self.btnslayout = QHBoxLayout()
        self.setup_url_list()
        self.setup_btns()
        self.update_url_list()
        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumWidth(640)

    def setup_url_list(self):
        self.urllist = QListWidget()
        self.urllist.itemClicked.connect(
            lambda: self.urllink.setText(
                self.parser.get("urls", self.urllist.currentItem().text().replace(" ", "_").lower())
            )
        )
        self.urllink = QLineEdit()
        self.mainlayout.addWidget(self.urllist)
        self.mainlayout.addWidget(self.urllink)
        self.mainlayout.addLayout(self.listlayout)

    def setup_btns(self):
        self.btns_conf = {
            "cancel": ("Cancel", self.cancel),
            "submit": ("Apply", self.apply)
        }
        self.btns = {}
        self.btns["new"] = QPushButton("New")
        self.btns["new"].clicked.connect(self.open_add_new_link)
        self.btnslayout.addWidget(self.btns["new"])
        self.btns["delete"] = QPushButton("Delete")
        self.btns["delete"].clicked.connect(self.delete_url_link)
        self.btnslayout.addWidget(self.btns["delete"])
        self.btnslayout.addStretch()
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def cancel(self):
        self.close_links.emit()
        self.close()

    def apply(self):
        if self.urllist.currentItem() is not None:
            self.parser.set("urls", self.urllist.currentItem().text().replace(" ", "_").lower(), self.urllink.text())
            with open(APP_CONFIG, "w") as cfgfile:
                self.parser.write(cfgfile)
        self.close_links.emit()
        self.close()

    def delete_url_link(self):
        if self.urllist.currentItem() is not None:
            self.urllink.clear()
            self.parser.remove_option("urls", self.urllist.currentItem().text().replace(" ", "_").lower())
            self.urllist.takeItem(self.urllist.currentRow())
            with open(APP_CONFIG, "w") as cfgfile:
                self.parser.write(cfgfile)
            self.update_url_list()

    def update_url_list(self):
        self.urllist.clear()
        for link_name, url_link in self.parser.items("urls"):
            self.urllist.addItem(QListWidgetItem(link_name.replace("_", " ").upper()))

    def open_add_new_link(self):
        self.newlink = NewLink(self.parser)
        self.newlink.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.newlink.open_link_settings.connect(self.show)
        self.newlink.update_url_list.connect(self.update_url_list)
        self.newlink.show()
        self.hide()

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    app = QApplication(sys.argv)
    widget = LinksSettings(parser)
    widget.show()
    sys.exit(app.exec())