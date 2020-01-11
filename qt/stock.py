import sys
from PyQt5.QtWidgets import *

from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300,300,300,150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPIctrl.1")
        
        b1_login = QPushButton("Login", self)
        b1_login.move(20,20)
        b1_login.clicked.connect(self.b1_login_clicked)

        b2_login = QPushButton("Check state", self)
        b2_login.move(20,70)
        b2_login.clicked.connect(self.b2_login_clicked)
    
    def b1_login_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        #QMessageBox.about(self, "message", "clicked")

    def b2_login_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") ==0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")
        #QMessageBox.about(self, "message", "clicked2")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()