from PyQt5 import uic, QtWidgets
import mysql.connector
import platform
#from reportlab.pdfgen import canvas

""" 



Author: Gerssivaldo Oliveira dos Santos

Contacts: 

https://github.com/andows159

https://www.linkedin.com/in/gerssivaldo-santos-a75921130

Note:
    The function of generating pdf of the table is still under development.
    The software is in constant updating.
 """

class EnterpriseManager():

    def __init__(self):
        #verify OS

        self.os = platform.system()
        print(self.os)

        #login mysql

        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="andows",
        )
        #create database if not exists

        cursor = self.database.cursor()
        create_database_command = "CREATE DATABASE IF NOT EXISTS enterprise_manager;"
        cursor.execute(create_database_command)
        self.database.commit()
        cursor.execute("use enterprise_manager;")
        self.database.commit()
        create_table_command = "CREATE TABLE IF NOT EXISTS produtos(id INT NOT NULL AUTO_INCREMENT, produto VARCHAR(50), descricao VARCHAR(70), preco_compra DOUBLE, preco_venda DOUBLE, radio_button VARCHAR(50), check_box VARCHAR(150), liquido DOUBLE, PRIMARY KEY(id));"
        cursor.execute(create_table_command)
        self.database.commit()
        #connect tp database
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="andows",
            database="enterprise_manager"
        )

        #QT instances
        app = QtWidgets.QApplication([])
        self.register_screen()
        app.exec()
      

    def login_screen(self):
        if self.os == "Windows":
            self.login_screen = uic.loadUi(r".\screens\login.ui")
        elif self.os == "Linux":
            self.login_screen = uic.loadUi("./screens/login.ui")
        self.login_screen.login_button.clicked.connect(self.menu_screen)
        self.login_screen.create_button.clicked.connect(self.create_screen)
        self.login_screen.show()

    def create_screen(self):
        if self.os == "Windows":
            self.create_screen = uic.loadUi(r".\screens\create.ui")
        elif self.os == "Linux":
            self.create_screen = uic.loadUi("./screens/create.ui")
        self.create_screen.show()

    def menu_screen(self):
        if self.os == "Windows":
            self.menu_screen = uic.loadUi(r".\screens\menu.ui")
        if self.os == "Linux":
            self.menu_screen = uic.loadUi("./screens/menu.ui")
        self.menu_screen.register_screen.clicked.connect(self.register_screen)
        self.menu_screen.control_screen.clicked.connect(self.control_screen)
        self.menu_screen.show()
   
    def register_screen(self):
        if self.os == "Windows":
            self.register_screen = uic.loadUi(r".\screens\register_products.ui")
        elif self.os == "Linux":
            self.register_screen = uic.loadUi("./screens/register_products.ui")
        self.register_screen.show()
        self.register_screen.register_button.clicked.connect(self.register_button)
        self.register_screen.control_screen.clicked.connect(self.control_screen)

    def control_screen(self):
        if self.os == "Windows":
            self.control_screen = uic.loadUi(r".\screens\control_screen.ui")
        elif self.os == "Linux":
            self.control_screen = uic.loadUi("./screens/control_screen.ui")
        self.control_screen.rm_button.clicked.connect(self.rm_buttom)
        self.control_screen.refresh_button.clicked.connect(self.refresh_button)
        self.control_screen.show()
  
        cursor = self.database.cursor()
        select = "SELECT * FROM produtos"
        cursor.execute(select)
        self.view_data = cursor.fetchall()
        self.control_screen.tableWidget.setRowCount(len(self.view_data))
        self.control_screen.tableWidget.setColumnCount(8)

        #ler a matriz
        for linha in range(0,len(self.view_data)): #para percorrendo as linhas
            for item in range(0,8): #dentro das linhas pegando os itens ao cruzar com as colunas
                self.control_screen.tableWidget.setItem(linha,item,QtWidgets.QTableWidgetItem(str(self.view_data[linha][item])))



    def rm_buttom(self):
      
    
        cursor = self.database.cursor()
        truncate = "TRUNCATE TABLE produtos;"
        cursor.execute(truncate)
        select = "SELECT * FROM produtos"
        cursor.execute(select)
        self.view_data = cursor.fetchall()
        self.control_screen.tableWidget.setRowCount(len(self.view_data))
        self.control_screen.tableWidget.setColumnCount(8)
        self.control_screen.show()

    def refresh_button(self):
        cursor = self.database.cursor()
        select = "SELECT * FROM produtos"
        cursor.execute(select)
        self.view_data = cursor.fetchall()
        self.control_screen.tableWidget.setRowCount(len(self.view_data))
        self.control_screen.tableWidget.setColumnCount(8)
        for linha in range(0,len(self.view_data)): #traversing the lines
            for item in range(0,8): #inside the lines picking up the items when crossing the columns
                self.control_screen.tableWidget.setItem(linha,item,QtWidgets.QTableWidgetItem(str(self.view_data[linha][item])))
        self.control_screen.show()

    def login_button(self):
        self.register_screen()
          
    def register_button(self):
        
        input_description = self.register_screen.input_description.text()
        
        input_product = self.register_screen.input_product.text()
        
        input_sell_price = float(self.register_screen.input_sell_price.text())
        
        input_buy_price = float(self.register_screen.input_buy_price.text())

        liquido = float(input_sell_price - input_buy_price)

        if self.register_screen.radioButton.isChecked():
            radio_option = "Ração pura"
        elif self.register_screen.radioButton_2.isChecked():
            radio_option = "Formulação própria"
        elif self.register_screen.radioButton_4.isChecked():
            radio_option = "Medicamentos"
        elif self.register_screen.radioButton_5.isChecked():
            radio_option = "Formulação indústrial"
        elif self.register_screen.radioButton_6.isChecked():
            radio_option = "Outros produtos"
        else:
            radio_option = ""
        
        check_option = []
        
        if self.register_screen.checkBox.isChecked():
            check_option.append("Aves")
        if self.register_screen.checkBox_2.isChecked():
            check_option.append("Bovinos")
        if self.register_screen.checkBox_3.isChecked():
            check_option.append("Ovinos")
        if self.register_screen.checkBox_4.isChecked():
            check_option.append("Caprinos")
        if self.register_screen.checkBox_5.isChecked():
            check_option.append("Suínos")
        if self.register_screen.checkBox_7.isChecked():
            check_option.append("Uso geral")
        
        check_option = "/".join(check_option)
        #input_amount = self.register_screen.input_amount.text()
    
        cursor = self.database.cursor()
        insert_into = f'INSERT INTO produtos (produto, descricao, preco_compra, preco_venda, radio_button, check_box, liquido) VALUES {input_product,input_description,input_buy_price,input_sell_price,radio_option,check_option, liquido}'
        print(insert_into)
        cursor.execute(insert_into)
        self.database.commit()

        if self.register_screen.checkBox_6.isChecked() == False:
            self.register_screen.input_product.setText("")
            self.register_screen.input_description.setText("")
            self.register_screen.input_buy_price.setValue(0)
            self.register_screen.input_sell_price.setValue(0)


instance = EnterpriseManager()
