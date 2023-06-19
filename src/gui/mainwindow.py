# This Python file uses the following encoding: utf-8
import sys, os
import csv
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QAbstractTableModel


#다른 코드들 import

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from scrap.scrap_init import run_crawling


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from gui.ui_form import Ui_MainWindow
filePath = "src/csvEdit/forTestFiles/cleaned.csv"

# CSV 데이터 저장형식 클래스
class CSVTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data_list = data

    def rowCount(self, parent):
        return len(self.data_list)

    def columnCount(self, parent):
        return len(self.data_list[0]) if self.data_list else 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data_list[row][col])
        return None

# 주 윈도우 클래스
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 검색버튼을 클릭할때 함수 실행
        self.ui.search_button.clicked.connect(self.initSearch)
    # 검색버튼 눌러질때 실행되는 함수
    def initSearch(self):
        #키워드 전달하기
        processCount = int(self.ui.multiProcess.currentText()) #multiProcess 콤보박스 오브젝트에서 값 가져오기
        keyword = self.ui.search_keyword_lineEdit.text() # search_keyword_lineedit 오브젝트에서 값 가져오기
        
        # 키워드 잘 가져오는지 디버깅용 출력
        print(keyword, processCount)
        

        #크롤러 실행
        run_crawling(keyword, processCount)

        # Read CSV file and retrieve the data (csv 출력 테스트용)
        data = []
        with open(filePath, 'r', encoding='cp949') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)

        # Create a model and set it to the table view
        model = CSVTableModel(data)
        self.ui.ShowingCSV.setModel(model)

#함수화

def initGUI():
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        widget = MainWindow()
        widget.show()
        sys.exit(app.exec())
    else:
        app = QApplication(sys.argv)
        widget = MainWindow()
        widget.show()
        sys.exit(app.exec())
