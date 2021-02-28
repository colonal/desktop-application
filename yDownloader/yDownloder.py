import sys,os, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices,QFont
import pafy
from natural.size import filesize
from  urllib.request import urlretrieve
import threading
import googleapiclient.discovery
from win10toast import ToastNotifier 
from apiclient import discovery
import mysql.connector
import sqlite3
from urllib.parse import parse_qs, urlparse
import re
from hashlib import sha256
import  subprocess


path = os.environ['APPDATA'] + "\\YDownloader"
pathDB = os.environ['APPDATA'] + "\\YDownloader\\DB"
pathTmp = os.environ['APPDATA'] + "\\YDownloader\\imgVideo"
pathProcessing = os.environ['APPDATA'] + "\\YDownloader\\ProcessingVideo"
icon = r"img\YDownloader.ico"
path_home = os.getcwd()
n = ToastNotifier()
TITLE = "yDownloder"
MESSAGE = "An unknown error occurred, try again"
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
IDUser = 0
paypal = ""
_Histori = {}




class Window(QWidget):
    finished = pyqtSignal()
    finished1 = pyqtSignal()
    finished2 = pyqtSignal()
    finished3 = pyqtSignal()
    finished4 = pyqtSignal()
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("yDownloader")
        self.setWindowIcon(QIcon("img\\YDownloader.ico"))
        self.setGeometry(200, 60, 610,400)
        self.UI()
        self.finished.connect(self.on_finished, Qt.QueuedConnection)
        self.finished1.connect(self.on_CProgress, Qt.QueuedConnection)
        self.finished2.connect(self.on_PProgress, Qt.QueuedConnection)
        self.finished3.connect(self.on_Progress, Qt.QueuedConnection)
        self.finished4.connect(self.on_History, Qt.QueuedConnection)
        self.DB_Connect()
        
        

    def UI(self):
        self.widgets()
        self.Staylmain()
        self.ButtonConnect()

    def on_finished(self):
        QMessageBox.information(self,TITLE,MESSAGE)
    def on_CProgress(self):
        self.CProgress.setValue(0)
        self.CProgress.setFormat("")
    def on_PProgress(self):
        self.PProgress.setValue(0)
        self.PProgress.setFormat("")
    def on_Progress(self):
        self.Progress.setValue(0)
        self.Progress.setFormat("")
    def on_History(self):
        self.setTable()
    
    def vidoButTap(self):
        self.tabs.setCurrentIndex(0)
    def playlistButTap(self):
        self.tabs.setCurrentIndex(1)
    def channelButTap(self):
        self.tabs.setCurrentIndex(2)
    def historyButTap(self):
        self.on_History()
        self.tabs.setCurrentIndex(4)
    def backeHistoryButTap(self):
        self.tabs.setCurrentIndex(3)
    def accountButTap(self):
        count = self.tabsChannel.currentIndex()
        if count == 0:
            self.tabs.setCurrentIndex(2)
        else:
            self.tabs.setCurrentIndex(3)
    def LoginSTap(self):
        self.tabsAccount.setCurrentIndex(0)
    def SignupTap(self):
        self.tabsAccount.setCurrentIndex(1)
    

    def widgets(self):
        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        tabLayout = QHBoxLayout()
        buttonV = QVBoxLayout()
        
        self.tabs = QTabWidget()
        buttonLayout.addLayout(buttonV, 15)
        buttonLayout.addLayout(tabLayout, 85)
        self.tabs.tabBar().setVisible(False)
        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tabs.addTab(self.tab1, "First Tab")
        self.tabs.addTab(self.tab2, "Second Tab")
        self.tabs.addTab(self.tab3, "Last Tap")
        self.tabs.addTab(self.tab4, "Last Tap")
        self.tabs.addTab(self.tab5, "Last Tap")
        # ################# widget #############
    
        vbox = QVBoxLayout()
        hbox_title = QHBoxLayout()
        hbox_img = QHBoxLayout()
        hbox_prs = QHBoxLayout()
        hbox_start = QHBoxLayout()

        # ################################# TouTuop Vidoe
        self.FormVidow = QFormLayout()
        self.FormVidow.setSpacing(20)
        self.FormVidow.setContentsMargins(10, 40, 10, 10)
        
        self.urlL = QLabel("URL")
        self.urlE = QLineEdit()
        self.urlS = QPushButton("Search")
        self.urlLayout = QHBoxLayout()

        self.urlLayout.addWidget(self.urlE)
        self.urlLayout.addWidget(self.urlS)
        self.FormVidow.addRow(self.urlL, self.urlLayout)
        
        

        self.saveL = QLabel("Save")
        self.saveE = QLineEdit()
        self.saveP = QPushButton("Browse")
        self.saveLayout = QHBoxLayout()

        self.saveLayout.addWidget(self.saveE)
        self.saveLayout.addWidget(self.saveP)
        self.FormVidow.addRow(self.saveL, self.saveLayout)


        self.qualtyL = QLabel("Qualty")
        self.qualtyE = QComboBox()
        self.qualtyE.addItems(["",])
        self.qualtyB = QCheckBox("Download Thumbnail")
        self.qualtyLayout = QHBoxLayout()
 
        self.qualtyLayout.addWidget(self.qualtyE)
        self.qualtyLayout.addWidget(self.qualtyB)
        self.FormVidow.addRow(self.qualtyL, self.qualtyLayout)
        vbox.addLayout(self.FormVidow)


        self.title = QLabel("Title: ")
        hbox_title.addWidget(self.title)
        hbox_title.setContentsMargins(10, 10, 10, 10)
        vbox.addLayout(hbox_title)

        self.img = QPixmap("img\\xXx.png")
        self.smaller_pixmap = self.img.scaled(90, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
        
        
        self.imgV = QLabel("img")
        self.imgV.setAlignment(Qt.AlignCenter)
        self.imgV.setPixmap(self.smaller_pixmap)
        hbox_img.addWidget(self.imgV)
        vbox.addLayout(hbox_img)


        self.Progress = QProgressBar()
        self.Progress.setAlignment(Qt.AlignCenter)
        hbox_prs.addStretch()
        hbox_prs.addWidget(self.Progress)
        self.Progress.setFixedSize(400, 20)
        vbox.addLayout(hbox_prs)
        hbox_prs.addStretch()


        self.start = QPushButton("Start Download")
        self.start.setFixedSize(150, 30)
        
        
        hbox_start.addWidget(self.start, alignment=Qt.AlignCenter)
        vbox.addLayout(hbox_start)
        # ##################################### End TouTuop Vidoe
        ############### buttonTab
        self.vidoBut = QPushButton("Vidoe")
        self.playlistBut = QPushButton("PlayList")
        self.channelBut = QPushButton("Channel")
        self.accountBut = QPushButton("Account")
        

        buttonV.addWidget(self.vidoBut)
        buttonV.addWidget(self.playlistBut)
        buttonV.addWidget(self.channelBut)
        buttonV.addWidget(self.accountBut)
        
        ############################# start PlayList
        vboxP = QVBoxLayout()
        FormPlaylist = QFormLayout()
        vboxP.addLayout(FormPlaylist)
        FormPlaylist.setSpacing(20)
        FormPlaylist.setContentsMargins(10, 40, 10, 10)


        self.PurlL = QLabel("URL")
        self.PurlE = QLineEdit()
        FormPlaylist.addRow(self.PurlL,self.PurlE)

        self.PsaveL = QLabel("Save")
        self.PsaveE = QLineEdit()
        self.PsaveP = QPushButton("Browse")
        self.PsaveP.setContentsMargins(10, 0, 10, 0)
        hboxPsave = QHBoxLayout()
        hboxPsave.addWidget(self.PsaveE)
        hboxPsave.addWidget(self.PsaveP)
        FormPlaylist.addRow(self.PsaveL, hboxPsave)

        self.PqualtyL = QLabel("Qualty")
        self.PqualtyE = QComboBox()
        self.PqualtyE.addItems(["Normal", "1080 P", "720 P", "480 P", "360 P", "240 P", "144 P", "Audio"])
        self.PqualtyC = QCheckBox("Download Thumbnail")
        self.PqualtyC.setContentsMargins(10, 0, 0, 0)
        hboxPqualty = QHBoxLayout()
        hboxPqualty.addWidget(self.PqualtyE)
        hboxPqualty.addWidget(self.PqualtyC)
        FormPlaylist.addRow(self.PqualtyL, hboxPqualty)

        self.Ptitle = QLabel("Title:")
        hbox_Ptitle = QHBoxLayout()
        hbox_Ptitle.addWidget(self.Ptitle)
        hbox_Ptitle.setContentsMargins(10, 10, 10, 10)
        vboxP.addLayout(hbox_Ptitle)


        self.PimgL = QLabel("Current video")
        hbox_PimgL = QHBoxLayout()
        hbox_PimgL.addWidget(self.PimgL)
        vboxP.addLayout(hbox_PimgL)
        
        
        self.Pimg = QLabel("img")
        self.Pimg.setFixedSize(150, 150)
        self.Pimg.setAlignment(Qt.AlignCenter)
        self.Pimg.setPixmap(self.smaller_pixmap)
        hbox_Pimg = QHBoxLayout()
        hbox_Pimg.addWidget(self.Pimg)
        
        vboxP.addLayout(hbox_Pimg)


        self.PProgress = QProgressBar()
        self.PProgress.setAlignment(Qt.AlignCenter)
        hbox_Pprs = QHBoxLayout()
        hbox_Pprs.addStretch()
        hbox_Pprs.addWidget(self.PProgress)
        self.PProgress.setFixedSize(400, 20)
        vboxP.addLayout(hbox_Pprs)
        hbox_Pprs.addStretch()


        self.Pstart = QPushButton("Start Download")
        self.Pstart.setFixedSize(150, 30)
        hbox_Pstart = QHBoxLayout()
        hbox_Pstart.addWidget(self.Pstart, alignment=Qt.AlignCenter)
        vboxP.addLayout(hbox_Pstart)
        
        

        self.tab2.setLayout(vboxP)
        ############################# end PlayList
        ############################# starrt channel
        vboxChannel = QVBoxLayout()
        self.tabsChannel = QTabWidget()
        self.tabsChannel.tabBar().setVisible(False)
        vboxChannel.addWidget(self.tabsChannel)
        self.tab3.setLayout(vboxChannel)
        
        self.tabChannel1 = QWidget()
        self.tabChannel2 = QWidget()
        self.tabChannel3 = QWidget()

        self.tabsChannel.addTab(self.tabChannel1, "First Tab")
        self.tabsChannel.addTab(self.tabChannel2, "Second Tab")
        self.tabsChannel.addTab(self.tabChannel3, "Last Tap")
        vboxC = QVBoxLayout()
        self.tabChannel1.setLayout(vboxC)

        self.tabsAccount = QTabWidget()
        self.tabsAccount.tabBar().setVisible(False)

        self.tabsAccount1 = QWidget()
        self.tabsAccount2 = QWidget()

        self.tabsAccount.addTab(self.tabsAccount1, "First tab")
        self.tabsAccount.addTab(self.tabsAccount2, "Second tab")

        vboxC.addWidget(self.tabsAccount)
        
        forimAccount = QFormLayout()
        forimAccount.setVerticalSpacing(50)
        forimAccount.setContentsMargins(0, 80, 0, 0)
        
        
        
        self.emalE = QLineEdit()
        self.emalE.setPlaceholderText("Enter yuor Mail")

        self.passwordE = QLineEdit()
        self.passwordE.setPlaceholderText("Enter Yuor Password")
        self.passwordE.setEchoMode(QLineEdit.Password)

        self.Login = QPushButton("Login")
        self.Signup = QPushButton("Signup")

        forimAccount.addRow(QLabel("E-mail"), self.emalE)
        forimAccount.addRow(QLabel("Password"), self.passwordE)
        forimAccount.addRow( self.Signup, self.Login)
        
        self.tabsAccount1.setLayout(forimAccount)

        forimAccount1 = QFormLayout()
        forimAccount1.setVerticalSpacing(50)
        forimAccount1.setContentsMargins(0, 80, 0, 0)
        HBOx = QHBoxLayout()

        fistName = QLabel("First Name ")
        self.FName = QLineEdit()
        HBOx.addWidget(self.FName)

        lastName = QLabel("Last Name")
        self.SName = QLineEdit()
        HBOx.addWidget(lastName)
        HBOx.addWidget(self.SName)

        self.emalES = QLineEdit()
        self.passwordES = QLineEdit()
        self.passwordES.setEchoMode(QLineEdit.Password)
        self.rewrite = QLineEdit()
        self.rewrite.setEchoMode(QLineEdit.Password)

        self.CreatAccount = QPushButton("Create an account")
        self.LoginS = QPushButton("Login")

        forimAccount1.addRow(fistName,HBOx)
        forimAccount1.addRow(QLabel("E-mail"), self.emalES)
        forimAccount1.addRow(QLabel("Password"), self.passwordES)
        forimAccount1.addRow(QLabel("Rewrite"), self.rewrite)
        forimAccount1.addRow(self.LoginS, self.CreatAccount)

        self.tabsAccount2.setLayout(forimAccount1)

        VBoxactv = QVBoxLayout()
        VBoxactv.setContentsMargins(0,0,0,30)
        HBoxactv = QHBoxLayout()
        HBoxactv.setContentsMargins(0, 20, 0, 40)
        self.LableMessge = QLabel("""This service is free now\n""")
        self.LableMessge1 = QLabel("""
You can support us by sending money via Paypal
Or you can skip this by inserting (colonel)\n
Thank you We wish you an enjoyable use\n""")
        self.paypal = QPushButton()
        self.paypal.setIcon(QIcon('img\paypal.png'))
        self.paypal.setIconSize(QSize(540, 50))
        self.wep = QLabel("")
        self.wep.setOpenExternalLinks(True)
        self.wep.setAlignment(Qt.AlignCenter)
        self.wep.setContentsMargins(0, 30, 0, 10)

        Activation = QLabel("Activation Code")
        self.ActivationL = QLineEdit()
        HBoxactv.addWidget(Activation)
        HBoxactv.addWidget(self.ActivationL)

        self.ActivationP = QPushButton("Activation")
        self.ActivationP.setStyleSheet("QPushButton{height: 22px;}")

        #
        VBoxactv.addWidget(self.LableMessge)
        VBoxactv.addWidget(self.LableMessge1)
        VBoxactv.addStretch()
        VBoxactv.addWidget(self.paypal)
        VBoxactv.addWidget(self.wep)
        VBoxactv.addLayout(HBoxactv)
        VBoxactv.addWidget(self.ActivationP)
        VBoxactv.addStretch()
        
        self.tabChannel2.setLayout(VBoxactv)
        # tab Download channel ########################
        vboxC = QVBoxLayout()
        FormPlayC = QFormLayout()
        vboxC.addLayout(FormPlayC)
        #FormPlaylist.setVerticalSpacing(20)
        FormPlayC.setSpacing(20)
        FormPlayC.setContentsMargins(10, 40, 10, 10)


        self.CurlL = QLabel("URL")
        self.CurlE = QLineEdit()
        FormPlayC.addRow(self.CurlL,self.CurlE)

        self.CsaveL = QLabel("Save")
        self.CsaveE = QLineEdit()
        self.CsaveP = QPushButton("Browse")
        self.CsaveP.setContentsMargins(10, 0, 10, 0)
        hboxCsave = QHBoxLayout()
        hboxCsave.addWidget(self.CsaveE)
        hboxCsave.addWidget(self.CsaveP)
        FormPlayC.addRow(self.CsaveL, hboxCsave)

        self.CqualtyL = QLabel("Qualty")
        self.CqualtyE = QComboBox()
        self.CqualtyE.addItems(["Normal", "1080 P", "720 P", "480 P", "360 P", "240 P", "144 P", "Audio"])
        self.CqualtyC = QCheckBox("Download Thumbnail")
        self.CqualtyC.setContentsMargins(10, 0, 0, 0)
        hboxCqualty = QHBoxLayout()
        hboxCqualty.addWidget(self.CqualtyE)
        hboxCqualty.addWidget(self.CqualtyC)
        FormPlayC.addRow(self.CqualtyL, hboxCqualty)

        self.Ctitle = QLabel("Title:")
        hbox_Ctitle = QHBoxLayout()
        hbox_Ctitle.addWidget(self.Ctitle)
        hbox_Ctitle.setContentsMargins(10, 10, 10, 10)
        vboxC.addLayout(hbox_Ctitle)


        self.CimgL = QLabel("Current video")
        hbox_CimgL = QHBoxLayout()
        hbox_CimgL.addWidget(self.CimgL)
        vboxC.addLayout(hbox_CimgL)
        
        
        self.Cimg = QLabel("img")
        self.Cimg.setFixedSize(150, 150)
        self.Cimg.setAlignment(Qt.AlignCenter)
        self.Cimg.setPixmap(self.smaller_pixmap)
        hbox_Cimg = QHBoxLayout()
        hbox_Cimg.addWidget(self.Cimg)
        
        vboxC.addLayout(hbox_Cimg)


        self.CProgress = QProgressBar()
        self.CProgress.setAlignment(Qt.AlignCenter)
        hbox_Cprs = QHBoxLayout()
        hbox_Cprs.addStretch()
        hbox_Cprs.addWidget(self.CProgress)
        self.CProgress.setFixedSize(400, 20)
        vboxC.addLayout(hbox_Cprs)
        hbox_Cprs.addStretch()


        self.Cstart = QPushButton("Start Download")
        self.Cstart.setFixedSize(150, 30)
        hbox_Cstart = QHBoxLayout()
        hbox_Cstart.addWidget(self.Cstart, alignment=Qt.AlignCenter)
        vboxC.addLayout(hbox_Cstart)

        self.tabChannel3.setLayout(vboxC)


    

        ############################# end channel
        ###################### start tab Account
        vboxAcount = QVBoxLayout()
        formAcount = QFormLayout()
        formAcount.setVerticalSpacing(30)
        formAcount.setContentsMargins(0,80,0,40)
        h = QHBoxLayout()
        f = QFrame()
        self.history = QPushButton()
        h.addWidget(self.history)
        f.setLayout(h)
        h.setAlignment(Qt.AlignRight)
        self.NameA = QLabel()
        self.MailA = QLabel()
        self.activationA = QLabel()
        self.ProductID = QLabel()
        self.statA = QLabel("Allowed number of devices 3, you have 3 left")
        self.statA.setContentsMargins(0, 0, 0, 20)
        self.logout = QPushButton("Log out")

        formAcount.addRow(QLabel("Name: "), self.NameA)
        formAcount.addRow(QLabel("Mail: "), self.MailA)
        formAcount.addRow(QLabel("Account is activation: "),self.activationA)
        formAcount.addRow(QLabel("Product ID: "),self.ProductID)
        formAcount.addRow(self.statA)

        ###
        self.Img = QPixmap("img\\logo.png")
        self.Smaller_pixmap = self.Img.scaled(150, 50, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.logo = QLabel(self)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setPixmap(self.Smaller_pixmap)
        self.logo.resize(50,50)
        self.logo.move(0,10)
        self.logo1 = QLabel()
        self.logo1.setAlignment(Qt.AlignCenter)
        self.logo1.setText('<html><head/><body><p><span style=" font-size:18pt; font-weight:600;">c o l o n a l</span></p></body></html>')
        self.logo1.setFont(QFont("Algerian"))
        ###
        vboxAcount.addWidget(f)
        vboxAcount.addLayout(formAcount)
        vboxAcount.addWidget(self.statA)
        vboxAcount.addWidget(self.logout)
        vboxAcount.addStretch()
        vboxAcount.addWidget(self.logo1)
        self.tab4.setLayout(vboxAcount)


        
        self.tab1.setLayout(vbox)
        
        tabLayout.addWidget(self.tabs)
        self.setLayout(buttonLayout)
        
        ###################### history
        VBoxH = QVBoxLayout()
        HBOxH = QHBoxLayout()
        self.HTable = QTableWidget()
        self.HTable.setColumnCount(3)
        self.HTable.setHorizontalHeaderItem(0, QTableWidgetItem("NAME"))
        self.HTable.setHorizontalHeaderItem(1, QTableWidgetItem("PATH"))
        self.HTable.setHorizontalHeaderItem(2, QTableWidgetItem("TIME"))
        self.HTable.horizontalHeader().setStretchLastSection(True) 
        self.HTable.horizontalHeader().setSectionResizeMode( QHeaderView.Stretch)

        self.backH = QPushButton("BACKE")
        self.deleteH = QPushButton("DELETE")
        
        VBoxH.addWidget(self.HTable)
        HBOxH.addWidget(self.backH)
        HBOxH.addWidget(self.deleteH)
        VBoxH.addLayout(HBOxH)
        self.tab5.setLayout(VBoxH)
        

    def Staylmain(self):
        try:
            with open("stayl\\stayl.css", "r") as L:
                self.setStyleSheet(L.read())
        except:
            pass
        self.setStyleSheet("QLabel{font: 12px;text-align: justify;}")
        self.setStyleSheet("QPushButton{font: 12px;text-align: justify;}")
        self.LableMessge.setStyleSheet("""QLabel{border: 1px solid gray;padding: 8px;
        font: 14px bold ;
        text-align: center;
        text-transform: uppercase;
        color: #4CAF50;}""")
        self.LableMessge.setAlignment(Qt.AlignCenter)
        self.LableMessge.setContentsMargins(0,10,0,0)
        self.LableMessge1.setStyleSheet("""QLabel{border: 1px solid gray;padding: 8px;
        font: 12px;
        text-indent: 50px;
        text-align: justify;
        letter-spacing: 3px;}""")
        self.LableMessge1.setContentsMargins(0,0,0,0)
        self.vidoBut.setStyleSheet("QPushButton{ height: 20px;text-align: center;}")
        self.playlistBut.setStyleSheet("QPushButton{height: 20px;text-align: center;}")
        self.channelBut.setStyleSheet("QPushButton{height: 20px;text-align: center;}")
        self.accountBut.setStyleSheet("QPushButton{height: 20px;text-align: center;}")
        
        self.history.setFixedSize(10,48)
        
        self.history.setStyleSheet("""QPushButton{
                                        background-color: #19232D;background-image : url('img//history7.png');
                                        background-repeat: no-repeat;border-color:#19232D;
                                        text-align: center;}
                                    QPushButton:hover {
                                        background-color: #19232D;background-image : url('img//history8.png');
                                        border: 1px solid #148CD2;
                                        color: #F0F0F0;}
                                    QPushButton:pressed {
                                        background-color: #19232D;background-image : url('img//history7.png');
                                        background-color: #243342;
                                        border: 1px solid #19232D;
                                        }""")

    
    def ButtonConnect(self):
        self.urlS.clicked.connect(self.runVideoSearch)
        self.saveP.clicked.connect(self.VideoSearchBrowse)
        self.start.clicked.connect(self.runVideoDownload)
        self.Pstart.clicked.connect(self.rundownloadVidoList)
        self.PsaveP.clicked.connect(self.VideoListSearchBrowse)
        self.paypal.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(f"{paypal}"))
        )
        self.CsaveP.clicked.connect(self.ChannelSearchBrowse)
        self.Cstart.clicked.connect(self.rundownloadVidoChannel)
        self.vidoBut.clicked.connect(self.vidoButTap)
        self.playlistBut.clicked.connect(self.playlistButTap)
        self.channelBut.clicked.connect(self.channelButTap)
        self.accountBut.clicked.connect(self.accountButTap)
        self.LoginS.clicked.connect(self.LoginSTap)
        self.Signup.clicked.connect(self.SignupTap)
        self.Login.clicked.connect(self.LOGIN)
        self.CreatAccount.clicked.connect(self.SIGNUP)
        self.ActivationP.clicked.connect(self.ActivationPcheck)
        self.logout.clicked.connect(self.Logout)
        self.history.clicked.connect(self.historyButTap)
        self.backH.clicked.connect(self.backeHistoryButTap)
        self.deleteH.clicked.connect(self.deleteHistory)

    ################################################################## Start processing download video
    def VideoSearchBrowse(self):
        save_place = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.saveE.setText(save_place)
    def runVideoSearch(self):
        self.urlS.setText("Processing...")
        threading.Thread(target=self.VideoSearch).start()
        self.qualtyE.setCurrentIndex(0)
    
    def VideoSearch(self):
        global MESSAGE
        videoLink = self.urlE.text()
        if len(videoLink) == 0:
            MESSAGE = "Enter the video URL"
            self.finished.emit()
            self.urlS.setText("Search")
            return
        try:
            video = None
            try:
                video = pafy.new(videoLink)
            except Exception as E:
                MESSAGE = "The link you entered is not valid, please check it and try again"
                self.finished.emit()
                self.urlS.setText("Search")
                return
            
            
            title = video.title
            img = video.thumb
            videoStreams = video.allstreams
            
            self.title.setText("Title: "+title)
            
            urlretrieve(img, f"{pathTmp}\\img1.jpg")
            img = QPixmap(f"{pathTmp}\\img1.jpg")
            smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.imgV.setPixmap(smaller_pixmap)
            
            self.qualtyE.clear()
            for s in videoStreams:
                size = filesize(s.get_filesize())
                data = f'{s.mediatype}  {s.extension}  {s.quality}  {size}'
                self.qualtyE.addItem(data)
            self.urlS.setText("Search")
        except Exception as Error:
            
            MESSAGE = f"The link you entered is not valid, please check it and try again\n\n{Error}"
            self.finished.emit()
            self.urlS.setText("Search")

    

    def VideoProgressBar(self, total, recvd, ratio, rate, eta):
        k = recvd / total
        suo = k * 100
        self.Progress.setValue(suo)
        self.Progress.setFormat(f"{int(suo)}")
    
    def runVideoDownload(self):
        self.start.setText("Downloading ...")
        threading.Thread(target=self.VideoDownload).start()
    def downloadVideo(self, video):
        video.download(filepath=pathProcessing, quiet=True, callback= self.VideoProgressBar)
    def downloadAudio(self,Audio):
        Audio.download(filepath=pathProcessing, quiet=True, callback= self.VideoProgressBar)
    def videoProcess(self, pwd):
        global MESSAGE
        try:
            x = os.listdir(pathProcessing)
            video = '"'+pathProcessing+"\\"+x[1] + '"'
            audio = '"'+pathProcessing+"\\"+x[0] + '"'
            video_path = '"{}\{}"'.format(pwd, x[1])
            self.Progress.setFormat("Processing...")
            
            cmd = f'ffmpeg -i {video} -i {audio} -c:v copy -c:a aac {video_path}  -loglevel quiet -hide_banner'
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                realtime_output = process.stdout.readline()

                if realtime_output == '' and process.poll() is not None:
                    break
                if realtime_output:
                    pass

            
            time.sleep(1)
            if len(x) > 0:
                for i in x:
                    os.remove(pathProcessing+"\\"+i)
            self.finished3.emit()

        except Exception as x:

            MESSAGE = "An unknown error has occurred, try again"
            self.finished.emit()

    def rundownloadVideoAudio(self, video, audio,pwd):
        self.downloadVideo(video)
        self.downloadAudio(audio)
        return self.videoProcess(pwd)
    def VideoDownload(self):
        global MESSAGE, _Histori
        try:
        
            url = self.urlE.text()
            pwd = self.saveE.text()
            qualty = self.qualtyE.currentIndex()
            
            if len(url) == 0 :
                MESSAGE = "Enter the video URL"
                self.finished.emit()
                return
            if len(pwd) == 0 :
                MESSAGE = "Select where to download the video"
                self.finished.emit()
                return
            if len(str(qualty)) == 0 :
                MESSAGE = "Choose the quality in which you want to download the video"
                self.finished.emit()
                return
            if os.path.exists(f"{pwd}") == False:
                MESSAGE ="The storage location does not exist. Please check it and try again"
                self.finished.emit()
                self.urlS = QPushButton("Search")
                return
            try:
                video = pafy.new(url)
            except Exception as E:
                MESSAGE = f"The link you entered is not valid, please check it and try again\n\n{E}"
                self.finished.emit()
            videoStreams = video.allstreams
            title = video.title
            _img = video.thumb


            if "normal" in str(videoStreams[qualty]) or "audio" in str(videoStreams[qualty]):
                
                videoStreams[qualty].download(filepath=pwd, quiet=True, callback= self.VideoProgressBar)
                self.Progress.clearFocus()
                self.finished3.emit()
                
            
            if "video" in str(videoStreams[qualty]):
                Video = videoStreams[qualty]
                audio = video.m4astreams
                lis = os.listdir(pathProcessing)
                if len(lis) > 0:
                    for i in lis:
                        os.remove(pathProcessing+"\\"+i)
                try:
                    self.rundownloadVideoAudio(Video, audio[0], pwd)
                except Exception as Error:
                    v = video.getbest(preftype='mp4')
                    v.download(filepath=pwd, quiet=True, callback= self.VideoProgressBar)
                        
                    

            if self.qualtyB.checkState() == 2:
                Title = ''
                for i in title:
                    if i not in '|?\/*:"؟':
                        Title += i
                urlretrieve(_img, f'{pwd}/{Title}.jpg')

            ##################################
            self.start.setText("Start Download")
            self.saveE.setText("")
            self.urlE.setText("")
            self.qualtyE.clear()
            self.title.setText("Title: ")
            self.img = QPixmap("img\\Don.png")
            self.smaller_pixmap = self.img.scaled(90, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.imgV.setPixmap(self.smaller_pixmap)
            self.qualtyB.setCheckState(0)
            self.finished3.emit()
            t = time.localtime()
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", t)
            _Histori[title] = [pwd, current_time]
            n.show_toast("yDownloader", f"Download is completed \n{title}", duration=10,icon_path=icon)
        except Exception as E:

            MESSAGE = f"Select where to download the video\n\n{E}"
            self.finished.emit()

        ################################################################## END processing download video
    ################################################################## START processing download video List
    def VideoListSearchBrowse(self):
        save_place = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.PsaveE.setText(save_place)
    def downloadVideoList(self, video):
        video.download(filepath=pathProcessing, quiet=True, callback= self.VideoListProgressBar)
    def downloadAudioList(self,Audio):
        Audio.download(filepath=pathProcessing, quiet=True, callback= self.VideoListProgressBar)

    def rundownloadVideoAudioList(self, video, audio,pwd):
        self.downloadVideoList(video)
        self.downloadAudioList(audio)
        return self.videoListProcess(pwd)
    def videoListProcess(self, pwd):
        global MESSAGE
        try:
            x = os.listdir(pathProcessing)
            video = '"'+pathProcessing+"\\"+x[1] + '"'
            audio = '"'+pathProcessing+"\\"+x[0] + '"'
            video_path = '"{}\{}"'.format(pwd, x[1])
            self.PProgress.setFormat("Processing...")
            cmd = f'ffmpeg -i {video} -i {audio} -c:v copy -c:a aac {video_path}  -loglevel quiet -hide_banner'
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                realtime_output = process.stdout.readline()

                if realtime_output == '' and process.poll() is not None:
                    break
                if realtime_output:
                    pass
            
            time.sleep(1)
            if len(x) > 0:
                for i in x:
                    os.remove(pathProcessing+"\\"+i)
            self.finished2.emit()
        except Exception as Error:
            MESSAGE = "An unknown error has occurred, try again"
            self.finished.emit()
        
    
    def VideoListProgressBar(self, total, recvd, ratio, rate, eta):
        k = recvd / total
        suo = k * 100
        self.PProgress.setValue(suo)
        self.PProgress.setFormat(f"{int(suo)}")
    def rundownloadVidoList(self):
        threading.Thread(target=self.downloadVidoList).start()
    def downloadVidoList(self):
        global MESSAGE
        
        q = ["normal", "1080","720","480","360","240","144", "audio"]
        url = self.PurlE.text()
        pwd = self.PsaveE.text()
        qualty = self.PqualtyE.currentIndex()
        if len(url) == 0 :
            MESSAGE = "Enter the video URL"
            self.finished.emit()
            return
        if len(pwd) == 0 :
            MESSAGE = "Select where to download the video"
            self.finished.emit()
            return
        if len(str(qualty)) == 0 :
            MESSAGE = "Choose the quality in which you want to download the video"
            self.finished.emit()
            return
        self.Pstart.setText("Downloading ...")
        videos = None
        title = None
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]

        try:
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "xxxxxxxxxxxxxxx")
        except Exception as E:
            print(f"line : 898\n You must enter api key correct\n{E}")
            return

        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 50
        )
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        total = len(playlist_items)
        listV =[ 
            f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
            for t in playlist_items
        ]

        title = playlist_items[0]['snippet']['channelTitle']
        T = title
        if os.path.exists(f"{pwd}\\{title}")==False:
            os.makedirs(f"{pwd}\\{title}")
        pwd = f"{pwd}\\{title}"
        
        
        if qualty == 0 or qualty == 7:
            count = 0
            if qualty == 0 :
                for video in listV:
                    count += 1
                    p = pafy.new(video)
                    videoStream = p.getbest(preftype='mp4')
                    title = p.title
                    img = p.thumb
                    self.Ptitle.setText("Title: "+title)
                    urlretrieve(img, f"{pathTmp}\\img1.jpg")
                    img = QPixmap(f"{pathTmp}\\img1.jpg")
                    smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.Pimg.setPixmap(smaller_pixmap)
                    self.PimgL.setText(f"Total: {total}  "+"Current video: "+str(count) )
                    videoStream.download(filepath=pwd, quiet=True,callback= self.VideoListProgressBar)
                    if self.PqualtyC.checkState() == 2:
                        Title = ''
                        for i in title:
                            if i not in '|?\/*:"؟':
                                Title += i
                        urlretrieve(img, f'{pwd}/{Title}.jpg')
            if qualty == 7:
                for video in listV:
                    count += 1
                    p = pafy.new(video)
                    videoStream = p.getbestaudio(preftype='m4a')
                    title = p.title
                    img = p.thumb
                    self.Ptitle.setText("Title: "+title)
                    urlretrieve(img, f"{pathTmp}\\img1.jpg")
                    img = QPixmap(f"{pathTmp}\\img1.jpg")
                    smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.Pimg.setPixmap(smaller_pixmap)
                    self.PimgL.setText(f"Total: {total}  "+"Current video: "+str(count) )
                    videoStream.download(filepath=pwd, quiet=True,callback= self.VideoListProgressBar)
                    if self.PqualtyC.checkState() == 2:
                        Title = ''
                        for i in title:
                            if i not in '|?\/*:"؟':
                                Title += i
                        urlretrieve(img, f'{pwd}/{Title}.jpg')
        else:
            count = 0
            for video in listV:
                count += 1
                Qualty = q[qualty]
                p = pafy.new(video)
                videoStream = p.allstreams
                audio = p.m4astreams
                title = p.title
                img = p.thumb
                self.Ptitle.setText("Title: "+title)
                urlretrieve(img, f"{pathTmp}\\img1.jpg")
                img = QPixmap(f"{pathTmp}\\img1.jpg")
                smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.Pimg.setPixmap(smaller_pixmap)
                self.PimgL.setText(f"Total: {total}  "+"Current video: "+str(count) )
                I = None
                c = 0
                if int(Qualty) == 1080:
                    c = 1
                while True:
                    Index = 0
                    v = 0
                    for i in videoStream:
                        try:
                            if str(Qualty) in str(i).split("x")[1] and "mp4" in str(i):
                                I = i
                                Index = v
                        except:
                            v += 1
                            continue
                        v += 1
                    if I != None:
                        lis = os.listdir(pathProcessing)
                        if len(lis) > 0:
                            for i in lis:
                                os.remove(pathProcessing+"\\"+i)
                        try:
                            self.rundownloadVideoAudioList(videoStream[Index], audio[0], pwd)
                        except Exception as Error:
                            videoStream = p.getbest(preftype='mp4')
                            videoStream.download(filepath=pwd, quiet=True, callback= self.VideoListProgressBer)
                        break
                    else:
                        if c == 0:
                            Qualty = int(Qualty) + 1
                        else:
                            Qualty = int(Qualty) - 1
                        if int(Qualty) > 1090 and int(Qualty) < 0:
                            if int(Qualty) > 1090:
                                c = 1
                            else:
                                c = 0
                            continue
                if self.PqualtyC.checkState() == 2:
                    Title = ''
                    for i in title:
                        if i not in '|?\/*:"؟':
                            Title += i
                    urlretrieve(img, f'{pwd}/{Title}.jpg')
                
        
        self.Pstart.setText("Start Download")
        self.PurlE.setText("")
        self.PsaveE.setText("")
        self.PqualtyE.setCurrentIndex(0)
        self.Ptitle.setText("Title: ")
        self.PimgL.setText("Current video: ")
        self.img = QPixmap("img\\Don.png")
        smaller_pixmap = self.img.scaled(90, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.Pimg.setPixmap(smaller_pixmap)
        self.PqualtyC.setCheckState(0)
        self.PProgress.clearFocus()
        self.finished2.emit()
        t = time.localtime()
        current_time = time.strftime("%d/%m/%Y %H:%M:%S", t)
        _Histori[title] = [pwd, current_time]
        n.show_toast("yDownloader", f"Download is completed \n{T}", duration=10,icon_path=icon)
        

    ############################################################### start channel vidos
    def ChannelSearchBrowse(self):
        save_place = QFileDialog.getExistingDirectory(self, 'Select Download Directory')
        self.CsaveE.setText(save_place)
    def VideoChannelProgressBar(self, total, recvd, ratio, rate, eta):
        k = recvd / total
        suo = k * 100
        self.CProgress.setValue(suo)
        self.CProgress.setFormat(f"{int(suo)}")
    def rundownloadVidoChannel(self):
        threading.Thread(target=self.downloadVidoChannel).start()
    
    def videoChannelProcess(self, pwd):
        global MESSAGE
        try:
            x = os.listdir(pathProcessing)
            video = '"'+pathProcessing+"\\"+x[1] + '"'
            audio = '"'+pathProcessing+"\\"+x[0] + '"'
            video_path = '"{}\{}"'.format(pwd, x[1])
            self.CProgress.setFormat("Processing...")
            cmd = f'ffmpeg -i {video} -i {audio} -c:v copy -c:a aac {video_path}  -loglevel quiet -hide_banner'
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                realtime_output = process.stdout.readline()

                if realtime_output == '' and process.poll() is not None:
                    break
                if realtime_output:
                    pass
            
            time.sleep(1)
            if len(x) > 0:
                for i in x:
                    os.remove(pathProcessing+"\\"+i)
            self.finished2.emit()
        except Exception as Error:
            MESSAGE = "An unknown error has occurred, try again"
            self.finished.emit()
    def downloadVideoChannel(self, video):
        video.download(filepath=pathProcessing, quiet=True, callback= self.VideoChannelProgressBar)
    def downloadAudioChannel(self,Audio):
        Audio.download(filepath=pathProcessing, quiet=True, callback= self.VideoChannelProgressBar)
    def rundownloadVideoAudioChannel(self, video, audio,pwd):
        self.downloadVideoChannel(video)
        self.downloadAudioChannel(audio)
        return self.videoChannelProcess(pwd)
    
    def channel_video(self):
        url = self.CurlE.text()
        url_id = str(url).split('/')[-1]
        self.Cstart.setText("Downloading ...")
        api_key = "xxxxxxxxxxxxxxx"
        try:
            youtube = discovery.build('youtube', 'v3', developerKey=api_key)
        except Exception as E:
            print(f"line : 1108\n You must enter api key correct\n{E}")
            return

        def get_channel_videos(channel_id):
            global MESSAGE

            # get Uploads playlist id
            try:
                res = youtube.channels().list(id=channel_id,
                                            part='contentDetails').execute()
                playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

                url_videos = []
                next_page_token = None

                while 1:
                    res = youtube.playlistItems().list(playlistId=playlist_id,
                                                    part='snippet',
                                                    maxResults=50,
                                                    pageToken=next_page_token).execute()
                    url_videos += res['items']
                    next_page_token = res.get('nextPageToken')

                    if next_page_token is None:
                        break

                return url_videos
            except Exception as E:
                MESSAGE = "The link you entered is not valid, please check it and try again"
                self.finished.emit()
            

        videos = get_channel_videos(url_id)
        video_URL = []
        img_URL = []
        Title_Video = []
        title_channel = videos[0]['snippet']['channelTitle']
        All_Data = []
        for video in videos:
            video_url = 'https://www.youtube.com/watch?v=' + str(video['snippet']['resourceId']['videoId'])
            title_video = video['snippet']['title']
            img_url = video['snippet']['thumbnails']['default']['url']
            video_URL.append(video_url)
            img_URL.append(img_url)
            Title_Video.append(title_video)
        All_Data.append(title_channel)
        All_Data.append(video_URL)
        All_Data.append(img_URL)
        All_Data.append(Title_Video)
        return All_Data
    
    def downloadVidoChannel(self):
        global MESSAGE
        
        q = ["normal", "1080","720","480","360","240","144", "audio"]
        
        url = self.CurlE.text()
        pwd = self.CsaveE.text()
        qualty = self.CqualtyE.currentIndex()
        if len(url) == 0 :
            MESSAGE = "Enter the video URL"
            self.finished.emit()
            return
        if len(pwd) == 0 :
            MESSAGE = "Select where to download the video"
            self.finished.emit()
            return
        if len(str(qualty)) == 0 :
            MESSAGE = "Choose the quality in which you want to download the video"
            self.finished.emit()
            return
        if os.path.exists(f"{pwd}") == False:
            MESSAGE ="The storage location does not exist. Please check it and try again"
            self.finished.emit()
            return
        AllDate = None
        try:
            AllDate = self.channel_video()
        except Exception as Error:
            MESSAGE = "An unknown error has occurred, try again"
            self.finished.emit()
            return
        
        if os.path.exists(f"{pwd}\\{AllDate[0]}") == False:
            os.mkdir(f"{pwd}\\{AllDate[0]}")
        pwd = f"{pwd}\\{AllDate[0]}"
        if qualty == 0 or qualty == 7:
            count = 0
            countVidoe = 0
            if qualty == 0 :
                self.Cstart.setText("Downloading ...")
                for i in AllDate[1]:
                    count += 1
                    p = None
                    try:
                        p = pafy.new(i)
                    except Exception as E:
                        MESSAGE = "The link you entered is not valid, please check it and try again"
                        self.finished.emit()
                        return
                    videoStream = p.getbest(preftype='mp4')
                    title = p.title
                    img = p.thumb
                    self.Ctitle.setText(title)
                    urlretrieve(img, f"{pathTmp}\\img1.jpg")
                    img = QPixmap(f"{pathTmp}\\img1.jpg")
                    smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.Cimg.setPixmap(smaller_pixmap)
                    self.CimgL.setText("Current video: "+str(count))
                    videoStream.download(filepath=pwd, quiet=True,callback= self.VideoChannelProgressBar)
                    if self.CqualtyC.checkState() == 2:
                        Title = ''
                        for i in title:
                            if i not in '|?\/*:"؟':
                                Title += i
                        urlretrieve(AllDate[2][countVidoe], f'{pwd}/{Title}.jpg')

                    countVidoe += 1
                
            if qualty == 7:
                self.Cstart.setText("Downloading ...")
                for i in AllDate[1]:
                    count += 1
                    p = None
                    try:
                        p = pafy.new(i)
                    except Exception as E:
                        MESSAGE = "The link you entered is not valid, please check it and try again"
                        self.finished.emit()
                        return
                    videoStream = p.getbestaudio(preftype='m4a')
                    title = p.title
                    img = p.thumb
                    self.Ctitle.setText(title)
                    urlretrieve(img, f"{pathTmp}\\img1.jpg")
                    img = QPixmap(f"{pathTmp}\\img1.jpg")
                    smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.Cimg.setPixmap(smaller_pixmap)
                    self.CimgL.setText("Current video: "+str(count))
                    videoStream.download(filepath=pwd, quiet=True,callback= self.VideoChannelProgressBar)
                    if self.CqualtyC.checkState() == 2:
                        Title = ''
                        for i in title:
                            if i not in '|?\/*:"؟':
                                Title += i
                        urlretrieve(AllDate[2][countVidoe], f'{pwd}/{Title}.jpg')
                    countVidoe += 1
        else:
            count = 0
            countVidoe = 0
            self.Cstart.setText("Downloading ...")
            for i in AllDate[1]:
                count += 1
                p = None
                try:
                    p = pafy.new(i)
                except Exception as E:

                    MESSAGE = "The link you entered is not valid, please check it and try again"
                    self.finished.emit()
                    return
                Qualty = q[qualty]  
                videoStream = p.allstreams
                audio = p.m4astreams
                title = p.title
                img = p.thumb
                self.Ctitle.setText(title)
                urlretrieve(img, f"{pathTmp}\\img1.jpg")
                img = QPixmap(f"{pathTmp}\\img1.jpg")
                smaller_pixmap = img.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.Cimg.setPixmap(smaller_pixmap)
                self.CimgL.setText("Current video: "+str(count))
                I = None
                c = 0
                if int(Qualty) == 1080:
                    c = 1
                while True:
                    Index = 0
                    v = 0
                    for i in videoStream:
                        try:
                            if str(Qualty) in str(i).split("x")[1] and "mp4" in str(i):
                                I = i
                                Index = v
                        except:
                            v += 1
                            continue
                        v += 1
                    if I != None:
                        lis = os.listdir(pathProcessing)
                        if len(lis) > 0:
                            for i in lis:
                                os.remove(pathProcessing+"\\"+i)
                        try:
                            self.rundownloadVideoAudioChannel(videoStream[Index], audio[0], pwd)
                        except Exception as Error:
                            E = "HTTP Error 404"
                            if E in str(Error):
                                if 2 < qualty :
                                    qualty -= 1
                                    self.CqualtyE.setCurrentIndex(qualty)
                                    return self.downloadVidoChannel()
                                else:
                                    videoStream = p.getbest(preftype='mp4')
                                    videoStream.download(filepath=pwd, quiet=True, callback= self.VideoChannelProgressBar)
                            else:
                                videoStream = p.getbest(preftype='mp4')
                                videoStream.download(filepath=pwd, quiet=True, callback= self.VideoChannelProgressBar)
                        break
                    else:
                        if c == 0:
                            Qualty = int(Qualty) + 1
                        else:
                            Qualty = int(Qualty) - 1
                        if int(Qualty) > 1090 and int(Qualty) < 0:
                            if int(Qualty) > 1090:
                                c = 1
                            else:
                                c = 0
                            continue
                if self.CqualtyC.checkState() == 2:
                    Title = ''
                    for i in title:
                        if i not in '|?\/*:"؟':
                            Title += i
                    urlretrieve(AllDate[2][countVidoe], f'{pwd}/{Title}.jpg')
                countVidoe += 1

        self.CProgress.clearFocus()
        self.finished1.emit()
        self.Cstart.setText("Start Download")
        self.CurlE.setText("")
        self.CsaveE.setText("")
        self.CqualtyE.setCurrentIndex(0)
        self.Ctitle.setText("")
        self.CimgL.setText("Current video: ")
        self.img = QPixmap("img\\Don.png")
        smaller_pixmap = self.img.scaled(90, 90, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.Cimg.setPixmap(smaller_pixmap)
        self.CqualtyC.setCheckState(0)
        t = time.localtime()
        current_time = time.strftime("%d/%m/%Y %H:%M:%S", t)
        _Histori[title] = [pwd, current_time]
        n.show_toast("yDownloader", f"Download is completed \n{AllDate[0]}", duration=10,icon_path=icon)

        # ############################## database connect
    def DB_Connect(self):
        global MESSAGE, paypal, _Histori
        try:
            self.db = mysql.connector.connect(user='root', password='', host='freedb.tech', db="yDownloadre")
            self.curdb = self.db.cursor(buffered=True)
            self.slit = sqlite3.connect(f"{pathDB}\\savelogin.db")
            self.curlit = self.slit.cursor()

            self.curlit.execute("""
            create table if not exists login (
            name	TEXT,
            mail	TEXT NOT NULL,
            password	TEXT NOT NULL )
            """)
            self.slit.commit()
            self.curlit.execute("""
            create table if not exists history(
            name  TEXT,
            pwd  TEXT,
            time  TEXT)
            """)
            self.slit.commit()
            self.curlit.execute("""create table if not exists Message(MText  TEXT)""")
            self.slit.commit()
            try:
                self.curdb.execute("SELECT * FROM link;")
                message = self.curdb.fetchone()
                paypal = message[1]
                WEP = message[3]
                self.wep.setText(f'<html><head/><body><p><a href="{WEP}"><span style=" text-decoration: underline; color:#ffffff;">Buy from the official website</span></a></p></body></html>')
                if len(message[2]) != 0:
                    self.curlit.execute("SELECT * FROM Message;")
                    MLDB =  self.curlit.fetchone()
                    c = 0
                    if MLDB != None:
                        if MLDB[0] == message[2] :
                            c = 0
                        else:
                            c = 1
                    else:
                        c = 1
                    if c == 1:
                        print(1)
                        if "URL" in message[2]:
                            print(2)
                            messag = message[2].split("URL")[0]
                            url = message[2].split("URL")[1].split("TITLE")[0]
                            title = message[2].split("URL")[1].split("TITLE")[1]
                        else:
                            print(3)
                            messag = message[2]
                            url = ""
                            title = ""
                        print(4)
                        help_message = QMessageBox()
                        help_message.setWindowIcon(QIcon(r"img\YDownloader.png"))
                        help_message.setWindowTitle('yDownloder About')
                        help_message.setText( f"<br>{messag}")
                        help_message.setTextFormat(Qt.RichText)
                        help_message.setInformativeText(f"<a  href='{url.strip()}'>{title}</a><br><br>COLONAL")
                        help_message.exec_()
                        self.curlit.execute("DELETE FROM Message")
                        self.curlit.execute("INSERT INTO Message( MText)VALUES (?)",(message[2],))
                        self.slit.commit()
            except Exception as E:
                print(E)
            self.check()
            _Histori = {}
            self.curlit.execute("SELECT * FROM history;")
            Hdata  = self.curlit.fetchall()
            for i in Hdata:
                _Histori[i[0]] = [i[1], i[2]]
            self.on_History()
            
        except Exception as ERRoR:
            MESSAGE = f"{ERRoR}"
            self.channelBut.setEnabled(False)
            self.accountBut.setEnabled(False)
            self.finished.emit()
    def LOGIN(self):
        global MESSAGE, IDUser
        emalE = self.emalE.text()
        passwordE = self.passwordE.text()

        if 0 == len(emalE) or len(emalE)  > 50 or 0 == len(passwordE) or len(passwordE) > 20:
            MESSAGE = "Please enter correct information"
            self.finished.emit()
            return
        if re.search(regex,emalE):
            if len(emalE)> 50:
                MESSAGE = "Invalid Email more 40 character"
                self.finished.emit()
                return
        else:
            MESSAGE = "Invalid Email"
            self.finished.emit()
            return

        passhash = sha256(passwordE.encode()).hexdigest()
        
        self.curdb.execute("SELECT id FROM client WHERE password=%s and mail=%s",(passhash,emalE))
        ID = self.curdb.fetchone()
        if ID == None:
            MESSAGE = "The email or password is wrong, try again"
            self.finished.emit()
            return
        self.curdb.execute("SELECT * FROM pcname  WHERE IdData=%s",(ID[0],))
        pc = self.curdb.fetchall()
        IDUser = ID[0]
        
        if len(pc) >= 3:
            pcName = os.getlogin()
            c = 0
            for i in pc:
                if pcName == i[1]:
                    c += 1
            if c == 0:
                MESSAGE = "You exceeded the login limit on different devices"
                self.finished.emit()
                return
        else:
            pcName = os.getlogin()
            c = 0
            for i in pc:
                if pcName == i[1]:
                    c += 1
            if c == 0:
                self.curdb.execute('INSERT INTO pcname (name_pc, IdData) VALUES (%s, %s)', (pcName, ID[0]))
                self.db.commit()

        
        self.curdb.execute("SELECT * FROM client  WHERE id=%s",(ID[0],))
        data = self.curdb.fetchone()
        if data[6] == "0":
            self.tabsChannel.setCurrentIndex(1)
        else:
            self.tabsChannel.setCurrentIndex(2)

        self.curlit.execute("DELETE FROM login")
        self.slit.commit()
        self.curlit.execute("INSERT INTO login (mail, password) VALUES (?,?)",(data[2], data[3]))
        self.slit.commit()

        self.statA.setText(f"Allowed number of devices 3, you have {3-len(pc)} left")
        self.NameA.setText(f"{data[1]}")
        self.MailA.setText(f"{data[2]}")
        self.ProductID.setText(F"{data[5]}")
        active = data[6]
        if active == "0":
            active = "No Activation"
        else:
            active = "Activation"
        self.activationA.setText(f"{active}")
    
    def check(self):
        global IDUser
        self.curlit.execute("SELECT * FROM login")
        data = self.curlit.fetchone()
        if data == None:
            self.tabsChannel.setCurrentIndex(0)
            self.tabsAccount.setCurrentIndex(0)
            return
        self.curdb.execute("SELECT * FROM client WHERE password=%s and mail=%s",(data[2],data[1]))
        ID = self.curdb.fetchone()
        
        if ID == None:
            self.tabsChannel.setCurrentIndex(0)
            self.tabsAccount.setCurrentIndex(0)
            return
        IDUser = ID[0]
        self.curdb.execute("SELECT * FROM pcname  WHERE IdData=%s",(ID[0],))
        pc = self.curdb.fetchall()
        
        if ID[6] == "0":
            self.tabsChannel.setCurrentIndex(1)
        else:
            self.tabsChannel.setCurrentIndex(2)
        
        self.statA.setText(f"Allowed number of devices 3, you have {3-len(pc)} left")
        self.NameA.setText(f"{ID[1]}")
        self.MailA.setText(f"{ID[2]}")
        self.ProductID.setText(F"{ID[5]}")
        active = ID[6]
        if active == "0":
            active = "No Activation"
        else:
            active = "Activation"
        self.activationA.setText(f"{active}")
        
        

    def SIGNUP(self):
        global MESSAGE
        fname = self.FName.text()
        lname = self.SName.text()
        Email = self.emalES.text()
        password = self.passwordES.text()
        rewrite = self.rewrite.text()
        if len(fname) == 0 or len(lname) == 0 or len(password) == 0 or len(Email) == 0 or len(rewrite) == 0:
            MESSAGE = "All fields are required"
            self.finished.emit()
            return
        if len(fname) > 20 or len(lname) > 20:
            MESSAGE = "First and Last names more  20  letters"
            self.finished.emit()
            return
        if fname.isalpha() == False or lname.isalpha() == False:
            MESSAGE = "First and Last names must contain letters only"
            self.finished.emit()
            return
        if re.search(regex,Email):
            if len(Email)> 50:
                MESSAGE = "Invalid Email more 40 character"
                self.finished.emit()
                return
        else:
            MESSAGE = "Invalid Email"
            self.finished.emit()
            return
        if password == rewrite:
            if len(password) > 20 or len(password) < 5:
                MESSAGE = "The password must be more than 5 syllables and not exceed 20"
                self.finished.emit()
                return
        else:
            MESSAGE = "Password does not match Rewrite"
            self.finished.emit()
            return
        if " " in fname or " " in lname or " " in password or " " in Email:
            MESSAGE = "All fields must not contain a space"
            self.finished.emit()
            return

        checkEmail = self.curdb.execute("SELECT mail FROM client WHERE mail =%s",(Email,))
        if checkEmail != None:
            MESSAGE = "Email already exists. Try logging in"
            self.finished.emit()
            return

        passhash = sha256(password.encode()).hexdigest()
        name = f"{fname} {lname}"
        activation = "0"
        pc = os.getlogin()
        

        try:
            self.curdb.execute('''INSERT INTO client (name ,mail, password, pc,activation)
                VALUES (%s, %s,%s, %s, %s)''', (name, Email, passhash, pc, activation))
            self.db.commit()
            
            self.curdb.execute('SELECT id FROM client WHERE mail=%s', (Email,))
            Id = self.curdb.fetchall()
            
            self.curdb.execute('INSERT INTO pcname (name_pc, IdData) VALUES (%s, %s)', (pc, Id[0][0]))
            self.db.commit()
            
            self.emalE.setText(Email)
            self.passwordE.setText(password)
            self.tabsAccount.setCurrentIndex(0)
        except Exception as Error:
            MESSAGE = f"{Error}"
            self.finished.emit()
    def ActivationPcheck(self):
        global MESSAGE
        code = self.ActivationL.text()
        self.curdb.execute("SELECT defaultActiv FROM client WHERE id=%s",(IDUser,))
        defaultActiv = self.curdb.fetchone()
        print(defaultActiv)
        if code == defaultActiv[0]:
            try:
                self.curdb.execute("UPDATE client SET code=%s, activation=%s WHERE id=%s",(defaultActiv[0],"1",IDUser))
                self.db.commit()
            except:
                MESSAGE = "Something went wrong, try again "
                self.finished.emit()
                return
        else:
            self.curdb.execute("SELECT code FROM client WHERE id=%s",(IDUser,))
            Code = self.curdb.fetchone()

            if Code[0] != None:
                if Code[0] == code:
                    try:
                        self.curdb.execute("UPDATE client SET activation=%s WHERE id=%s",("1",IDUser))
                        self.db.commit()
                    except:
                        MESSAGE = "Something went wrong, try again "
                        self.finished.emit()
                        return
                else:
                    MESSAGE = "The code entered is incorrect. Check case and try again"
                    self.finished.emit()
                    return
            else:
                MESSAGE = "The code entered is incorrect. Check case and try again\nThe free code is colonal"
                self.finished.emit()
                return
        self.check()
    def Logout(self):
        self.curlit.execute("DELETE FROM login")
        self.slit.commit()
        self.check()
        self.emalE.setText("")
        self.passwordE.setText("")
        self.tabs.setCurrentIndex(2)
    
    def setTable(self):
        global _Histori
        self.HTable.setRowCount(len(_Histori))
        c = 0
        for i in _Histori:
            self.HTable.setItem(c,0,QTableWidgetItem(i))
            self.HTable.setItem(c,1,QTableWidgetItem(_Histori[i][0]))
            self.HTable.setItem(c,2,QTableWidgetItem(_Histori[i][1]))

            if len(_Histori) > c:
                
                c += 1
    def deleteHistory(self):
        global _Histori
        Q = QMessageBox.information(self,"yDownloader", "Are you sure to delete a record ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if Q == QMessageBox.Yes:
            _Histori = {}
            self.curlit.execute("DELETE FROM history")
            self.slit.commit()
            self.on_History()
    def closeEvent(self, event):
        global _Histori
        self.slit = sqlite3.connect(f"{pathDB}\\savelogin.db")
        self.curlit = self.slit.cursor()
        
        self.curlit.execute("DELETE FROM history")
        self.slit.commit()
        for i in _Histori:
            self.curlit.execute("INSERT INTO history(name,pwd,time) VALUES (?,?,?);",(i,_Histori[i][0],_Histori[i][1]))
        
        self.slit.commit()

def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())

if __name__ == "__main__":
    if os.path.exists(f"{path}") == False:
        os.makedirs(f"{path}")
    if os.path.exists(f"{pathTmp}") == False:
        os.makedirs(f"{pathTmp}")
    if os.path.exists(f"{pathDB}") == False:
        os.makedirs(f"{pathDB}")
    if os.path.exists(f"{pathProcessing}") == False:
        os.makedirs(f"{pathProcessing}")
    lis = os.listdir(pathProcessing)
    if len(lis) > 0:
        for i in lis:
            os.remove(pathProcessing+"\\"+i)
    main()