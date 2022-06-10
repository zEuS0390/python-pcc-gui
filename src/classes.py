from PyQt5.QtWidgets import (
    QApplication, QWidget
)
from PyQt5.QtGui import QIcon

try:
    from db.manager import *
    from db.tables import *
    import rc.resources
except:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from src.constants import *
    from db.manager import *
    from db.tables import *
    import rc.resources

class Classes(QWidget):

    def __init__(self, db, parent=None):
        super(Classes, self).__init__(parent)
        self.setup_UI()

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/classes.png"))
        self.setWindowTitle("Handled Classes")

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = Classes(manager)
    widget.show()
    sys.exit(app.exec())