try:
    import pyautogui
    import time
    from datetime import datetime
    from PyQt5 import uic
    from PyQt5.QtGui import QIcon, QPixmap
    from PyQt5.QtWidgets import QApplication,QSystemTrayIcon, QMenu, QMainWindow,QTableWidgetItem, QAction, QFileDialog, QMessageBox
    import sqlite3
    import sys
    import threading
    import webbrowser
    import mouseinfo
    import os
    

    exitT = 0
    stop = 0
    dirfile = os.environ['APPDATA']
    if os.path.exists(f"{dirfile}\\Auto Zoom") == False :
        os.mkdir(f"{dirfile}\\Auto Zoom")
    dirfile = f"{dirfile}\\Auto Zoom"

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
            self.setFixedSize(514, 497)
            trayIcon.show()
            def showMessage():
                trayIcon.showMessage("Auto Zoom", "The program is running in the background, when you close the program stops completely",QIcon("img/Zoom-App-Icon.png"), msecs = 10000)
            menu = QMenu()
            # Exit start
            
            
            
            # Exit end
            # Show start
            showAction = menu.addAction("Show")
            exitAction = menu.addAction("Exit")
            
            showAction.triggered.connect(self.show)
            exitAction.triggered.connect(self.Exit)
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
            self.pushButton_11.clicked.connect(self.Browse)
            self.pushButton_12.clicked.connect(self.Browse1)
            self.pushButton.setIcon(QIcon('img/play.png'))
            #self.pushButton_6.setIcon(QIcon('img/Setting.png'))
            stylesheet = """
            QPushButton{
                
                background-color: #19232D;
                border: 1px solid #32414B;
                }
            QPushButton:hover {
                background-color: #505F69;}
            QPushButton:pressed  {
                background-color: #19232D;}
            QPushButton:default {
                border-color: navy; /* make the default button prominent */
            }
            
            """
            self.pushButton_6.setStyleSheet(stylesheet+ "QPushButton{border-image : url('img//setting.png');}")
            self.pushButton_7.setStyleSheet(stylesheet+ "QPushButton{border-image : url('img//back.png');}")
            self.pushButton_6.clicked.connect(self.OSetting)
            self.pushButton_7.clicked.connect(self.CSetting)
            self.pushButton_8.clicked.connect(self.run_mous_info)
            self.pushButton_9.clicked.connect(self.SaveSetting)
            self.pushButton_10.clicked.connect(self.Default)
            img = QPixmap("img//open Zoom E.png")
            self.label_11.setPixmap(img)
            self.label_11.resize(img.width(), img.height())
            img1 = QPixmap("img//chat1.png")
            self.label_17.setPixmap(img1)
            self.label_17.resize(img1.width(), img1.height())
            self.MassageOpen()
            self.TimeNow()
        def MassageOpen(self):
            global dirfile
            db = sqlite3.connect(f"{dirfile}\\Zoom.db")
            MO = []
            for i in db.execute("SELECT MessageOpen FROM message"):
                MO.append(i)
            
            title = "Auto Zoom"
            message = """
    It is a program to automatically open a meeting so that you do not miss the meeting time, and it is in its first version, you must make sure that it works well and to not rely entirely on it
    Requirements
    1- Google Chrome browser
    2- Zoom desktop program

    We hope to benefit from it
    COLONAL
            """
            
            if MO[0][0] == 0 :
                db.execute("UPDATE message SET MessageOpen=1")
                QMessageBox.about(self, title, message)

            
            db.commit()
            db.close()
            pass
        def Browse(self):
            save = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
            
            self.lineEdit_6.setText(save[0])
        def Browse1(self):
            save = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.jpg *.png)")
            
            self.lineEdit_7.setText(save[0])

        def Time (self):
            global exitT
            while True:
                if exitT == 1:
                    break
                time.sleep(1)
                x = time.ctime().split(" ")[3]
                self.label_29.setText(x)

        def shoW(self):
                self.show()
        def Exit(self):
                global exitT
                
                exitT += 1
                self.close()
                #self.quit()
        
        def closeEvent(self, event):
            global exitT
            exitT += 1
        
        def run(self):
            threading.Thread(target= self.start).start()
            
        def TimeNow(self):
            threading.Thread(target= self.Time).start()
                
            # #############
        def connect_db(self):
            global dirfile
            _db = sqlite3.connect(f'{dirfile}\\Zoom.db')
            _db.row_factory = sqlite3.Row
            _db.execute("create table if not exists zoom(Id integer primary key autoincrement, name text, link text, time text,commant text, Day text)")
            _db.execute("create table if not exists setting(Id integer primary key autoincrement, OpenZoom text, chat text)")
            _db.execute("create table if not exists Dsetting(Id integer primary key autoincrement, DOpenZoom text, DChat text)")
            _db.execute("create table if not exists message(Id integer primary key autoincrement, MessageOpen integer, MessageSetting integer)")
            _db.commit()
            Dsetting = []
            setting = []
            massage = []
            for i in _db.execute("SELECT ID from Dsetting"):
                Dsetting.append(i)
            for i in _db.execute("SELECT ID from setting"):
                setting.append(i)
            for i in _db.execute("SELECT ID from message"):
                massage.append(i)
            if len(Dsetting) == 0:
                _db.execute("INSERT  into Dsetting (DOpenZoom ,DChat) values('img\\open_zoom.png','img\\chat.png')")
            if len(setting) == 0:
                _db.execute("INSERT  into setting (OpenZoom ,chat) values('img\\open_zoom.png','img\\chat.png')")
            if len(massage) == 0:
                _db.execute("INSERT  into message (MessageOpen ,MessageSetting) values(0,0)")
            
            _db.commit()
            _db.close()
       
        def Show_All(self):
            self.show_data()
            self.tabWidget.setCurrentIndex(1)

        def Back(self):
            self.label_7.setText("")
            self.label_8.setText("")
            self.label_9.setText("")
            self.label_10.setText("")
            self.tabWidget.setCurrentIndex(0)
        
        def OSetting(self):
            global dirfile
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.lineEdit_7.setText("")
            self.label_26.setText("")
            self.label_27.setText("")
            self.label_28.setText("")
            _db = sqlite3.connect(f"{dirfile}\\Zoom.db")
            setting = []
            for i in  _db.execute("Select * from setting"):
                setting.append(i[1])
                setting.append(i[2])
            
            
            if "png" in setting[0] or "jpg" in setting[0]:
                self.lineEdit_6.setText(setting[0])
            else:
                s = setting[0].split(",")
                self.lineEdit_4.setText(s[0])
                self.lineEdit_5.setText(s[1])
            #
            if "png" in setting[1] or "jpg" in setting[1]:
                self.lineEdit_7.setText(setting[1])
            else:
                s = setting[1].split(",")
                self.lineEdit_8.setText(s[0])
                self.lineEdit_9.setText(s[1])
            MO = []
            for i in _db.execute("SELECT MessageSetting FROM message"):
                MO.append(i)
            
            title = "Auto Zoom"
            message = """
    These settings are advanced,
    Please do not change it unless you understand how to use it

    You have to choose between entering coordinates, and these coordinates represent where you press the left mouse button on a screen or enter a picture and it determines its presence on a screen and press the center coordinates of an image with the left button of the mouse

    Remember that you can always return the default value and then press the Save button
            """
          
            if MO[0][0] == 0 :
                _db.execute("UPDATE message SET MessageSetting=1")
                _db.commit()
                QMessageBox.about(self, title, message)

            
            

            _db.close()
            self.tabWidget.setCurrentIndex(2)
        
        def CSetting(self):
            self.tabWidget.setCurrentIndex(0)
        
        def run_mous_info(self):
            threading.Thread(target= self.mous_info).start()
        def mous_info(self):
            mouseinfo.mouseInfo()

        def show_data(self):
            global dirfile
            try:
               
                self.tableWidget.clearContents()
                _db = sqlite3.connect(f"{dirfile}\\Zoom.db")
                _date = _db.execute("Select * from zoom")
                
                date = []
                for i in _date:
                    date.append(i)
                
                
                self.tableWidget.setRowCount(len(date))
                c = 0
                for i in date:
                    self.tableWidget.setItem(c,0,QTableWidgetItem(i[1]))
                    self.tableWidget.setItem(c,1,QTableWidgetItem(i[2]))
                    self.tableWidget.setItem(c,2,QTableWidgetItem(i[3]))
                    self.tableWidget.setItem(c,3,QTableWidgetItem(i[5]))
                    self.tableWidget.setItem(c,4,QTableWidgetItem(i[4]))
                    if len(date) > c:
                        
                        c += 1
                _db.close()
            except Exception as er:
                print(er)

        def save(self):
            global dirfile
            self.label_7.setText("")
            self.label_8.setText("")
            self.label_9.setText("")
            self.label_10.setText("")
            name = self.lineEdit.text()
            link = self.lineEdit_2.text()
            time = self.timeEdit.time()
            chat = self.textEdit.toPlainText()
            time = str(time).split("(")[1].split(")")[0].replace(" ", '').replace(",",":")
            if time.split(":")[1] == "0":
                time = time.split(":")[0] + ":"+ time.split(":")[1]+ '0'
            if len(time.split(":")[1]) == 1:
                time = time.split(":")[0] + ":"+ "0" +time.split(":")[1]
            day = ''
            if self.checkBox.isChecked():
                day += "Sun,"
            if self.checkBox_2.isChecked():
                day += "Mon,"
            if self.checkBox_4.isChecked():
                day += "Tue,"
            if self.checkBox_3.isChecked():
                day += "Wed,"
            if self.checkBox_6.isChecked():
                day += "Thu,"
            if self.checkBox_5.isChecked():
                day += "Fri,"
            if self.checkBox_7.isChecked():
                day += "Sat,"
            
            if name == None or len(name) == 0:
                
                self.label_7.setText("Please enter a name")
                return
            if "https://us02web.zoom.us" in link or "https://zoom.us"  in link:
                pass
            else:
                
                self.label_8.setText("Please enter a valid link")
                return
            if time == "0:00":
                
                self.label_10.setText("Please enter a valid Time")
                return
            if len (day) == 0:
                self.label_9.setText("Please choose today")
                return
            conn = sqlite3.connect(f'{dirfile}\\Zoom.db')
            c = conn.cursor()
            c.execute("insert into zoom(name , link , time,  commant, Day) values(?,?,?,?,?)", (name, link, time, chat, day))
            conn.commit()
            conn.close()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.textEdit.setPlainText("")
            self.show_data()
        
        def delete(self):
            global dirfile
            conn = sqlite3.connect(f'{dirfile}\\Zoom.db')
            name = self.lineEdit_3.text()
            c = conn.cursor()
            sql = 'DELETE FROM zoom WHERE name=?'
            c.execute(sql, (name,))
            conn.commit()
            conn.close()
            self.show_data()
            self.lineEdit_3.setText("")
            
        def start(self):
            global trayIcon, exitT, stop, dirfile

            if stop == 0:
                stop = 1
            else:
                self.pushButton.setIcon(QIcon('img/play.png'))
                stop = 0
            self.pushButton.setIcon(QIcon('img/stop.png'))
            trayIcon.showMessage("Auto Zoom", "The program is running in the background, when you close the program stops completely",QIcon("img/Zoom-App-Icon.png"), msecs = 10000)
            self.hide()
            def auto_zoom(link , Time, chat, Day, setting):
                def r(cors, chat, setting):
                    trayIcon.showMessage("Auto Zoom", f"Will now run", QIcon("img/Zoom-App-Icon.png"), msecs=1000)
                    chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab(cors)
                    time.sleep(5)
                    pyautogui.moveTo(708, 191)
                    #####################
                    
                    #####################
                    if "png" in setting[0] or "jpg" in setting[0]:
                        while True:
                            if stop == 0:
                                self.pushButton.setIcon(QIcon('img/play.png'))
                                return
                            if "img\open_zoom.png" in setting[0]:
                                open_zoom = pyautogui.locateCenterOnScreen("img\\open_zoom.png")
                                if open_zoom != None:
                                    break
                                open_zoom = pyautogui.locateCenterOnScreen("img\\open_zoom1.png")
                                if open_zoom != None:
                                    break
                            else:
                                open_zoom = pyautogui.locateCenterOnScreen(str(setting[0]))
                                if open_zoom != None:
                                    break
                        pyautogui.click(open_zoom[0],open_zoom[1])
                    else:
                        s = setting[0].split(",")
                        pyautogui.click(int(s[0]),int(s[1]))
                    
                    time.sleep(10)
                    while True:
                        if exitT != 0:
                            return
                        if stop == 0:
                            self.pushButton.setIcon(QIcon('img/play.png'))
                            return
                        join = pyautogui.locateCenterOnScreen("img\\Zoom.png")
                        if join == None:
                            time.sleep(2)
                            continue
                        else:
                            pyautogui.click(join[0], join[1])
                            if chat != None and chat != "":
                                if "png" in setting[1] or "jpg" in setting[1]:
                                    d = 0
                                    while True:
                                        if stop == 0:
                                            self.pushButton.setIcon(QIcon('img/play.png'))
                                            return
                                        pyautogui.move(10,0)
                                        if "img\chat.png" in setting[1]:
                                            write_chat = pyautogui.locateCenterOnScreen("img\chat.png")
                                            if write_chat != None:
                                                d = 1
                                                break
                                        else:
                                            write_chat = pyautogui.locateCenterOnScreen(str(setting[1]))
                                            if write_chat != None:
                                                d = 0
                                                break
                                    time.sleep(2)
                                    if d == 1 :
                                        pyautogui.click(write_chat[0]-130, write_chat[1])
                                    else:
                                        pyautogui.click(write_chat[0], write_chat[1])
                                else:
                                    s = setting[0].split(",")
                                    pyautogui.click(int(s[0]), int(s[1]))
                                pyautogui.write(chat)
                                pyautogui.hotkey("enter")
                            break
                    
                    
                while True:
                    exi = 0
                    if exitT != 0:
                        return
                    if stop == 0:
                        self.pushButton.setIcon(QIcon('img/play.png'))
                        return
                    
                    x = datetime.now()
                    # day = time.ctime().split(" ")[0]
                    xx = str(x).split(" ")[1].split(".")[0]
                    if "00" != xx.split(":")[2]:
                        continue
                    
                    xx = xx.split(":")
                    xx = f"{xx[0]}:{xx[1]}"
                    cunt = 0 
                    for i in link:
                        if Time[cunt] in xx : #and day in Day:
                            

                            r(link[cunt], chat[cunt], setting)
                            link.pop(cunt)
                            Time.pop(cunt)
                            chat.pop(cunt)
                            if len(link) == 0:
                                self.pushButton.setIcon(QIcon('img/play.png'))
                                exi = 1
                                break
                            continue
                        if len(link) > cunt:
                            cunt += 1
                    if exi == 1:
                        break
                    time.sleep(60)
            _link = []
            Time = []
            chat = []
            Day = []
            conn = sqlite3.connect(f'{dirfile}\\Zoom.db')
            c = conn.cursor()

            for row in c.execute("SELECT * FROM Zoom;"):
                day = time.ctime().split(" ")[0]
                if day in  str(row[5]):
                    _link.append(row[2])
                    Time.append(row[3])
                    chat.append(row[4])
                    Day.append(row[5])
            setting = []
            for i in c.execute("SELECT * FROM setting"):
                setting.append(i[1])
                setting.append(i[2])
            

            if len(_link) == 0:
                pyautogui.alert("There is nothing for today", "Auto Zoom")
                self.pushButton.setIcon(QIcon('img/play.png'))
                return
            if len(_link) == len(Time) == len(chat):
                auto_zoom(_link, Time, chat,Day, setting)
        
        def SaveSetting(self):
            global dirfile 
            ow = self.lineEdit_4.text()
            oh = self.lineEdit_5.text()
            oi = self.lineEdit_6.text()
            cw = self.lineEdit_8.text()
            ch = self.lineEdit_9.text()
            ci = self.lineEdit_7.text()
        

            OpenZoom = ""
            chat = ""
            if len(ow) == 0 and len(oh) == 0 and len(oi) > 0:
                OpenZoom = oi

            elif len(ow) > 0 and len(oh) > 0 and len(oi) == 0:
                chack = "1234567890"
                c = 0
                for i in ow:
                    if i not in chack:
                        c = 1
                for i in oh:
                    if i not in chack:
                        c = 1
                if c  == 0:
                    OpenZoom = ow + "," + oh
                else:
                    self.label_26.setText("Please enter correct information, coordinates are numbers only")
                    return
            elif len(ow) == 0 and len(oh) == 0 and len(oi) == 0:
                pass
            else:
                self.label_26.setText("Please enter correct data, either coordinates or an image")
                return
            ####
            if len(cw) == 0 and len(ch) == 0 and len(ci) > 0:
                chat = ci

            elif len(cw) > 0 and len(ch) > 0 and len(ci) == 0:
                chack = "1234567890"
                c = 0
                for i in ow:
                    if i not in chack:
                        c = 1
                for i in oh:
                    if i not in chack:
                        c = 1
                if c  == 0:
                    chat = cw + ',' + ch
                else:
                    self.label_26.setText("Please enter correct information, coordinates are numbers only")
                    return
            elif len(cw) == 0 and len(ch) == 0 and len(ci) == 0:
                pass
            else:
                self.label_27.setText("Please enter correct data, either coordinates or an image")
                return
            db = sqlite3.connect(f"{dirfile}\\Zoom.db")
            db.execute("UPDATE setting SET OpenZoom= ? , chat = ?", (OpenZoom, chat))
            self.label_28.setText("Successfully updated")
            db.commit()
            db.close()
            
        def Default(self):
            global dirfile
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.label_28.setText("")
            self.label_27.setText("")
            self.label_26.setText("")
            _db = sqlite3.connect(f"{dirfile}\\Zoom.db")
            Dsetting = []
            for i in  _db.execute("Select * from Dsetting"):
                Dsetting.append(i[1])
                Dsetting.append(i[2])
            

            if "png" in Dsetting[0] or "jpg" in Dsetting[0]:
                self.lineEdit_6.setText(Dsetting[0])
            else:
                s = Dsetting[0].split(",")
                self.lineEdit_4.setText(s[0])
                self.lineEdit_5.setText(s[1])
            if "png" in Dsetting[1] or "jpg" in Dsetting[1]:
                self.lineEdit_7.setText(Dsetting[1])
            else:
                s = Dsetting[1].split(",")
                self.lineEdit_8.setText(s[0])
                self.lineEdit_9.setText(s[1])

            

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec_()
except Exception as z:
    import pyautogui as p
    p.alert(z, "Auto Zoom")
