import requests
from bs4 import BeautifulSoup

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

from PyQt5.QtCore import *

class MyWindow(QMainWindow):

    def __init__(self, stock_code):
        super().__init__()

        self.time = 0
        self.code = stock_code

        self.setWindowTitle("Stock Checker")
        self.setGeometry(100,100,180,50)

        self.label = QLabel("Now : ",self)
        self.label.move(10,20)

        self.timeVar = QTimer()
        self.timeVar.setInterval(3000)
        self.timeVar.timeout.connect(self.stock_check)
        self.timeVar.start()

    def stock_check(self): 
        url = "https://finance.naver.com/item/main.nhn?code="+self.code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        
        no_today = bs_obj.find("p", {"class": "no_today"}) # 태그 p, 속성값 no_today 찾기
        blind = no_today.find("span", {"class": "blind"}) # 태그 span, 속성값 blind 찾기now_price = blind.text

        #now_price = blind.text.replace(',',"'h")
        now_price = blind.text
        self.label.setText('Now : '+now_price)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow(sys.argv[1])
    myWindow.show()
    app.exec_()