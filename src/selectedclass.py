from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QLineEdit,
    QLabel, QHBoxLayout,
    QComboBox, QTableWidget,
    QAbstractItemView, QAbstractScrollArea,
    QHeaderView, QPushButton,
    QTableWidgetItem, QGridLayout,
    QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import logging

try:
    from db.manager import *
    from db.tables import *
    from src.addstudent import AddStudent
    from src.constants import *
    from src.handledclassattendance import HandledClassAttendance
    import rc.resources
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    from db.manager import *
    from db.tables import *
    from addstudent import AddStudent
    from handledclassattendance import HandledClassAttendance
    import rc.resources

class SelectedClass(QWidget):

    def __init__(self, handledclass_id: int, db: Manager, parent=None):
        super(SelectedClass, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.handledclass_id = handledclass_id
        self.db = db
        self.setup_UI()
        self.destroyed.connect(SelectedClass._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("SelectedClass instance deleted.")

    def setup_UI(self):
        handledclass = get_handled_class(self.db, self.handledclass_id)
        self.setWindowIcon(QIcon(":/add_class.png"))
        self.setWindowTitle("Handled Class ({} {} {})".format("{}-{}".format(handledclass.course.name, handledclass.course.part), handledclass.schedule, handledclass.time))

        self.mainlayout = QVBoxLayout()
        self.headerlayout = QHBoxLayout()
        self.detailslayout = QGridLayout()
        self.optionslayout = QVBoxLayout()
        self.studentstablelayout = QVBoxLayout()

        self.setup_header_contents()
        self.setup_students_table()

        self.setLayout(self.mainlayout)
        self.resize(640, 480)

    def setup_header_contents(self):
        self.setup_details()
        self.setup_options()
        self.mainlayout.addLayout(self.headerlayout)

    def setup_details(self):
        self.detailsGroup = QGroupBox("Details")
        self.detailsGroup.setLayout(self.detailslayout)
        self.inputs_conf = {
            "course": ("Course:", QComboBox),
            "schedule": ("Schedule:", QLineEdit),
            "time": ("Time:", QLineEdit),
            "sessions": ("Sessions:", QLineEdit),
        }
        self.inputs = {}
        row = 0
        for name, val in self.inputs_conf.items():
            obj = None
            label = QLabel(val[0])
            if val[1] == QLineEdit or val[1] == QComboBox or val[1] == QLabel:
                obj = val[1]()
            self.detailslayout.addWidget(label, row, 0)
            self.detailslayout.addWidget(obj, row, 1)
            self.inputs[name] = (label, obj)
            row += 1
        self.headerlayout.addWidget(self.detailsGroup, 50)
        self.update_combobox()

    def setup_options(self):
        self.optionsGroup = QGroupBox("Options")
        self.optionsGroup.setLayout(self.optionslayout)
        self.btns_conf = {
            "attendance": ("Attendance", self.open_class_attendance),
            "assignments": ("Assignments", lambda: None),
            "activities": ("Activities", lambda: None),
            "quizzes": ("Quizzes", lambda: None)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            self.optionslayout.addWidget(btn)
            self.btns[name] = btn
        self.headerlayout.addWidget(self.optionsGroup, 50)

    def setup_students_table(self):
        self.student_ids = []
        self.students_in_table = []
        table_headers = {
            "fname": "First Name",
            "mname": "Middle Name",
            "lname": "Last Name",
            "gender": "Gender",
            "age": "Age"
        }
        self.studentstable = QTableWidget()
        self.studentstable.setColumnCount(len(table_headers))
        self.studentstable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.studentstable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.studentstable.horizontalHeader().setStretchLastSection(True)
        self.studentstable.verticalHeader().setVisible(True)
        self.studentstable.setAlternatingRowColors(True)
        self.studentstable.setHorizontalHeaderLabels(table_headers.values())
        self.studentstable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.studentstable.verticalHeader().setVisible(False)
        self.studentstable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.studentstable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.studentstable_header = self.studentstable.horizontalHeader()
        self.studentstable_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.studentstable_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.studentstable_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.studentstable_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.studentstablelayout.addWidget(self.studentstable)
        self.mainlayout.addLayout(self.studentstablelayout)

        self.refresh_students_table()

    def update_student_table(self, added_student_id: int):
        if added_student_id not in self.student_ids:
            self.student_ids.append(added_student_id)

        if added_student_id not in self.students_in_table:
            self.students_in_table.append(added_student_id)
            student = get_student(self.db, added_student_id)
            if student is not None:
                row = self.studentstable.rowCount()
                self.studentstable.setRowCount(row+1)
                fname = QTableWidgetItem(student.fname)
                fname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                mname = QTableWidgetItem(student.mname)
                mname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                lname = QTableWidgetItem(student.lname)
                lname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                age = QTableWidgetItem(str(student.age))
                age.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                gender = QTableWidgetItem(student.gender)
                gender.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.studentstable.setItem(row, 0, fname)
                self.studentstable.setItem(row, 1, mname)
                self.studentstable.setItem(row, 2, lname)
                self.studentstable.setItem(row, 3, gender)
                self.studentstable.setItem(row, 4, age)

    def refresh_students_table(self):
        handledclass = get_handled_class(self.db, self.handledclass_id)
        students = get_students_in_class(self.db, self.handledclass_id)
        self.studentstable.setRowCount(0)
        self.inputs["course"][1].setCurrentText("{}-{}".format(handledclass.course.name, handledclass.course.part))
        self.inputs["course"][1].setEnabled(False)
        self.inputs["schedule"][1].setText(handledclass.schedule)
        self.inputs["schedule"][1].setReadOnly(True)
        self.inputs["time"][1].setText(handledclass.time)
        self.inputs["time"][1].setReadOnly(True)
        self.inputs["sessions"][1].setText("{}/{}".format(handledclass.current_session, handledclass.sessions))
        self.inputs["sessions"][1].setReadOnly(True)
        for student in students:
            self.update_student_table(student.student_id)

    def update_combobox(self):
        self.inputs["course"][1].clear()
        courses = ["{}-{}".format(course.name, course.part) for course in get_courses(self.db)]
        self.inputs["course"][1].addItems(courses)

    def open_class_attendance(self):
        self.classattendance = HandledClassAttendance(self.handledclass_id, self.db)
        self.classattendance.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.classattendance.show()

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = SelectedClass(manager)
    widget.show()
    sys.exit(app.exec())