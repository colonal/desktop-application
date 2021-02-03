import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3, os
import addproduct, addmember, sellings, stayle
from PIL import Image

pathDB = os.environ['APPDATA']


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(150,100,1150,650)
        self.setFixedSize(self.size())
        self.UI()

    def UI(self):
        self.toolBar()
        self.tabWigdet()
        self.widgets()
        self.layouts()
        self.DB()
        self.displayProducts()
        self.displayMember()
        self.getStatistics()

    def DB(self):
        print(pathDB)
        if os.path.exists(f"{pathDB}\\Product Manager") == False :
            os.mkdir(f"{pathDB}\\Product Manager")
        
        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        _db.execute("""create table if not exists Products(
            product_Id integer primary key autoincrement,
            product_Name text,
            product_Mamufachturer text,
            product_price  integer,
            product_qouta integer,
            product_img text,
            product_availabitity Text DEFAULT Available         
            )""")

        _db.execute("""create table if not exists Members(
            member_Id integer primary key autoincrement,
            member_Name text,
            member_surName text,
            member_phone text
            )""")

        _db.execute("""create table if not exists Sellings(
            selling_Id integer primary key autoincrement,
            selling_product_Id integer,
            selling_member_Id integer,
            selling_qoutity integer,
            selling_amount integer
            )""")
        _db.commit()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ######################### Toolbar Buttons ######################
        # ######################### Add Product ##########################
        self.addProduct = QAction(QIcon('icons/add.png'), "Add Product", self)
        self.tb.addAction(self.addProduct)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addSeparator()

        # ######################### Add Member ###########################
        self.addMember = QAction(QIcon("icons/users.png"), "Add Member", self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()

        # ######################### Sell Products ######################## 
        self.sellProduct = QAction(QIcon("icons/sell.png"), "Sell Product", self)
        self.tb.addAction(self.sellProduct)
        self.sellProduct.triggered.connect(self.funcSellProducts)
        self.tb.addSeparator()

    def tabWigdet(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Members")
        self.tabs.addTab(self.tab3, "Statistics")

    def widgets(self):
        # ########################### Tabl Widget ####################
        # ########################### Main Left Layout Widget ###########
        self.productsTable = QTableWidget()
        self.productsTable.setColumnCount(6)
        self.productsTable.setColumnHidden(0, True)
        self.productsTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product Id"))
        self.productsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.productsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.productsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.productsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Qouta"))
        self.productsTable.setHorizontalHeaderItem(5, QTableWidgetItem("Availbility "))
        self.productsTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.productsTable.doubleClicked.connect(self.selectedProduct)
        # ############################ Right top Layout Widgets ################
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search For Products")
        self.searchEntry.textChanged.connect(self.searshProduct)
        self.searchButton = QPushButton("Search")
        self.searchButton.setStyleSheet(stayle.searchButton())
        self.searchButton.clicked.connect(self.searshProduct)
        # ############################ Right middle Layout Widget ##############
        self.allProducts = QRadioButton("ALL Product")
        self.availableProducts = QRadioButton("Available")
        self.notAvailableProducts = QRadioButton("Not Available")
        self.listButton = QPushButton("List")
        self.listButton.clicked.connect(self.listProducts)
        self.listButton.setStyleSheet(stayle.listButton())
        # ######################## Tab2 widgwt ############# 
        self.membersTable = QTableWidget()
        self.membersTable.setColumnCount(4)
        self.membersTable.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.membersTable.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.membersTable.setHorizontalHeaderItem(2, QTableWidgetItem("Member Surname"))
        self.membersTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.membersTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.membersTable.doubleClicked.connect(self.selectedMember)
        self.memberSearchText = QLabel("Search Members")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searshMember)
        # ######################## Tab3 widgwt ############# 
        self.totalProductsLabel = QLabel()
        self.totalMemberLabel = QLabel()
        self.soldProductsLabel =QLabel()
        self.totalAmountLabel= QLabel()
        


    def layouts(self):
        # ########################### Table Layout ########################
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRithrLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(stayle.searshBoxStayle())
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(stayle.listBoxStayle())
        self.bottomGroupBox = QGroupBox()
        # ###########################Add Widgets ######################
        # ###########################Left main Layout widget ##########
        self.mainLeftLayout.addWidget(self.productsTable)
        
        # ########################### Right top layout Widgets #########
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)
        # ############################ Right Button Layout widgets # #########\
        self.rightMiddleLayout.addWidget(self.allProducts)
        self.rightMiddleLayout.addWidget(self.availableProducts)
        self.rightMiddleLayout.addWidget(self.notAvailableProducts)
        self.rightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)


        self.mainRithrLayout.addWidget(self.topGroupBox,20)
        self.mainRithrLayout.addWidget(self.middleGroupBox,20)
        self.mainRithrLayout.addWidget(self.bottomGroupBox,60)
        #self.mainRithrLayout.addStretch()

        self.mainLayout.addLayout(self.mainLeftLayout, 70)
        self.mainLayout.addLayout(self.mainRithrLayout, 30) 
        self.tab1.setLayout(self.mainLayout)
        # ########################### Tab2 Layouts ##########
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QHBoxLayout()
        self.memberRightLayout = QHBoxLayout()
        self.memberRightGroupBox = QGroupBox("Search For Members")

        self.memberRightGroupBox.setContentsMargins(10, 20, 10, 490)
        self.memberRightLayout.addWidget(self.memberSearchText)
        self.memberRightLayout.addWidget(self.memberSearchEntry)
        self.memberRightLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightLayout)

        self.memberLeftLayout.addWidget(self.membersTable)

        self.memberMainLayout.addLayout(self.memberLeftLayout, 70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox,30)

        self.tab2.setLayout(self.memberMainLayout)
        # ########################### Tab3 Layouts ##########
        self.statisticsMainLayout = QVBoxLayout()
        self.statisticsLayout = QFormLayout()
        self.statisticsGroupBox = QGroupBox("Statistics")

        self.statisticsLayout.addRow(QLabel("Total Product: "), self.totalProductsLabel)
        self.statisticsLayout.addRow(QLabel("Total Member: "), self.totalMemberLabel)
        self.statisticsLayout.addRow(QLabel("Sold Products: "), self.soldProductsLabel)
        self.statisticsLayout.addRow(QLabel("Total Amount: "), self.totalAmountLabel)

        self.statisticsGroupBox.setLayout(self.statisticsLayout)
        self.statisticsGroupBox.setFont(QFont("Arial",20))
        self.statisticsMainLayout.addWidget(self.statisticsGroupBox)

        self.tab3.setLayout(self.statisticsMainLayout)
        self.tabs.blockSignals(False)


    def funcAddProduct(self):
        self.newProduct = addproduct.AddProduct()

    def funcAddMember (self):
        self.newMember = addmember.AddMember()

    def displayProducts(self):
        self.productsTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.productsTable.rowCount())):
            self.productsTable.removeRow(i)

        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        query = _db.execute("SELECT product_Id,product_Name,product_Mamufachturer,product_price,product_qouta,product_availabitity FROM Products")
        for row_data in query:
            row_number = self.productsTable.rowCount()
            self.productsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productsTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.productsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def displayMember(self):
        self.membersTable.setFont(QFont("Times", 12))

        for i in reversed(range(self.membersTable.rowCount())):
            self.membersTable.removeRow(i)

        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        query = _db.execute("SELECT member_Id,member_Name,member_surName,member_phone FROM Members")
        for row_data in query:
            row_number = self.membersTable.rowCount()
            self.membersTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.membersTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.membersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def selectedProduct(self):
        global productId
        listProduct= []
        for i in range(6):
            listProduct.append(self.productsTable.item(self.productsTable.currentRow(),i).text())
        
        productId = listProduct[0]

        print(listProduct)
        print(productId)
        self.display = DisplayProduct()
        self.display.show()

    def selectedMember(self):
        global membertId
        listMember= []
        for i in range(4):
            listMember.append(self.membersTable.item(self.membersTable.currentRow(),i).text())

        membertId = listMember[0]
        print(listMember)
        print(membertId)

        self.DisplayMember = DisplayMember()
        self.DisplayMember.show()

    def searshProduct(self):
        value = self.searchEntry.text()
        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        if value == "":
            #QMessageBox.information(self,"Warning", "Searsh query cant be empty!!!")
            pass

        else:
            #self.searchEntry.setText("")
            query = "SELECT product_Id,product_Name,product_Mamufachturer,product_price,product_qouta,product_availabitity FROM Products WHERE product_Name LIKE ? or product_Mamufachturer LIKE ? "
            results = _db.execute(query,("%"+value+"%","%"+value+"%")).fetchall()
            print(results)
            ################
            if results == []:
                #QMessageBox.information(self,"Warning", "There is no such a product or mamufachturer")
                pass
            else:
                for i in reversed(range(self.productsTable.rowCount())):
                    self.productsTable.removeRow(i)

                
                for row_data in results:
                    row_number = self.productsTable.rowCount()
                    self.productsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productsTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        _db.close()

    def searshMember(self):
        value = self.memberSearchEntry.text()
        print(value)
        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        if value == "":
            #QMessageBox.information(self,"Warning", "Searsh query cant be empty!!!")
            pass

        else:
            query = "SELECT member_Id,member_Name,member_surName FROM Members WHERE member_Name LIKE ? or member_surName LIKE ? or member_phone LIKE ? "
            results = _db.execute(query,("%"+value+"%","%"+value+"%","%"+value+"%")).fetchall()
            print(results)
            if results == []:
                #QMessageBox.information(self,"Warning", "There is no such a product or mamufachturer")
                pass
            else:
                for i in reversed(range(self.membersTable.rowCount())):
                    self.membersTable.removeRow(i)

                
                for row_data in results:
                    row_number = self.membersTable.rowCount()
                    self.membersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.membersTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        _db.close()

    def listProducts(self):
        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        if self.allProducts.isChecked() == True:
            self.displayProducts()

        elif self.availableProducts.isChecked():
            query = ("SELECT product_Id,product_Name,product_Mamufachturer,product_price,product_qouta,product_availabitity FROM Products WHERE product_availabitity='Available'")
            product = _db.execute(query).fetchall()
            print(product)
            if product == []:
                #QMessageBox.information(self,"Warning", "There is no such a product or mamufachturer")
                pass
            else:
                for i in reversed(range(self.productsTable.rowCount())):
                    self.productsTable.removeRow(i)

                
                for row_data in product:
                    row_number = self.productsTable.rowCount()
                    self.productsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productsTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        elif self.notAvailableProducts.isChecked():
            query = ("SELECT product_Id,product_Name,product_Mamufachturer,product_price,product_qouta,product_availabitity FROM Products WHERE product_availabitity='UnAvailable'")
            product = _db.execute(query).fetchall()
            print(product)
            if product == []:
                #QMessageBox.information(self,"Warning", "There is no such a product or mamufachturer")
                pass
            else:
                for i in reversed(range(self.productsTable.rowCount())):
                    self.productsTable.removeRow(i)

                
                for row_data in product:
                    row_number = self.productsTable.rowCount()
                    self.productsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productsTable.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        _db.close()
    def funcSellProducts(self):
        self.sell = sellings.SellProducts()

    def getStatistics(self):
        _db = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        countProducts = _db.execute("SELECT count(product_Id) FROM Products").fetchall()
        countMember = _db.execute("SELECT count(member_Id) FROM Members").fetchall()
        selling = _db.execute("SELECT SUM(selling_qoutity), SUM(selling_amount) FROM Sellings").fetchall()
        countProducts = countProducts[0][0]
        countMember = countMember[0][0]
        soldProducts = selling[0][0]
        totalAmount = selling[0][1]
        print(countProducts,countMember, soldProducts, totalAmount)
        self.totalProductsLabel.setText(str(countProducts))
        self.totalMemberLabel.setText(str(countMember))
        self.soldProductsLabel.setText(str(soldProducts))
        self.totalAmountLabel.setText(str(totalAmount)+"$")

    def tabChanged(self):
        self.getStatistics()
        self.displayProducts()
        self.displayMember()


        
class DisplayMember(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Member Details")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,600)
        self.setFixedSize(self.size())
        # ################ DB
        pathDB = os.environ['APPDATA']

        self.con = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        self.cur = self.con.cursor()
        # ####################
        self.UI()
    
    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layout()

    def memberDetails(self):
        global membertId
        query = ("SELECT * FROM Members WHERE member_Id=?")
        member = self.cur.execute(query,(membertId,)).fetchone()
        print(member)
        self.memberName=member[1]
        self.memberSurName = member[2]
        self.memberPhon = member[3]

    def widgets(self):
        self.memberImg = QLabel()
        self.img=QPixmap('icons/members.png')
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display Member")
        self.titleText.setAlignment(Qt.AlignCenter)
        # #########################
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.memberName)
        self.surNameEntry = QLineEdit()
        self.surNameEntry.setText(self.memberSurName)
        self.phonEntry = QLineEdit()
        self.phonEntry.setText(self.memberPhon)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updataMember)
        self.deleteBut = QPushButton("Delete")
        self.deleteBut.clicked.connect(self.deleteMember)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayuot = QVBoxLayout()
        self.buttmLayout = QFormLayout()

        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(stayle.MembertopFrame())
        self.buttmFrame = QFrame()
        self.buttmFrame.setStyleSheet(stayle.MemberbuttmFrame())
        # ################# add Widget
        self.topLayuot.addWidget(self.titleText)
        self.topLayuot.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayuot)

        self.buttmLayout.addRow(QLabel("Name"), self.nameEntry)
        self.buttmLayout.addRow(QLabel("SurName"),self.surNameEntry)
        self.buttmLayout.addRow(QLabel("Phone"), self.phonEntry)
        self.buttmLayout.addRow(QLabel(""),self.updateBtn)
        self.buttmLayout.addRow(QLabel(""),self.deleteBut)
        self.buttmFrame.setLayout(self.buttmLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttmFrame)

        self.setLayout(self.mainLayout)

    def deleteMember(self):
        global membertId
        mbox = QMessageBox.question(self,"Warning","Are you sure to delete this member", QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                self.cur.execute("DELETE FROM Members WHERE member_Id=?",(membertId,))
                self.con.commit()
                QMessageBox.information(self,"INFORMATION", "Member has beeen deleted!")
            except:
                QMessageBox.information(self,"INFORMATION", "Member has Not beeen deleted!")

    def updataMember (self):
        global membertId
        name = self.nameEntry.text()
        surName = self.surNameEntry.text()
        phon = self.phonEntry.text()

        if (name and surName and phon  !=""):
            try:
                query = "UPDATE Members set member_Name=?,member_surName=?,member_phone=?WHERE member_Id=?"
                self.cur.execute(query,(name,surName,phon,membertId))
                self.con.commit()
                QMessageBox.information(self,"Info", "Members has been updated !")
            except:
                QMessageBox.information(self,"Info", "Members has Not been updated !")
        else:
            QMessageBox.information(self,"Info", "Fields cant be empty !!!")
    
    def closeEvent(self, Event) :
        return self.con.close()


class DisplayProduct(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Product Details")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,600)
        self.setFixedSize(self.size())
        # ################ DB
        pathDB = os.environ['APPDATA']

        self.con = sqlite3.connect(f"{pathDB}\\Product Manager\\Products.db")
        self.cur = self.con.cursor()
        # ####################
        self.UI()

        #self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layout()

    def productDetails(self):
        global productId
        query = "SELECT * FROM Products WHERE product_Id=?"
        product =self.cur.execute(query,(productId,)).fetchone()

        print(product)
        self.productName = product[1]
        self.productManufacturer = product[2]
        self.productPrice = product[3]
        self.productQouta = product[4]
        self.productImg = product[5]
        self.productStatus = product[6]

    def widgets(self):
        # ##################### top Layout
        self.product_Img = QLabel()
        self.img = QPixmap('img/{}'.format(self.productImg))
        self.product_Img.setPixmap(self.img)
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Updata Product")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.titleText.setFont(QFont("Times", 14))
        # ###################### Buttom Layout
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.productName)
        self.manufacturer = QLineEdit()
        self.manufacturer.setText(self.productManufacturer)
        self.priceEntry = QLineEdit()
        self.priceEntry.setText(str(self.productPrice))
        self.qoutaEntry = QLineEdit()
        self.qoutaEntry.setText(str(self.productQouta))
        self.availabilityCombo = QComboBox()
        self.availabilityCombo.addItems(["Available", "UnAvailable"])
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteProduct)
        self.updateBtn = QPushButton("Updata")
        self.updateBtn.clicked.connect(self.updataProduct)


    def uploadImg(self):
        size = (256,256)
        self.filename, ok = QFileDialog.getOpenFileName(self,"Upload Image", "","Image Files (*.jpg *.png)")  
        if ok:
            print(self.filename)
            defaultImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))
            self.img = QPixmap("img/{0}".format(defaultImg))
            self.product_Img.setPixmap(self.img)

    def updataProduct(self):
        global productId
        name = self.nameEntry.text()
        manufacturer = self.manufacturer.text()
        price = int(self.priceEntry.text())
        qouta  =int (self.qoutaEntry.text())
        status = self.availabilityCombo.currentText()
        defaultTmg = self.productImg

        if (name and manufacturer and price and qouta !=""):
            try:
                query = "UPDATE Products set product_Name=?,product_Mamufachturer=?,product_price=?, product_qouta=?, product_img=?, product_availabitity=? WHERE product_Id=?"
                self.cur.execute(query,(name,manufacturer,price,qouta,defaultTmg, status,productId))
                self.con.commit()
                QMessageBox.information(self,"Info", "Product has been updated !")
            except:
                QMessageBox.information(self,"Info", "Product has Not been updated !")
        else:
            QMessageBox.information(self,"Info", "Fields cant be empty !!!")

    def deleteProduct(self):
        global productId
        mbox = QMessageBox.question(self,"Warning", "Are you sure to delete this product", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                self.cur.execute( "delete FROM Products WHERE product_Id=?",(productId,))
                self.con.commit()
                QMessageBox.information(self,"INFORMATION", "Product has beeen deleted!")
            except:
                QMessageBox.information(self,"INFORMATION", "Product has Not beeen deleted!")




    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayuot = QVBoxLayout()
        self.buttmLayout = QFormLayout()

        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(stayle.topFrame())
        self.buttmFrame = QFrame()
        self.buttmFrame.setStyleSheet(stayle.buttmFrame())
        # ############### Add widgets
        self.topLayuot.addWidget(self.titleText)
        self.topLayuot.addWidget(self.product_Img)
        self.topFrame.setLayout(self.topLayuot)
        self.buttmLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.buttmLayout.addRow(QLabel("Manufacturer: "), self.manufacturer)
        self.buttmLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.buttmLayout.addRow(QLabel("Qouta: "), self.qoutaEntry)
        self.buttmLayout.addRow(QLabel("Status: "), self.availabilityCombo)
        self.buttmLayout.addRow(QLabel("Image: "), self.uploadBtn)
        self.buttmLayout.addRow(QLabel(""), self.deleteBtn)
        self.buttmLayout.addRow(QLabel(""), self.updateBtn)
        self.buttmFrame.setLayout(self.buttmLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.buttmFrame)

        self.setLayout(self.mainLayout)


    def closeEvent(self, Event) :
        return self.con.close()


def main():
    App = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(App.exec_())

if "__main__" == __name__:
    main() 