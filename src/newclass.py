from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QLineEdit,
    QLabel, QHBoxLayout,
    QComboBox, QTableWidget,
    QAbstractItemView, QAbstractScrollArea,
    QHeaderView, QPushButton,
    QTableWidgetItem
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import logging

try:
    from db.manager import *
    from db.tables import *
    from src.addstudent import AddStudent
    from src.constants import *
    import rc.resources
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import *
    from db.manager import *
    from db.tables import *
    from src.addstudent import AddStudent
    import rc.resources

class IndexButton(QPushButton):

    def __init__(self, id, *args, parent=None):
        super(IndexButton, self).__init__(*args, parent)
        self.id = id
        self.destroyed.connect(IndexButton._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("IndexButton instance deleted.")


class NewClass(QWidget):

    switch_window = pyqtSignal()
    update_list = pyqtSignal()

    def __init__(self, db: Manager, parent=None):
        super(NewClass, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(NewClass._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("NewClass instance deleted.")

    def closeEvent(self, event):
        self.switch_window.emit()
        return super().closeEvent(event)

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/add_class.png"))
        self.setWindowTitle("Add New Class")

        self.mainlayout = QVBoxLayout()
        self.inputslayout = QHBoxLayout()
        self.studentstablelayout = QVBoxLayout()
        self.tablectrllayout = QHBoxLayout()
        self.btnslayout = QHBoxLayout()

        self.setup_inputs()
        self.setup_table_ctrl()
        self.setup_students_table()
        self.setup_btns()

        self.setLayout(self.mainlayout)

        self.resize(640, 480)

    def setup_inputs(self):
        self.inputs_conf = {
            "course": ("Course:", QComboBox),
            "schedule": ("Schedule:", QLineEdit),
            "time": ("Time:", QLineEdit),
            "sessions": ("Sessions:", QLineEdit),
        }
        self.inputs = {}
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        for name, val in self.inputs_conf.items():
            inputvlayout = QVBoxLayout()
            obj = None
            label = QLabel(val[0])
            label.setFont(font)
            if val[1] == QLineEdit:
                obj = val[1]()
                obj.setFont(font)
            elif val[1] == QComboBox:
                obj = val[1]()
                obj.setFont(font)
            inputvlayout.addWidget(label)
            inputvlayout.addWidget(obj)
            self.inputslayout.addLayout(inputvlayout, 25)
            self.inputs[name] = (label, obj)
        self.mainlayout.addLayout(self.inputslayout)
        self.update_combobox()

    def setup_table_ctrl(self):
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        table_title = QLabel("List of Students")
        table_title.setFont(font)
        self.import_students_btn = QPushButton("Import Students")
        self.import_students_btn.setFont(font)
        self.add_student_btn = QPushButton("Add Student")
        self.add_student_btn.setFont(font)
        self.add_student_btn.clicked.connect(self.add_student)
        self.tablectrllayout.addWidget(table_title)
        self.tablectrllayout.addStretch()
        self.tablectrllayout.addWidget(self.import_students_btn)
        self.tablectrllayout.addWidget(self.add_student_btn)
        self.mainlayout.addLayout(self.tablectrllayout)

    def setup_students_table(self):
        self.student_ids = []
        self.students_in_table = []
        table_headers = {
            "fname": "First Name",
            "mname": "Middle Name",
            "lname": "Last Name",
            "gender": "Gender",
            "age": "Age",
            "actions": "Actions"
        }
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        self.studentstable = QTableWidget()
        self.studentstable.setFont(font)
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

    def setup_btns(self):
        self.btns_conf = {
            "cancel": ("Cancel", self.close),
            "submit": ("Submit", self.add)
        }
        self.btns = {}
        self.btnslayout.addStretch()
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.setFont(font)
            btn.clicked.connect(val[1])
            self.btnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.btnslayout)

    def add_student(self):
        self.addstudent = AddStudent(self.db)
        self.addstudent.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.addstudent.update_table.connect(self.update_student_table)
        self.addstudent.showMaximized()

    def update_student_table(self, added_student_id: int):
        if added_student_id not in self.student_ids:
            self.student_ids.append(added_student_id)

        if added_student_id not in self.students_in_table:
            self.students_in_table.append(added_student_id)
            student = get_student(self.db, added_student_id)
            if student is not None:
                row = self.studentstable.rowCount()
                self.studentstable.setRowCount(row+1)
                delaction = IndexButton(added_student_id, "Delete")
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
                self.studentstable.setItem(row, 3, age)
                self.studentstable.setItem(row, 4, gender)
                self.studentstable.setCellWidget(row, 5, delaction)
                delaction.clicked.connect(self.delete_added_student)

    def delete_added_student(self):
        sender_id = self.sender().id
        self.student_ids.remove(sender_id)
        self.students_in_table.clear()
        self.studentstable.setRowCount(0)
        for student_id in self.student_ids:
            self.update_student_table(student_id)

    def update_combobox(self):
        self.inputs["course"][1].clear()
        courses = ["{}-{}".format(course.name, course.part) for course in get_courses(self.db)]
        self.inputs["course"][1].addItems(courses)

    def add(self):
        add_handled_class(
            self.db,
            course_name=self.inputs["course"][1].currentText().split("-")[0],
            course_part=self.inputs["course"][1].currentText().split("-")[1],
            student_ids=self.student_ids,
            sessions=int(self.inputs["sessions"][1].text()),
            schedule=self.inputs["schedule"][1].text(),
            time=self.inputs["time"][1].text()
        )
        self.update_list.emit()
        self.close()

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = NewClass(manager)
    widget.show()
    sys.exit(app.exec())