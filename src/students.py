from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QTableWidget, QAbstractScrollArea,
    QAbstractItemView, QHeaderView,
    QPushButton, QTableWidgetItem,
    QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

try:
    from db.manager import *
    from db.tables import *
    from src.constants import *
    from src.newstudent import NewStudent
    import rc.resources
except ModuleNotFoundError:
    import os, sys
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from newstudent import NewStudent
    from constants import *
    from db.manager import *
    from db.tables import *
    import rc.resources

class IndexClass(QPushButton):

    def __init__(self, student_id: int, *args, parent=None):
        super(IndexClass, self).__init__(*args, parent)
        self.student_id = student_id

class Students(QWidget):

    def __init__(self, db, parent=None):
        super(Students, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(Students._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("Students instance deleted.")
    
    def setup_UI(self):
        self.setWindowIcon(QIcon(":/student.png"))
        self.setWindowTitle("Students")
        self.mainlayout = QVBoxLayout()
        self.studentstablelayout = QHBoxLayout()
        self.btnslayout = QHBoxLayout()
        self.setup_table_btns()
        self.setup_students_table()
        self.setLayout(self.mainlayout)
        self.setMinimumSize(800, 480)

    def setup_students_table(self):
        studentstable_headers = {
            "fname": "First Name",
            "mname": "Middle Name",
            "lname": "Last Name",
            "gender": "Gender",
            "age": "Age",
            "open": " ",
            "archive": " "
        }
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        self.studentstable = QTableWidget()
        self.studentstable.setFont(font)
        self.studentstable.setColumnCount(len(studentstable_headers))
        self.studentstable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.studentstable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.studentstable.horizontalHeader().setStretchLastSection(True)
        self.studentstable.verticalHeader().setVisible(True)
        self.studentstable.setAlternatingRowColors(True)
        self.studentstable.setHorizontalHeaderLabels(studentstable_headers.values())
        self.studentstable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.studentstable.verticalHeader().setVisible(False)
        self.studentstable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.studentstable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.studentstable_header = self.studentstable.horizontalHeader()
        for row, _ in enumerate(studentstable_headers):
            self.studentstable_header.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        self.studentstablelayout.addWidget(self.studentstable)
        self.mainlayout.addLayout(self.studentstablelayout)

        self.update_students_table()

    def update_students_table(self):
        self.studentstable.setRowCount(0)
        students = get_students(self.db)
        self.studentstable.setRowCount(len(students))
        for row, student in enumerate(students):
            open_btn = IndexClass(student.student_id, "Open")
            archive_btn = IndexClass(student.student_id, "Archive")
            fname = QTableWidgetItem(student.fname)
            fname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            mname = QTableWidgetItem(student.mname)
            mname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            lname = QTableWidgetItem(student.lname)
            lname.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            gender = QTableWidgetItem(student.gender)
            gender.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            age = QTableWidgetItem(str(student.age))
            age.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.studentstable.setItem(row, 0, fname)
            self.studentstable.setItem(row, 1, mname)
            self.studentstable.setItem(row, 2, lname)
            self.studentstable.setItem(row, 3, gender)
            self.studentstable.setItem(row, 4, age)
            self.studentstable.setCellWidget(row, 5, open_btn)
            self.studentstable.setCellWidget(row, 6, archive_btn)
            open_btn.clicked.connect(self.open_selected_student)
            archive_btn.clicked.connect(self.archive_selected_student)
    
    def setup_table_btns(self):
        self.btnslayout.addStretch()
        self.btns_conf = {
            "new_student": ("New Student", self.open_new_student),
        }
        self.btns = {}
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.clicked.connect(val[1])
            btn.setFont(font)
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def open_new_student(self):
        self.newstudent = NewStudent(self.db)
        self.newstudent.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.newstudent.update_list.connect(self.update_students_table)
        self.newstudent.show()

    def open_selected_student(self):
        pass

    def archive_selected_student(self):
        student_id = self.sender().student_id
        print(student_id)
        delete_student(self.db, student_id)
        self.update_students_table()


if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = Students(manager)
    widget.show()
    sys.exit(app.exec())