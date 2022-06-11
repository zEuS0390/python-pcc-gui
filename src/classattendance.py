from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QVBoxLayout
)
from PyQt5.QtGui import QIcon

from src.constants import APP_CONFIG

try:
    from db.manager import *
    from db.tables import *
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from db.manager import *
    from db.tables import *
    import rc.resources

class ClassAttendance(QWidget):

    def __init__(self, handledclass: int, db: Manager, parent=None):
        super(ClassAttendance, self).__init__(parent)
        self.handledclass = handledclass
        self.db = db
        self.setup_UI()

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/"))
        self.setWindowTitle("Class Attendance")
        self.mainlayout = QVBoxLayout()
        
        self.setLayout(self.mainlayout)

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = ClassAttendance(manager)
    widget.show()
    sys.exit(app.exec())
