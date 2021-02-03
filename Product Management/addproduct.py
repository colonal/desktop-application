import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3, os
from PIL import Image

pathDB = os.environ['APPDATA']

con = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
cur = con.cursor()
defaultImg = "store.png"

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layout()

    def widgets(self):
        # ########################### widget of top layout ###########
        self.addProductImg = QLabel()
        self.img = QPixmap('icons/addproduct.png')
        self.addProductImg.setPixmap(self.img)
        self.titleText = QLabel("Add Product")
        # ########################### widget of Buttom layout ########
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of product")
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setPlaceholderText("Enter name of maunfacturer")
        self.priceEntry = QLineEdit()
        self.priceEntry.setPlaceholderText("Enter qouta of product")
        self.qoutaEntry = QLineEdit()
        self.qoutaEntry.setPlaceholderText("Enter qouta of product")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.buttomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.buttomFrame = QFrame()
        # ################## add widgets ##################
        # ################## widget of toplayut############
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        # ################## widgets of form layout ########
        self.buttomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.buttomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.buttomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.buttomLayout.addRow(QLabel("Qouta: "), self.qoutaEntry)
        self.buttomLayout.addRow(QLabel("Upload: "), self.uploadBtn)
        self.buttomLayout.addRow(QLabel(""), self.submitBtn)
        self.buttomFrame.setLayout(self.buttomLayout)
        
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttomFrame)

        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size = (256, 255)

        self.filename, ok = QFileDialog.getOpenFileName(self,"Upload Image", "","Image Files (*.jpg *.png)")  
        if ok:
            print(self.filename)
            defaultImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))
            self.img = QPixmap("img/{0}".format(defaultImg))
            self.addProductImg.setPixmap(self.img)

    def addProduct(self):
        global defaultImg

        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = self.priceEntry.text()
        qouta = self.qoutaEntry.text()

        if (name and manufacturer and price and price and qouta !=""):
            try:
                query = "INSERT INTO Products(product_Name ,product_Mamufachturer,product_price, product_qouta,product_img)VALUES(?,?,?,?,?)"
                cur.execute(query,(name, manufacturer, price, qouta, defaultImg))
                con.commit()
                QMessageBox.information(self,"Into","Product has been added")
                #con.close()
                self.nameEntry.setText("")
                self.manufacturerEntry.setText("")
                self.priceEntry.setText("")
                self.qoutaEntry.setText("")
                self.img = QPixmap('icons/addproduct.png')
                self.addProductImg.setPixmap(self.img)
            except Exception as Error:
                print(Error)
                QMessageBox.information(self,"Into","Product has not been added")
        else:
            QMessageBox.information(self,"Into","Fields cant be empty !!!")

