import sys
from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from UserData import data
import configparser
from dadata import Dadata
import subprocess
from main import start

myarr = []

class APP(QtWidgets.QMainWindow):
    def __init__(self):
        super(APP, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.pulSpecialization()
        self.btnAllClick()
        self.btnCityClick()
        self.btnSearch()

    def init_UI(self):
        self.setWindowTitle("Парсер")
        text = self.ui.lineEdit.text()

    def pulSpecialization(self):
        self.ui.comboSpec.addItem("")
        for item in data:
            for key in item.keys():
                self.ui.comboSpec.addItem(key)

    def btnSearch(self):
        self.ui.pushButton.clicked.connect(self.clickedbtnSearch)

    def clickedbtnSearch(self):
        self.ui.listWidget.clear()
        if (self.ui.comboSpec.itemText(self.ui.comboSpec.currentIndex()) != ""):
            text = self.ui.lineEdit.text()
            print(text)
            token = "4c7aad934821b04d2f914b0e8e3bd51864197591"
            dadata = Dadata(token)
            result = dadata.suggest("address", text)
            print(result[0]['data']['city'])
            for res in result:
                if (res['data']['city'] == text):
                    self.ui.listWidget.addItem(res['unrestricted_value'])
                    myarr.append(res['data']['postal_code'])


    def btnCityClick(self):
        self.ui.btnParseCity.clicked.connect(self.clickedbtnCity)

    def clickedbtnCity(self):
        if (self.ui.listWidget.currentItem()):
            if (self.ui.comboSpec.itemText(self.ui.comboSpec.currentIndex()) != ""):
                for item in data[self.ui.comboSpec.currentIndex() - 1].values():
                    config = configparser.ConfigParser()
                    config.read('MyData.ini')
                    config.set('Link', 'spec', item)
                    config.set('Link', 'index', myarr[self.ui.listWidget.currentRow()])
                    myarr.clear()
                    with open('MyData.ini', 'w') as configfile:
                        config.write(configfile)
                        self.Message("Идёт парсинг, пожалуйста ждите!")
            if(start()):
                #subprocess.call("main.py", shell=True)
                self.Message("Не найдено информации!")
            else:
                self.Message("Информация была успешно спарсена, откройте EXCEL файл!")

    def btnAllClick(self):
        self.ui.btnParseAll.clicked.connect(self.clicked)

    def clicked(self):
        if (self.ui.comboSpec.itemText(self.ui.comboSpec.currentIndex()) != ""):
            for item in data[self.ui.comboSpec.currentIndex() - 1].values():
                config = configparser.ConfigParser()
                config.read('MyData.ini')
                config.set('Link', 'spec', item)
                config.set('Link', 'index', '')
                with open('MyData.ini', 'w') as configfile:
                    config.write(configfile)
                    self.Message("Идёт парсинг, пожалуйста ждите!")
            if (start()):
                # subprocess.call("main.py", shell=True)
                self.Message("Не найдено информации!")
            else:
                self.Message("Информация была успешно спарсена, откройте EXCEL файл!")

    def Message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Сообщение")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = APP()
    application.show()
    sys.exit(app.exec_())