from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import time
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon, QMenu, QMainWindow,QTableWidgetItem, QAction
import sqlite3
import sys
import threading

exitT = 0

class MainApp(QMainWindow):
    
    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi(f'autoZoomGUI.ui', self)
        global trayIcon
        self.setWindowIcon(QIcon('img/Zoom-App-Icon.png')) 
        self.setWindowTitle('Auto Zoom')
        # ##########################
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        # ##########################
        # hidden icon Start
        trayIcon = QSystemTrayIcon(QIcon("img/Zoom-App-Icon.png"), parent=self)
        trayIcon.setToolTip("Open Auto Zoom")
        trayIcon.show()
        def showMessage():
            trayIcon.showMessage("Auto Zoom", "The program is running in the background, when you close the program stops completely",QIcon("img/Zoom-App-Icon.png"), msecs = 10000)
        menu = QMenu()
        # Exit start
        
        def Exit(self):
            global exitT
            exitT += 1
            exit()
        
        # Exit end
        # Show start
        showAction = menu.addAction("Show")
        exitAction = menu.addAction("Exit")
        def shoW(self):
            self.show()
        showAction.triggered.connect(self.show)
        exitAction.triggered.connect(Exit)
        # End Show
        trayIcon.setContextMenu(menu)
        # ###  ###   ###
       
        ######## #######
        self.connect_db()
        self.show_data()
        self.tabWidget.tabBar().setVisible(False)
        self.pushButton_2.clicked.connect(self.Show_All)
        self.pushButton_3.clicked.connect(self.Back)
        self.pushButton_4.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.run)
        self.pushButton.setIcon(QIcon('img/play.png'))
    
    def closeEvent(self, event):
        global exitT
        exitT += 1
    
    def run(self):
    	threading.Thread(target= self.start).start()
        # ##### db
        
	    
        # #############
    def connect_db(self):
        _db = sqlite3.connect('Zoom.db')
        _db.row_factory = sqlite3.Row
        _db.execute("create table if not exists zoom(Id integer primary key autoincrement, name text, link text, time text,commant text)")
        _db.commit()
        _db.close()
   
    def Show_All(self):
        self.show_data()
        self.tabWidget.setCurrentIndex(1)

    def Back(self):
        self.tabWidget.setCurrentIndex(0)
    
    def show_data(self):
        try:
            print("show_data")
            self.tableWidget.clearContents()
            _db = sqlite3.connect("Zoom.db")
            _date = _db.execute("Select * from zoom")
            
            date = []
            for i in _date:
                date.append(i)
            print(f"\ndata: \n{date}\n{len(date)}")
            
            self.tableWidget.setRowCount(len(date))
            c = 0
            for i in date:
                self.tableWidget.setItem(c,0,QTableWidgetItem(i[1]))
                self.tableWidget.setItem(c,1,QTableWidgetItem(i[2]))
                self.tableWidget.setItem(c,2,QTableWidgetItem(i[3]))
                self.tableWidget.setItem(c,3,QTableWidgetItem(i[4]))
                #self.tableWidget.setItem(c,4,QTableWidgetItem(i[5]))
                if len(date) > c:
                    print(c)
                    c += 1
            _db.close()
        except Exception as er:
            print(er)

    def save(self):
        
        name = self.lineEdit.text()
        link = self.lineEdit_2.text()
        time = self.timeEdit.time()
        chat = self.textEdit.toPlainText()
        time = str(time).split("(")[1].split(")")[0].replace(" ", '').replace(",",":")
        print(name,link,time,chat)
        conn = sqlite3.connect('Zoom.db')
        c = conn.cursor()
        c.execute("insert into zoom(name , link , time,  commant) values(?,?,?,?)", (name, link, time, chat))
        conn.commit()
        conn.close()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.textEdit.setPlainText("")
        self.show_data()
    
    def delete(self):
        print("Delete")
        conn = sqlite3.connect('Zoom.db')
        name = self.lineEdit_3.text()
        c = conn.cursor()
        sql = 'DELETE FROM zoom WHERE name=?'
        c.execute(sql, (name,))
        conn.commit()
        conn.close()
        self.show_data()
        self.lineEdit_3.setText("")
        
    def start(self):
        print("start")
        global trayIcon
        global exitT
        self.pushButton.setIcon(QIcon('img/play.png'))
        trayIcon.showMessage("Auto Zoom", "The program is running in the background, when you close the program stops completely",QIcon("img/Zoom-App-Icon.png"), msecs = 10000)
        self.hide()
        
        def auto_zoom(link , Time, chat):
            def r(cors, chat):
                trayIcon.showMessage("Auto Zoom", f"Will now run", QIcon("img/Zoom-App-Icon.png"), msecs=1000)
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.implicitly_wait(30)
                driver.maximize_window()

                driver.get(cors)
                time.sleep(5)
                #####################
                
                #####################
                pyautogui.click(763,221, clicks=1, button="left", interval=1)
                pyautogui.click(763,221, clicks=1, button="left")
                time.sleep(10)
                while True:
                    if exitT != 0:
                        return
                    join = pyautogui.locateCenterOnScreen("img\\Zoom.png")
                    if join == None:
                        time.sleep(2)
                        continue
                    else:
                        print("Joen meetng")
                        pyautogui.click(join[0], join[1])
                        if chat != None and chat != "":
                            print("chat")
                            time.sleep(15)
                            # pyautogui.click(join[0], join[1], clicks = 2, button= 'left')
                            pyautogui.move(10, 10)
                            pyautogui.click(688,735)
                            pyautogui.write(chat)
                            pyautogui.hotkey("enter")
                        break
                
                driver.quit()
            sheck = []
            sheck_1 = []
            while True:
                if exitT != 0:
                        return
                for i in link:
                    if i in sheck:
                        pass
                    else:
                        sheck_1.append(i)
                if len(sheck_1) == 0:
                    break
                
                x = datetime.now()
                # day = time.ctime().split(" ")[0]
                xx = str(x).split(" ")[1].split(".")[0]
                if "00" != xx.split(":")[2]:
                    continue
                
                xx = xx.split(":")
                xx = f"{xx[0]}:{xx[1]}"
                cunt = 0 
                for i in link:
                    print(link[cunt], "\n", xx,"\t\t", Time[cunt],"\n")
                    if Time[cunt] in xx and link[cunt] not in sheck : # and day == "Tue":
                        
                        print(f"Don: {xx}")
                        #exit()
                        sheck.append(link[cunt])
                        r(link[cunt], chat[cunt])
                        del link[cunt]
                        continue
                    if len(link) > cunt:
                        cunt += 1
                time.sleep(60)
        _link = []
        Time = []
        chat = []
        conn = sqlite3.connect('Zoom.db')
        c = conn.cursor()

        for row in c.execute("SELECT * FROM Zoom;"):
            print(row)
            _link.append(row[2])
            Time.append(row[3])
            chat.append(row[4])

        print("link\n", _link, '\n')
        print("Time\n", Time, '\n')
        print("chat\n", chat, '\n')


        if len(_link) == len(Time) == len(chat):
            auto_zoom(_link, Time, chat)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
