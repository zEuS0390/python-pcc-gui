from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QTableWidget,
    QAbstractScrollArea, QAbstractItemView,
    QHeaderView, QHBoxLayout,
    QPushButton, QTableWidgetItem
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

try:
    from db.manager import *
    from db.tables import *
    from src.newcourse import NewCourse
    import rc.resources
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    from db.manager import *
    from db.tables import *
    from newcourse import NewCourse
    import rc.resources

class IndexCourse(QPushButton):

    def __init__(self, course_id, *args, parent=None):
        super(IndexCourse, self).__init__(*args, parent)
        self.course_id = course_id

class Courses(QWidget):

    def __init__(self, db, parent=None):
        super(Courses, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(Courses._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("Courses instance deleted.")

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/"))
        self.setWindowTitle("Registered Courses")
        self.mainlayout = QVBoxLayout()
        self.coursestablelayout = QVBoxLayout()
        self.tablebtnslayout = QHBoxLayout()
        self.setup_table_btns()
        self.setup_courses_table()
        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumSize(640, 480)
    
    def setup_courses_table(self):
        coursestable_headers = {
            "course_name": "Course Name",
            "course_part": "Course Part",
            "coures_desc": "Course Description",
            "handledclasses": "Handled Classes",
            "open": "",
            "archive": ""
        }
        self.coursestable = QTableWidget()
        self.coursestable.setColumnCount(len(coursestable_headers))
        self.coursestable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.coursestable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.coursestable.horizontalHeader().setStretchLastSection(True)
        self.coursestable.verticalHeader().setVisible(True)
        self.coursestable.setAlternatingRowColors(True)
        self.coursestable.setHorizontalHeaderLabels(coursestable_headers.values())
        self.coursestable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.coursestable.verticalHeader().setVisible(False)
        self.coursestable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.coursestable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.coursestable_header = self.coursestable.horizontalHeader()
        for row, _ in enumerate(coursestable_headers):
            self.coursestable_header.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        self.coursestablelayout.addWidget(self.coursestable)
        self.mainlayout.addLayout(self.coursestablelayout)

        self.update_courses_table()

    def setup_table_btns(self):
        self.tablebtnslayout.addStretch()
        self.btns_conf = {
            "new_course": ("New Course", self.open_new_course),
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.tablebtnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.tablebtnslayout)

    def open_new_course(self):
        self.newcourse = NewCourse(self.db)
        self.newcourse.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.newcourse.update_list.connect(self.update_courses_table)
        self.newcourse.show()

    def update_courses_table(self):
        self.coursestable.setRowCount(0)
        courses = get_courses(self.db)
        self.coursestable.setRowCount(len(courses))
        for row, course in enumerate(courses):
            open_btn = IndexCourse(course.course_id, "Edit")
            archive_btn = IndexCourse(course.course_id, "Archive")
            name = QTableWidgetItem(course.name)
            name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            part = QTableWidgetItem(course.part)
            part.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            desc = QTableWidgetItem(course.desc)
            desc.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            handledclasses = QTableWidgetItem(str(len(course.handledclasses)))
            handledclasses.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.coursestable.setItem(row, 0, name)
            self.coursestable.setItem(row, 1, part)
            self.coursestable.setItem(row, 2, desc)
            self.coursestable.setItem(row, 3, handledclasses)
            self.coursestable.setCellWidget(row, 4, open_btn)
            self.coursestable.setCellWidget(row, 5, archive_btn)
            open_btn.clicked.connect(self.open_selected_course)
            archive_btn.clicked.connect(self.archive_selected_course)

    def open_selected_course(self):
        print("EDIT:", self.sender().course_id)

    def archive_selected_course(self):
        print("ARCHIVE:", self.sender().course_id)
        

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = Courses(manager)
    widget.show()
    sys.exit(app.exec())