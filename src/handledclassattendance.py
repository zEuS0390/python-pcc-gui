from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QVBoxLayout, QTableWidget,
    QAbstractScrollArea, QAbstractItemView,
    QHeaderView, QHBoxLayout,
    QPushButton, QLineEdit,
    QTableWidgetItem
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from db.manager import *
    from db.tables import *
except ModuleNotFoundError:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from constants import APP_CONFIG
    from db.manager import *
    from db.tables import *
    import rc.resources

class IndexAttendance(QPushButton):

    def __init__(self, classattendance_id: int, status: str, *args, parent=None):
        super(IndexAttendance, self).__init__(*args, parent)
        self.status = status
        self.classattendance_id = classattendance_id

class HandledClassAttendance(QWidget):

    switch_window = pyqtSignal()

    def __init__(self, handledclass_id: int, db: Manager, parent=None):
        super(HandledClassAttendance, self).__init__(parent)
        self.handledclass_id = handledclass_id
        self.db = db
        self.session_no = 0
        self.setup_UI()

    def closeEvent(self, event):
        self.switch_window.emit()
        return super().closeEvent(event)

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/"))
        self.setWindowTitle("Class Attendance")
        self.mainlayout = QVBoxLayout()
        self.attendancetablelayout = QVBoxLayout()
        self.navsessionslayout = QHBoxLayout()
        self.setup_navsessions()
        self.setup_attendance_table()
        self.update_current_session()
        self.update_attendance_table()
        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumSize(640, 480)

    def setup_attendance_table(self):
        self.attendancetable = QTableWidget()
        table_headers = {
            "status": "Status",
            "student_name": "Student Name",
            "absent": "",
            "present": "",
            "late": "",
            "excused": "",
            "clear": ""
        }
        font = QFont()
        font.setPointSize(12)
        self.attendancetable = QTableWidget()
        self.attendancetable.setFont(font)
        self.attendancetable.setColumnCount(len(table_headers))
        self.attendancetable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.attendancetable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.attendancetable.horizontalHeader().setStretchLastSection(True)
        self.attendancetable.verticalHeader().setVisible(True)
        self.attendancetable.setAlternatingRowColors(True)
        self.attendancetable.setHorizontalHeaderLabels(table_headers.values())
        self.attendancetable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.attendancetable.verticalHeader().setVisible(False)
        self.attendancetable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.attendancetable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.attendancetable_header = self.attendancetable.horizontalHeader()
        self.attendancetable_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.attendancetable_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.attendancetable_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.attendancetable_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.attendancetablelayout.addWidget(self.attendancetable)
        for row, _ in enumerate(table_headers):
            self.attendancetable_header.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        self.mainlayout.addLayout(self.attendancetablelayout)

    def update_attendance_table(self):
        self.attendancetable.setRowCount(0)
        handledclass = get_handled_class(self.db, self.handledclass_id)
        self.session.setText("{}/{}".format(self.session_no, handledclass.sessions))
        attendances = get_session_attendance_in_class(self.db, self.handledclass_id, self.session_no)
        self.attendancetable.setRowCount(len(attendances))
        row = 0
        for row, attendance in enumerate(attendances):
            status = QTableWidgetItem(attendance.status)
            status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            student_name = QTableWidgetItem("{}, {}".format(attendance.student.lname, "".join([fname[0] for fname in attendance.student.fname.split()])))
            student_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            absent_btn = IndexAttendance(attendance.classattendance_id, "absent", "Absent")
            present_btn = IndexAttendance(attendance.classattendance_id, "present", "Present")
            late_btn = IndexAttendance(attendance.classattendance_id, "late", "Late")
            excused_btn = IndexAttendance(attendance.classattendance_id, "excused", "Excused")
            clear_btn = IndexAttendance(attendance.classattendance_id, "", "Clear")
            self.attendancetable.setItem(row, 0, status)
            self.attendancetable.setItem(row, 1, student_name)
            self.attendancetable.setCellWidget(row, 2, absent_btn)
            self.attendancetable.setCellWidget(row, 3, present_btn)
            self.attendancetable.setCellWidget(row, 4, late_btn)
            self.attendancetable.setCellWidget(row, 5, excused_btn)
            self.attendancetable.setCellWidget(row, 6, clear_btn)
            absent_btn.clicked.connect(self.set_attendance_status)
            present_btn.clicked.connect(self.set_attendance_status)
            late_btn.clicked.connect(self.set_attendance_status)
            excused_btn.clicked.connect(self.set_attendance_status)
            clear_btn.clicked.connect(self.set_attendance_status)
            row += 1

    def set_attendance_status(self):
        indexattendance = self.sender()
        classattendance_id = indexattendance.classattendance_id
        status = indexattendance.status
        update_class_attendance_status(self.db, classattendance_id, status)
        self.update_attendance_table()

    def setup_navsessions(self):
        font = QFont()
        font.setPointSize(12)
        self.back_btn = QPushButton("<< BACK")
        self.back_btn.setFont(font)
        self.back_btn.clicked.connect(self.back_session)
        self.session = QLineEdit()
        self.session.setFont(font)
        self.session.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session.setReadOnly(True)
        self.next_btn = QPushButton("NEXT >>")
        self.next_btn.setFont(font)
        self.next_btn.clicked.connect(self.next_session)
        self.navsessionslayout.addWidget(self.back_btn)
        self.navsessionslayout.addStretch()
        self.navsessionslayout.addWidget(self.session)
        self.navsessionslayout.addStretch()
        self.navsessionslayout.addWidget(self.next_btn)
        self.mainlayout.addLayout(self.navsessionslayout)

    def update_current_session(self):
        handledclass = get_handled_class(self.db, self.handledclass_id)
        self.session_no = handledclass.current_session

    def next_session(self):
        handledclass = get_handled_class(self.db, self.handledclass_id)
        if self.session_no < handledclass.sessions:
            self.session_no += 1
            update_handledclass_current_session(self.db, self.handledclass_id, self.session_no)
            self.update_attendance_table()

    def back_session(self):
        if self.session_no > 1:
            self.session_no -= 1
            update_handledclass_current_session(self.db, self.handledclass_id, self.session_no)
            self.update_attendance_table()


if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = HandledClassAttendance(manager)
    widget.show()
    sys.exit(app.exec())
