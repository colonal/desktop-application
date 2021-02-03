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


class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layout()

    def widgets(self):
        # ##################### widgets of top layout
        self.addMemberImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleTixt = QLabel("Add Member")
        self.titleTixt.setAlignment(Qt.AlignCenter)
        # ##################### widgets of buttom layout
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name of member")
        self.surnameEntry=QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter surname of member")
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter name phone member")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addMember)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.buttomLayout = QFormLayout()

        self.topFrame = QFrame()
        self.buttomFrame = QFrame()
        # ############################# add widgets
        self.topLayout.addWidget(self.titleTixt)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)

        self.buttomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.buttomLayout.addRow(QLabel("SurName: "), self.surnameEntry)
        self.buttomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.buttomLayout.addRow(QLabel(""), self.submitBtn)
        self.buttomFrame.setLayout(self.buttomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttomFrame)

        self.setLayout(self.mainLayout)

    def addMember(self):
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone= self.phoneEntry.text()

        if (name and surname and phone != ""):
            try:
                query = "INSERT INTO Members(member_Name, member_surName, member_phone)VALUES(?,?,?)"
                cur.execute(query,(name,surname, phone))
                con.commit()
                QMessageBox.information(self,"Info", "Member has been added !")
                self.nameEntry.setText("")
                self.surnameEntry.setText("")
                self.phoneEntry.setText("")
            except Exception as Error:
                print(Error)
                QMessageBox.information(self,"Info", "Member has not been added !!!")

        else:
            QMessageBox.information(self,"Info", "Fields can not be empty!")
