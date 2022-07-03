from PyQt5.QtWidgets import (
    QApplication
)
from configparser import ConfigParser
from src.app import MainWindow
from src.constants import *
import sys, rc.resources, logging

# Main entry point of the application
if __name__=="__main__":
    # Initialize configuration parser
    parser = ConfigParser()
    # Parse the file path from APP_CONFIG in constants
    parser.read(APP_CONFIG)
    # If debug is enabled in the configuration, provide logs
    if parser.getboolean("application", "debug"):
        logging.basicConfig(
            filename=LOG_NAME, 
            format="[%(asctime)s] [%(levelname)s]: %(message)s",
            datefmt="%m-%d-%Y %H:%M:%S",
            encoding="utf-8", 
            level=logging.DEBUG
        )
    # Initialize PyQt5 Application
    app = QApplication(sys.argv)
    # Instantiate MainWindow QWidget
    mainwindow = MainWindow(parser)
    # Display the maximized window
    mainwindow.showMaximized()
    # Wait for an application to exit
    sys.exit(app.exec())