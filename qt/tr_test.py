import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from pprint import pprint

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 400, 550)

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

        
    def event_connect(self, err_code):
        if err_code ==0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self): #종목 코드에 따른 데이터 확인 
        code = self.code_edit.text()
        self.text_edit.append("종목코드 : " +code)

        #SetInpuValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",code)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기준일자",20191201)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분",'1')

        #CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10081_req", "opt10081","0","0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_coe, msg1, msg2):
        if rqname == "opt10081_req":
            print(rqname)
            value = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "화면번호")
            print(dir(value))
            print(type(value))
            print(value)
            for i in value:
                print(i)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()