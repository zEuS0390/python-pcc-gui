from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QTableWidget,
    QAbstractScrollArea, QAbstractItemView,
    QHeaderView, QTableWidgetItem,
    QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

try:
    from db.manager import *
    from db.tables import *
    from src.newclass import NewClass
    from src.selectedclass import SelectedClass
    import rc.resources
except:
    import sys, os
    sys.path.insert(0, os.path.dirname(sys.path[0]))
    from configparser import ConfigParser
    from src.constants import *
    from db.manager import *
    from db.tables import *
    from newclass import NewClass
    from src.selectedclass import SelectedClass
    import rc.resources

class IndexClass(QPushButton):

    def __init__(self, handledclass_id: int, *args, parent=None):
        super(IndexClass, self).__init__(*args, parent)
        self.handledclass_id = handledclass_id

class HandledClasses(QWidget):

    def __init__(self, db, parent=None):
        super(HandledClasses, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.db = db
        self.setup_UI()
        self.destroyed.connect(HandledClasses._on_destroyed)

    @staticmethod
    def _on_destroyed():
        print("Classes instance deleted.")

    def setup_UI(self):
        self.setWindowIcon(QIcon(":/classes.png"))
        self.setWindowTitle("Handled Classes")

        self.mainlayout = QVBoxLayout()
        self.classestablelayout = QVBoxLayout()
        self.tablebtnslayout = QHBoxLayout()

        self.setup_table_btns()
        self.setup_classes_table()

        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())
        self.setMinimumSize(640, 480)

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
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        self.classestable = QTableWidget()
        self.classestable.setFont(font)
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
        self.classestable.setRowCount(0)
        handled_classes = get_handled_classes(self.db)
        self.classestable.setRowCount(len(handled_classes))
        for row, handled_class in enumerate(handled_classes):
            open_btn = IndexClass(handled_class.handledclass_id, "Open")
            archive_btn = IndexClass(handled_class.handledclass_id, "Archive")
            course = QTableWidgetItem("{}-{}".format(handled_class.course.name, handled_class.course.part))
            course.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            schedule = QTableWidgetItem(handled_class.schedule)
            schedule.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            hctime = QTableWidgetItem(handled_class.time)
            hctime.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            days = QTableWidgetItem("{}/{}".format(handled_class.current_session, handled_class.sessions))
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
            open_btn.clicked.connect(self.open_selected_handled_class)
            archive_btn.clicked.connect(self.archive_selected_handled_class)

    def setup_table_btns(self):
        self.tablebtnslayout.addStretch()
        self.btns_conf = {
            "new_class": ("New Class", self.open_new_class),
        }
        self.btns = {}
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Roboto Mono")
        for name, val in self.btns_conf.items():
            btn = QPushButton(val[0])
            btn.setFont(font)
            btn.clicked.connect(val[1])
            self.tablebtnslayout.addWidget(btn)
            self.btns[name] = btn
        self.mainlayout.addLayout(self.tablebtnslayout)

    def open_new_class(self):
        self.newclass = NewClass(self.db)
        self.newclass.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.newclass.switch_window.connect(self.show)
        self.newclass.update_list.connect(self.update_classes_table)
        self.newclass.showMaximized()
        self.hide()
    
    def open_selected_handled_class(self):
        handledclass_id = self.sender().handledclass_id
        self.selectedclass = SelectedClass(handledclass_id, self.db)
        self.selectedclass.switch_window.connect(self.show)
        self.selectedclass.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.selectedclass.showMaximized()
        self.hide()

    def archive_selected_handled_class(self):
        handledclass_id = self.sender().handledclass_id
        delete_handledclass(self.db, handledclass_id)
        self.update_classes_table()

if __name__=="__main__":
    parser = ConfigParser()
    parser.read(APP_CONFIG)
    manager = Manager(parser)
    app = QApplication(sys.argv)
    widget = HandledClasses(manager)
    widget.show()
    sys.exit(app.exec())