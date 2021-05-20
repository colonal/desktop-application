
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication,  QSize, QThread, Qt, pyqtSignal
from PyQt5.QtGui import  QPixmap,QFont
from robobrowser import RoboBrowser
import sys, os
import urllib.request
import webbrowser

dirfile = os.environ['APPDATA']
if os.path.exists(f"{dirfile}\\anime4up") == False :
    os.mkdir(f"{dirfile}\\anime4up")
dirfile = f"{dirfile}\\anime4up"
lis = os.listdir(dirfile)
if len(lis) > 0:
    for i in lis:
        os.remove(dirfile+"\\"+i)


URL = "https://ww.anime4up.com/?search_param=animes&s="
DATA = {}
stopthread = 0

class Thread(QThread):
    Data = pyqtSignal(dict)
    

    def run(self):
        global DATA, stopthread
        url = []
        try:
            self.browser = RoboBrowser(parser="lxml", history=True)
            self.browser.open(URL)
            a = self.browser.find_all("div", {"class":"col-lg-3 col-md-3 col-sm-12 col-xs-12 col-no-padding col-mobile-no-padding DivEpisodeContainer"})
            print(a)
            if a == 0:
                print("Sorry, no contents found!")
            for i in a:
                if stopthread == 1:
                    stopthread = 0
                    return
                url.append(i.find("a").get("href"))
        except Exception as E:
            print(E)
        linkes = []
        data = {}
        c = 1       
        for u in url:
            if stopthread == 1:
                    stopthread = 0
                    return
            try:
                self.browser.open(u)
                
                li = self.browser.select('iframe', attrs={})
                for link in li:
                    if stopthread == 1:
                        stopthread = 0
                        return
                    data = {}
                    linkes.append(link.get('src'))
                    data[f"Episode:{c}"]= link.get('src')
                    DATA[f"Episode:{c}"]= link.get('src')
                    print(f"Episode:{c}\t url: ",link.get('src'))
                    self.Data.emit(data)
                c += 1
            except Exception as E:
                    print("Error ", E)

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class MYapp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.MainUI()
        self.VMain = QVBoxLayout()
        
        self.setWindowFlags(Qt.FramelessWindowHint) # Remove title bar

        self._translate = QCoreApplication.translate
        self.thread = Thread()
        self.thread.Data.connect(self.setURL)
        self.setGeometry(400,100,300,400)
        self.TopBar()
        self.MainSearch()
        self.createLayout_Container()
        self.maxNormal=False
        self.URL = ""
        self.count = 0
        self.ConnectBotton()
        
        self.setLayout(self.VMain)
        self.installEventFilter(self)
        self.show()
        
        
        
    def TopBar(self):
        self.H = QHBoxLayout()
        self.H1 = QHBoxLayout()
        self.btn_maximize = QPushButton()
        self.btn_maximize.setMinimumSize(QSize(16, 16))
        self.btn_maximize.setMaximumSize(QSize(17, 17))
        self.btn_maximize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;    \n"
"    background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(85, 255, 127, 150);\n"
'    background-image: url("img/maximize1.png");' 
"    background-repeat: no-repeat; \n"
"    background-position: center;\n"
"}")
        
        
        
        self.btn_minimize = QPushButton()
        self.btn_minimize.setMinimumSize(QSize(16, 16))
        self.btn_minimize.setMaximumSize(QSize(17, 17))
        self.btn_minimize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;        \n"
"    background-color: rgb(255, 170, 0);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(255, 170, 0, 150);\n"
'    background-image: url("img/minimize.png");' 
"    background-repeat: no-repeat; \n"
"    background-position: center;\n"
"}")
        self.btn_close = QPushButton()
        self.btn_close.setMinimumSize(QSize(16, 16))
        self.btn_close.setMaximumSize(QSize(17, 17))
        self.btn_close.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;        \n"
"    background-color: rgb(255, 0, 0);\n"
"}\n"
"QPushButton:hover {        \n"
"    background-color: rgba(255, 0, 0, 150);\n"
'    background-image: url("img/close5.png");' 
"    background-repeat: no-repeat; \n"
"    background-position: center;\n"
"}")
        
        
        self.H.addWidget(self.btn_minimize)
        self.H.addWidget(self.btn_maximize)
        self.H.addWidget(self.btn_close)
        
        self.label_title = QLabel()
        pixmap = QPixmap("img\\anime4up.png")
        smaller_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_title.setPixmap(smaller_pixmap)
        
        self.H1.addWidget(self.label_title)
        self.H1.addLayout(self.H)
        self.VMain.addLayout(self.H1)
        self.VMain.addWidget(QHLine())
        self.VMain.addStretch()
        
    def MainUI(self):
        self.setStyleSheet("""
            background-color: rgb(77, 77, 127);
            color: #ffffff;""")
    
    def MainSearch(self):
        VMainSearch = QVBoxLayout()
        VSearch = QVBoxLayout()
        HSearch = QHBoxLayout()
        self.labilSearch= QLabel() 
        self.EntrySearch = QLineEdit()
        self.ButtonSearsh = QPushButton()
        
        
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.labilSearch.setFont(font)
        self.labilSearch.setStyleSheet("color: #FFFFFF; background-color: none;")
        self.labilSearch.setAlignment(Qt.AlignCenter)
        self.labilSearch.setText(self._translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Search</span> Anime</p></body></html>"))
        
        
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QFont.PreferDefault)
        self.ButtonSearsh.setFont(font)
        self.ButtonSearsh.setStyleSheet(" \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:rgb(77, 77, 127);\n"
"")
        self.ButtonSearsh.setText(self._translate("MainWindow", "Search"))
        
        self.EntrySearch.setFont(font)
        self.EntrySearch.setStyleSheet("background-color: rgb(45, 45, 74);")
        
        VSearch.addWidget(self.EntrySearch)
        VSearch.addWidget(self.ButtonSearsh)
        VSearch.setContentsMargins(0, 20, 0, 20)
        
        HSearch.addStretch()
        HSearch.addLayout(VSearch)
        HSearch.addStretch()
        
        VMainSearch.addWidget(self.labilSearch)
        
        VMainSearch.addLayout(HSearch)
        #VMainSearch.addStretch()

        VMainSearch.setContentsMargins(0, 20, 0, 0)
        
        
        self.VMain.addLayout(VMainSearch)
        self.VMain.addStretch()
        
    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.hide()
        self.scrollarea.setFixedHeight(250)
        #self.scrollarea.resize(500,500)
        self.scrollarea.setWidgetResizable(True)
        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QGridLayout(widget)
        self.layout_SArea.setContentsMargins(20, 5, 20, 5)
        h = QVBoxLayout()
        h.addWidget(self.scrollarea)
        
        
        
        self.VMain.addLayout(h)
        self.VMain.addStretch()
    def createLayout_group(self, LEN, data, dataSrc):
        print(LEN)
        c = 0
        for i in data: #row
            #for j in range(3): # colon
            label = QLabel()
            pixmap = QPixmap(dataSrc[i])
            smaller_pixmap = pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
            label.setPixmap(smaller_pixmap)
            but = QPushButton(f"{i}")
            but.setFixedHeight(90)
            but.setContentsMargins(10, 10, 10, 30)
            but.clicked.connect(self.Click)
            self.layout_SArea.addWidget(label, c, 0)
            self.layout_SArea.addWidget(but, c, 1)
            c += 1
        #return bouttn
    
    def SearshAnime(self):
        global stopthread
        self.browser = RoboBrowser(parser="lxml", history=True)
        if self.thread.isRunning():
            stopthread = 1
            self.thread.quit()
            self.thread.exit()
        for i in reversed(range(self.layout_SArea.count())): 
            self.layout_SArea.itemAt(i).widget().setParent(None)

        site = "https://ww.anime4up.com/?search_param=animes&s="
        
        s = site+self.EntrySearch.text()
        self.browser.open(s)
        name = self.browser.find_all("div",{"class":"col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding"})
        #print(name)
        data = {}
        dataSrc = {}
        for i in name:
            url = i.find("h3").find("a").get("href")
            titil = i.find("h3").find("a").text
            img = i.find("img").get("src")
            m = f"{dirfile}\\{titil.replace(':','')}"+".png"
            print(m)
            try:
                urllib.request.urlretrieve(img,m)
                dataSrc[titil] = m
            except:
                dataSrc[titil] = ""
            data[titil] = url
        self.SearchData = data
        
        print(self.thread.isRunning())
        self.createLayout_group(len(name), data, dataSrc)
        self.scrollarea.show()
        
    def ConnectBotton(self):
        self.ButtonSearsh.clicked.connect(self.SearshAnime)
        self.btn_close.clicked.connect(self.Btn_close)
        self.btn_minimize.clicked.connect(self.Btn_minimize)
        self.btn_maximize.clicked.connect(self.Btn_maximize)
        
    def Btn_close(self):
        sys.exit()
    
    def Btn_minimize(self):
        self.showMinimized()
    
    def Btn_maximize(self):
        if(self.maxNormal):
            self.showNormal()
            self.maxNormal= False
            #self.maximize.setIcon(QIcon('img/max.png'))
            self.btn_maximize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;    \n"
"    background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(85, 255, 127, 150);\n"
'    background-image: url("img/maximize1.png");' 
"    background-repeat: no-repeat; \n"
"    background-position: center;\n"
"}")
            print('1')
        else:
            self.showMaximized()
            self.maxNormal=  True
            print('2')
            #self.maximize.setIcon(QIcon('img/max2.png'))
            self.btn_maximize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;    \n"
"    background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(85, 255, 127, 150);\n"
'    background-image: url("img/maximize3.png");' 
"    background-repeat: no-repeat; \n"
"    background-position: center;\n"
"}")
    
    def Click(self):
        global URL, stopthread
        ButtonId = self.sender().text()
        if "Episode:" not in ButtonId:
            stopthread = 0
            print(self.SearchData[ButtonId])
            try:
                URL = self.SearchData[ButtonId]
                self.count = 0
                for i in reversed(range(self.layout_SArea.count())): 
                    self.layout_SArea.itemAt(i).widget().setParent(None)
                self.thread.start()
            except Exception as E:
                print("Error ", E)
        else:
            print(DATA[ButtonId])
            webbrowser.open_new_tab(DATA[ButtonId])
    def close(self):
        self.close()
    def setURL(self, value):
        for i in value: #row
            but = QPushButton(f"{i}")
            but.setContentsMargins(20, 10, 20, 10)
            but.clicked.connect(self.Click)
            self.layout_SArea.addWidget(but, self.count, 0)
            self.count += 1

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.moving:
            self.move(event.globalPos()-self.offset)
    
    
    
    
app = QApplication(sys.argv)
window = MYapp()
sys.exit(app.exec_())