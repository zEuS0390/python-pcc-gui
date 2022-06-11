from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QTableWidget,
    QAbstractScrollArea, QAbstractItemView,
    QHeaderView, QTableWidgetItem,
    QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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
        self.db = db
        self.setup_UI()

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/classes.png"))
        self.setWindowTitle("Handled Classes")

        self.mainlayout = QVBoxLayout()
        self.classestablelayout = QVBoxLayout()

        self.setup_classes_table()

        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumWidth(640)

    def setup_classes_table(self):
        classestable_headers = {
            "course": "Course",
            "schedule": "Schedule",
            "time": "Time",
            "students": "Students",
            "days": "Days",
            "open": " ",
            "archive": " "
        }
        self.classestable = QTableWidget()
        self.classestable.setColumnCount(len(classestable_headers))
        self.classestable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.classestable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.classestable.horizontalHeader().setStretchLastSection(True)
        self.classestable.verticalHeader().setVisible(True)
        self.classestable.setAlternatingRowColors(True)
        self.classestable.setHorizontalHeaderLabels(classestable_headers.values())
        self.classestable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.classestable.verticalHeader().setVisible(False)
        self.classestable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.classestable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.classestable_header = self.classestable.horizontalHeader()
        for row, _ in enumerate(classestable_headers):
            self.classestable_header.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        self.classestablelayout.addWidget(self.classestable)
        self.mainlayout.addLayout(self.classestablelayout)

        self.update_classes_table()

    def update_classes_table(self):
        handled_classes = get_handled_classes(self.db)
        self.classestable.setRowCount(len(handled_classes))
        for row, handled_class in enumerate(handled_classes):
            print(handled_class)
            open_btn = QPushButton("Open")
            archive_btn = QPushButton("Archive")
            course = QTableWidgetItem("{}-{}".format(handled_class.course.name, handled_class.course.part))
            course.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            schedule = QTableWidgetItem(handled_class.schedule)
            schedule.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            hctime = QTableWidgetItem(handled_class.time)
            hctime.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            days = QTableWidgetItem(str(handled_class.sessions))
            days.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            no_of_students = QTableWidgetItem(str(len(handled_class.students)))
            no_of_students.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.classestable.setItem(row, 0, course)
            self.classestable.setItem(row, 1, schedule)
            self.classestable.setItem(row, 2, hctime)
            self.classestable.setItem(row, 3, no_of_students)
            self.classestable.setItem(row, 4, days)
            self.classestable.setCellWidget(row, 5, open_btn)
            self.classestable.setCellWidget(row, 6, archive_btn)

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = Classes(manager)
    widget.show()
    sys.exit(app.exec())