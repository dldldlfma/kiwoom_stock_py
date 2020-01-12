import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget_example") #우리가 만들 GUI Window의 이름을 설정해줌 
        self.setGeometry(300, 300, 300, 550)  #우리가 만들 GUI Window의 크기를 설정

        label = QLabel('값 : ', self) #QLabel은 별도의 설정이 불가능한 그냥 Label을 붙이는 것
        label.move(20,20) # 전체 윈도우 (0,0)을 기준으로 (20,20)에 위치 시킨다.

        self.code_edit = QLineEdit(self) #QLineEdit이라는 작은 텍스트상자 선언
        self.code_edit.move(80,20) #code_edit이라는 이름으로 선언한 QLineEdit의 위치를 설정 왼쪽 상단이 (0, 0)인것을 기준으로 오른쪽으로 80 픽셀 아래쪽으로 20 픽셀 이동한 곳에 위치 시킨다.
        self.code_edit.setText("init") #code_edit의 초기값을 적어준다.
        self.code_edit.returnPressed.connect(self.btn_clicked)#returnPressed.connect(함수) QLineEdit이라는 Widget에서 Enter를 누른것이 감지 되었을때 (함수)를 동작시킨다
        
        btn = QPushButton("값 추가", self) #QPushButton이라는 버튼을 추가한다. 
        btn.move(180,20) #버튼의 위치를 (180, 20)에 위치시킨다.

        btn.clicked.connect(self.btn_clicked)

        self.code_listWidget = QListWidget(self)
        self.code_listWidget.setGeometry(20,60,240,450)        
        self.code_listWidget.itemDoubleClicked.connect(self.list_item_double_click) #double click 신호가 오면 사용
        #--------------------------------------------------------
    
    
    def btn_clicked(self):
        if(self.code_edit.text() != ""): #code_edit안에 적혀 있는 값이 공백이 아니라면
            self.code_listWidget.addItem(self.code_edit.text()) #code_exit 안에 적혀 있는 값을 추가 
            self.code_edit.setText("") #추가한뒤 다시 code_edit을 공백으로 변경 
    
    def list_item_double_click(self):
        selected_value=self.code_listWidget.selectedItems().pop().text()[0:6] #QListWidget에서 선택된 값의 stock code부분만 추출
        print(selected_value) #print로 선택된 값을 출력
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()