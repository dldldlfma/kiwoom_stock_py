import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 550)

        label = QLabel('종목 코드 : ', self)
        label.move(20,20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80,20)
        self.code_edit.setText("005930") #삼성전자 005930 // 키움증권 039490 // 하이닉스 000660

        btn1 = QPushButton("조회", self)
        btn1.move(190,20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10,60,280,180)
        self.text_edit.setEnabled(False)

        #-------------------------------------------------------

        btn2 = QPushButton("계좌 얻기", self)
        btn2.move(190,260)
        btn2.clicked.connect(self.btn2_clicked)

        self.text_edit2 = QTextEdit(self)
        self.text_edit2.setGeometry(10,300,280,180)
        self.text_edit2.setEnabled(False)
        #--------------------------------------------------------
    
    def event_connect(self, err_code):
        if err_code ==0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append("종목코드 : " +code)

        #SetInpuValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",code)

        #CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001",0,"0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_coe, msg1, msg2):
        if rqname =="opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            price = self.kiwoom.dynamicCall("CommGetData(QString, QSTring, QString, int, QString)",trcode, "", rqname, 0, "현재가")

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())
            self.text_edit.append("현재가: " + price.strip())

    def btn2_clicked(self):
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        user_id = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_ID"])
        user_name = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_NAME"])
        self.text_edit2.append("계좌번호 : " +account_num.rstrip(';'))
        self.text_edit2.append("사용자ID : " +user_id.rstrip(';'))
        self.text_edit2.append("사용자이름 : " +user_name.rstrip(';'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()