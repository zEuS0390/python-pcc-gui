from PyQt5.QtWidgets import (
    QApplication
)
from configparser import ConfigParser
from src.app import MainWindow
import sys, rc.resources

if __name__=="__main__":
    parser = ConfigParser()
    parser.read("cfg/app.cfg")
    app = QApplication(sys.argv)
    mainwindow = MainWindow(parser)
    mainwindow.show()
    sys.exit(app.exec())