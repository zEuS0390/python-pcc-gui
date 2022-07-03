from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QListWidget,
    QListWidgetItem, QHBoxLayout,
    QPushButton
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from db.manager import *
    from db.tables import *
    from src.newstudent import NewStudent
    import rc.resources
except ModuleNotFoundError:
    import os, sys
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from src.constants import *
    from db.manager import *
    from db.tables import *
    from src.newstudent import NewStudent
    import rc.resources

class AddStudent(QWidget):

    update_table = pyqtSignal(int)

    def __init__(self, db: Manager, parent=None):
        super(AddStudent, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/add_student.png"))
        self.setWindowTitle("Add Student")
        self.mainlayout = QVBoxLayout()
        self.studentslistlayout = QVBoxLayout()
        self.btnslayout = QHBoxLayout()
        self.setup_students_list()
        self.setup_btns()
        self.setLayout(self.mainlayout)

    def setup_students_list(self):
        font = QFont()
        font.setPointSize(12)
        self.student_ids = []
        self.studentslist = QListWidget()
        self.studentslist.setFont(font)
        students = get_students(self.db)
        for student in students:
            item = QListWidgetItem(QIcon(":/new_student.png"),
                "{lname}, {fname}, {mname} - {age}".format(
                    lname = student.lname, 
                    fname = student.fname,
                    mname = student.mname,
                    age = student.age
                )
            )
            self.studentslist.addItem(item)
            self.student_ids.append(student.student_id)
        self.studentslistlayout.addWidget(self.studentslist)
        self.mainlayout.addLayout(self.studentslistlayout)

    def setup_btns(self):
        font = QFont()
        font.setPointSize(12)
        self.new_btn = QPushButton("New")
        self.new_btn.setFont(font)
        self.new_btn.clicked.connect(self.open_new_student)
        self.btnslayout.addWidget(self.new_btn)
        self.btnslayout.addStretch()
        self.btns_conf = {
            "cancel": ("Cancel", self.close),
            "submit": ("Add", self.add)
        }
        self.btns = {}
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.setFont(font)
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def add(self):
        student_id = self.student_ids[self.studentslist.currentRow()]
        self.update_table.emit(student_id)
        self.close()

    def open_new_student(self):
        self.new_student = NewStudent(self.db)
        self.new_student.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.new_student.update_list.connect(self.update_list)
        self.new_student.show()

    def update_list(self):
        self.student_ids.clear()
        self.studentslist.clear()
        students = get_students(self.db)
        for student in students:
            item = QListWidgetItem(QIcon(":/new_student.png"),
                "{lname}, {fname}, {mname} - {age}".format(
                    lname = student.lname, 
                    fname = student.fname,
                    mname = student.mname,
                    age = student.age
                )
            )
            self.studentslist.addItem(item)
            self.student_ids.append(student.student_id)

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = AddStudent(manager)
    widget.show()
    sys.exit(app.exec())