import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3, os,stayle
from PIL import Image

pathDB = os.environ['APPDATA']

con = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
cur = con.cursor()
defaultImg = "store.png"


class SellProducts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell Products")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layout()
    

    def widgets(self):
        # ################################ top layout wiggets
        self.sellProductImg = QLabel()
        self.img = QPixmap('icons/shop.png')
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.sellProductImg.resize(150,150)
        self.titleText = QLabel("Sell Products")
        self.titleText.setAlignment(Qt.AlignCenter)
        # ############################## bottom layout widgets
        self.productComno = QComboBox()
        self.productComno.currentIndexChanged.connect(self.chanaComboValue)
        self.memberCombo = QComboBox()
        self.quantityCombo = QComboBox()
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.sellProdect)

        query1 = ("SELECT * FROM Products WHERE product_availabitity=?")
        products= cur.execute(query1,("Available",)).fetchall()
        query2 = ("SELECT member_Id,member_Name FROM Members")
        members = cur.execute(query2).fetchall()
        quantity = products[0][4]

        for product in products:
            self.productComno.addItem(product[1] ,product[0])

        for member in members:
            self.memberCombo.addItem(member[1],member[0])
        
        for i in range(1,quantity+1):
            self.quantityCombo.addItem(str(i))

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.buttomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(stayle.sellingtopFrame())
        self.buttomFrame = QFrame()
        self.buttomFrame.setStyleSheet(stayle.sellingbuttmFrame())

        # ######################### add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)

        self.buttomLayout.addRow(QLabel("Product: "), self.productComno)
        self.buttomLayout.addRow(QLabel("Member: "), self.memberCombo)
        self.buttomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.buttomLayout.addRow(QLabel(""), self.submitBtn)
        self.buttomFrame.setLayout(self.buttomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttomFrame)

        self.setLayout(self.mainLayout)

    def chanaComboValue(self):
        productId = self.productComno.currentData()
        query = ("SELECT product_qouta FROM Products WHERE product_Id=?")
        qoute = cur.execute(query,(productId,)).fetchone()
        
        for i in range(1,qoute[0]+1):
            self.quantityCombo.addItem(str(i))

    def sellProdect (self):
        global productName, productId, memberName,memberID,quantity
        productName = self.productComno.currentText()
        productId = self.productComno.currentData()
        memberName = self.memberCombo.currentText()
        memberID = self.memberCombo.currentData()
        quantity = int(self.quantityCombo.currentText())
        self.confirm = ConfirmWindow()
        self.confirm.show()
        self.close()


class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Sell Product")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        # ################ DB
        pathDB = os.environ['APPDATA']

        self.con = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        self.cur = self.con.cursor()
        # ####################
        self.UI()
    
    def UI(self):
        self.widgets()
        self.layout()


    def widgets(self):
        self.SellProductImg = QLabel()
        self.img=QPixmap('icons/shop.png')
        self.SellProductImg.setPixmap(self.img)
        self.SellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Product")
        self.titleText.setAlignment(Qt.AlignCenter)
        # ############################### widget of bottom layout
        global productName, productId, memberName,memberID, quantity
        priceQuery = ("SELECT  product_price FROM Products WHERE product_Id=?")
        price = self.cur.execute(priceQuery,(productId,)).fetchone()
        self.amount = quantity*price[0]
        self.productName = QLabel()
        self.productName.setText(productName)
        self.memberName = QLabel()
        self.memberName.setText(memberName)
        self.amountLabel = QLabel()
        self.amountLabel.setText(f"{price[0]}X{quantity} = {price[0]*quantity}")

        self.confirmBtn  =  QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.Confirm)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayuot = QVBoxLayout()
        self.buttmLayout = QFormLayout()

        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(stayle.ConfirmtopFrame())
        self.buttmFrame = QFrame()
        self.buttmFrame.setStyleSheet(stayle.ConfirmbuttmFrame())
        # ################# add Widget
        self.topLayuot.addWidget(self.titleText)
        self.topLayuot.addWidget(self.SellProductImg)
        self.topFrame.setLayout(self.topLayuot)

        self.buttmLayout.addRow(QLabel("Product: "),self.productName)
        self.buttmLayout.addRow(QLabel("Member: "),self.memberName)
        self.buttmLayout.addRow(QLabel("Amount"),self.amountLabel)
        self.buttmLayout.addRow(QLabel(""),self.confirmBtn)

        self.buttmFrame.setLayout(self.buttmLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttmFrame)

        self.setLayout(self.mainLayout)

    def Confirm(self):
        global productName, productId, memberName,memberID, quantity
        try:
            sellQuery = "INSERT INTO Sellings (selling_product_Id,selling_member_Id,selling_qoutity,selling_amount)VALUES(?,?,?,?)"
            self.cur.execute(sellQuery,(productId,memberID,quantity,self.amount))
            self.con.commit()
            qutaQuery = ("SELECT  product_qouta FROM Products WHERE product_Id=?")
            self.qouta = self.cur.execute(qutaQuery,(productId,)).fetchone()

            if quantity == self.qouta[0]:
                updataQoutaQuery = "UPDATE Products set product_qouta=?,product_availabitity=? WHERE product_Id=?"
                self.cur.execute(updataQoutaQuery,(0,"UnAvailable", productId))

                self.con.commit()
            else:
                newQouta = self.qouta[0] - quantity
                updataQoutaQuery = "UPDATE Products set product_qouta=? WHERE product_Id=?"
                self.cur.execute(updataQoutaQuery,(newQouta,productId))
                self.con.commit()
            QMessageBox.information(self,"Info", "Success")

        except Exception as Error:
            QMessageBox.information(self,"Info", f"Something went wrong !!!!\n\n{Error}")