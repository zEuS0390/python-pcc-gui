from PyQt5.QtWidgets import (
    QApplication
)
from configparser import ConfigParser
from src.app import MainWindow
from src.constants import *
import sys, rc.resources, logging

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    if parser.getboolean("application", "debug"):
        logging.basicConfig(
            filename=LOG_NAME, 
            format="[%(asctime)s] [%(levelname)s]: %(message)s",
            datefmt="%m-%d-%Y %H:%M:%S",
            encoding="utf-8", 
            level=logging.DEBUG
        )
    app = QApplication(sys.argv)
    mainwindow = MainWindow(parser)
    mainwindow.showMaximized()
    sys.exit(app.exec())