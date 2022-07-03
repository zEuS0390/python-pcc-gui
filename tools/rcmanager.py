from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QVBoxLayout, QLineEdit,
    QFileDialog, QPushButton,
    QListWidget, QListWidgetItem,
    QMessageBox
)
from configparser import ConfigParser
import os, sys, shutil, subprocess
sys.path.insert(0, os.path.dirname(sys.path[0]))

# This function will get all files from a specified resource directory
def getfiles(rcpath):
    with open(rcpath, "r") as file:
        c = file.read()
    l = c.split("<qresource>")
    nl = l[1].split("</qresource>")   
    rcf = [f.strip() for f in nl[0].split("\n")]
    for index, item in enumerate(rcf):
        if len(item) == 0:
            rcf.remove('')
    for index, item in enumerate(rcf):
        i = item.find("\"")+1
        l = item.find("\">")
        rcf[index] = item[i:l]
    return rcf

# This function will insert a new resource file
def insert(rcpath, alias, imgpath):
    with open(rcpath, "r") as file:
        c = file.read()
    l = c.split("<qresource>")
    nl = l[1].split("</qresource>")   
    rcf = [f.strip() for f in nl[0].split("\n")]
    for item in rcf:
        if len(item) == 0:
            rcf.remove('')
    entry = "<file alias=\"%s\">%s</file>"
    rcf.append(entry %(alias, imgpath))
    rcf = ["\n\t\t" + f for f in rcf]
    with open(rcpath, "w") as file:
        file.write("".join(l[0]).strip()+"\n\t<qresource>"+"".join(rcf)+"\n\t</qresource>"+"".join(nl[1]))

# Resource Manager Widget
class RCManager(QWidget):

    def __init__(self, parser: ConfigParser, parent=None):
        super(RCManager, self).__init__(parent)
        self.parser = parser
        self.setup_UI()

    def setup_UI(self):
        self.setWindowTitle("Resource Manager")
        self.mainlayout = QVBoxLayout()
        self.open_btn = QPushButton("INSERT")
        self.compile_btn = QPushButton("COMPILE")
        self.file_list = QListWidget()
        self.updateList()
        self.mainlayout.addWidget(self.file_list)
        self.mainlayout.addWidget(self.open_btn)
        self.mainlayout.addWidget(self.compile_btn)
        self.open_btn.clicked.connect(self.insertFile)
        self.compile_btn.clicked.connect(self.compileFile)
        self.setLayout(self.mainlayout)
        self.resize(self.mainlayout.sizeHint())

    def insertFile(self):
        _path, _type = QFileDialog.getOpenFileName()
        try:
            if len(_path) > 0:
                ret = shutil.copy2(_path, os.path.join(self.parser.get("image", "folder"), os.path.basename(_path)))
                insert("rc/resources.qrc", os.path.basename(ret), os.path.join("..", "img", os.path.basename(ret)).replace("\\", "/"))
                self.updateList()
        except:
            print("Error encountered!")

    def compileFile(self):
        subprocess.call([
            "pyrcc5", 
            "-o", 
            os.path.join(self.parser.get("rc", "folder"), "%s.py" %(self.parser.get("rc", "name"))),
            os.path.join(self.parser.get("rc", "folder"), "%s.qrc" %(self.parser.get("rc", "name")))]
        )
        message = QMessageBox()
        message.setIcon(QMessageBox.Icon.Information)
        message.setWindowTitle("Compile")
        message.setText("Successfully compiled!")
        message.setStandardButtons(QMessageBox.StandardButton.Ok)
        message.exec()

    def updateList(self):
        self.file_list.clear()
        files = getfiles(os.path.join(self.parser.get("rc", "folder"), "%s.qrc" %(self.parser.get("rc", "name"))))
        for n in files:
            self.file_list.addItem(QListWidgetItem(n))

# Run the application here since this is separate from the main application
if __name__=="__main__":
    parser = ConfigParser()
    parser.read("cfg/rc.cfg")
    app = QApplication(sys.argv)
    widget = RCManager(parser)
    widget.show()
    sys.exit(app.exec())