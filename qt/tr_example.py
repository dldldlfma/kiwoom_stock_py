import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pprint import pprint

import matplotlib.pyplot as plt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        self.remained_data = None

        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 800, 550)

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
        
        btn3 = QPushButton("종목 코드 얻기", self)
        btn3.move(490,20)
        btn3.clicked.connect(self.btn3_clicked)

        self.code_listWidget = QListWidget(self)
        self.code_listWidget.setGeometry(310,60,280,450)        

        self.code_listWidget.itemDoubleClicked.connect(self.stock_code_list_double_click) #double click 신호가 오면 사용
        #--------------------------------------------------------
        btn4 = QPushButton("종목 일봉 얻기", self)
        btn4.move(610,20)
        btn4.clicked.connect(self.take_day_graph)

        #--------------------------------------------------------
    
    def event_connect(self, err_code):
        if err_code ==0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self): #종목 코드에 따른 데이터 확인 
        code = self.code_edit.text()
        self.text_edit.append("종목코드 : " +code)

        #SetInpuValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",code)
        #CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001",0,"0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_coe, msg1, msg2):
        if(prev_next =='2'):
            self.remained_data =True
        else:
            self.remained_data = False

        if(rqname =="opt10001_req"):
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            price = self.kiwoom.dynamicCall("CommGetData(QString, QSTring, QString, int, QString)",trcode, "", rqname, 0, "현재가")

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())
            self.text_edit.append("현재가: " + price.strip())
            self.text_edit.append("\n")
        
        elif(rqname =="opt10081_req"):#일일시세 확인이라면
            data_cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)#얼마나 반복해서 읽어야 하는지 확인하고
            
            date_list=[]
            close_price_list=[]

            for i in range(data_cnt):
                date = self._comm_get_data(trcode, "", rqname, i, "일자")
                open = self._comm_get_data(trcode, "", rqname, i, "시가")
                high = self._comm_get_data(trcode, "", rqname, i, "고가")
                low = self._comm_get_data(trcode, "", rqname, i, "저가")
                close = self._comm_get_data(trcode, "", rqname, i, "현재가")
                volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
                date_list.append(date[2:])
                close_price_list.append(int(close))
                #print(date, open, high, low, close, volume)
            
            
            date_list.reverse()
            close_price_list.reverse()

            short_date = []
            short_close = []
            for i in range(data_cnt):
                if(i % 10 ==0):
                    short_date.append(date_list[i])
                    short_close.append(close_price_list[i])

            for i in range(len(short_date)):
                print(short_date[i],short_close[i])
                #print(type(date_list[i]),type(close_price_list[i]))

            plt.figure()
            plt.plot(short_date,short_close)
            plt.xticks(rotation=90)

            plt.show()

        


    def btn2_clicked(self): #로그인 정보 확인
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        user_id = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_ID"])
        user_name = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["USER_NAME"])
        self.text_edit2.append("계좌번호 : " +account_num.rstrip(';'))
        self.text_edit2.append("사용자ID : " +user_id.rstrip(';'))
        self.text_edit2.append("사용자이름 : " +user_name.rstrip(';'))

    def btn3_clicked(self): # 종목코드 호출
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
            kospi_code_name_list.append(x + " : " + name)

        self.code_listWidget.addItems(kospi_code_name_list)
    
    def stock_code_list_double_click(self):
        selected_stock_code=self.code_listWidget.selectedItems().pop().text()[0:6] #QListWidget에서 선택된 값의 stock code부분만 추출
        self.code_edit.setText(selected_stock_code)
        self.btn1_clicked()
        
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()
    
    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
    
    def take_day_graph(self):
        code = self.code_edit.text()
        rqname = "opt10081_req"
        
        #SetInpuValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",code)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기준일자","20200117")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분",1)
        
        #CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, "opt10081",0,"0101")

        while self.remained_data == True:
            time.sleep(0.2)
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",code)
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기준일자","20200117")
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분",1)
        
            #CommRqData
            self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, "opt10081",2,"0101")

        

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()