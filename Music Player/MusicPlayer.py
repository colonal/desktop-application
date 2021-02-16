import sys, os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import  QSize, QTimer, Qt
from PyQt5.QtCore import pyqtSignal
import random, time 
from pygame import mixer
from mutagen.mp3 import MP3
import pyautogui as A
import sqlite3
from threading import Thread
import webbrowser
from moviepy.editor import *



musicList = []
_historyCount = {}
_historyTime = {}
mixer.init()
muted = False
get = 0
count = 0
songLength = 0
index = 0
ind = -99
statuwindow = False
Geometry = []
nameplay = ''
pathDB = os.environ['APPDATA']
sliderChange = 0
sliderChangeStop = False
openMusic  = ''
ConvertId = 1
MESSAGE = ""





class Player(QMainWindow):
    finished = pyqtSignal()
    finished1 = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(450, 50, 300, 500)
        self.setWindowIcon(QIcon(r"icons\icon.png"))
        self.setAcceptDrops(True)
        self.finished.connect(self.on_finished, Qt.QueuedConnection)
        self.finished1.connect(self.on_finished1, Qt.QueuedConnection)
        try:
            self.UI()
        except Exception as error:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")
        self.show()
        

    def UI(self):
        self.DB()
        self.MenuBar()
        self.widget()
        self.layouts()
        self.style()
        self.startProgram()
    
    def on_finished(self):
        self.playList.clear()
        for i in musicList:
            name = os.path.basename(i)
            self.playList.addItem(name)
        print(f"ConvertId2:{ConvertId}")
        self.playList.setCurrentRow(ConvertId)
        self.PlaySound()
        self.playSounds()
        self.updateSiderPlay()
    def on_finished1(self):
        QMessageBox.information(self,"Music Player",f"{MESSAGE}")

    def DB(self):
        if os.path.exists(f"{pathDB}\\Music Player") == False :
            os.mkdir(f"{pathDB}\\Music Player")
    
        self._db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        self._db.execute("create table if not exists open(Id integer primary key autoincrement,music text)")
        self._db.execute("create table if not exists history(music text, count integer, Time text)")
        
        self._db.commit()
        self._db.close()
    
    
    def startProgram(self):
        global musicList, _historyCount, _historyTime
        db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        row = db.execute("select music from open")
        if len(openMusic) > 0:
            musicList.append(openMusic)
            self.playList.addItem(os.path.basename(openMusic))
            self.playList.setCurrentRow(0)
        for i in row:
            musicList.append(i[0])
            name = os.path.basename(i[0])
            self.playList.addItem(name)
        
        hm = db.execute("select * from history")
        for i in hm:
            _historyCount[i[0]] = i[1]
            _historyTime[i[0]] = i[2]
        if self.playList.currentRow() != (-1):
            self.playSounds()
        
        db.close()
        
    
    
    def widget(self):
        # ############################## ProgressBar
        self.siderPlay = QSlider(Qt.Horizontal)
        self.siderPlay.setValue(0)
        self.siderPlay.setMinimum(0)
        self.siderPlay.setMaximum(100)
        self.siderPlay.setEnabled(False)
        self.siderPlay.valueChanged.connect(self.SliderChange)
        # #################################### Labels
        self.songTimerLabel = QLabel("0:00")
        self.songLentthLabel = QLabel("/ 0:00")
        self.songTimerLabel.setStyleSheet("color: #fff")
        self.songLentthLabel.setStyleSheet("color: #fff")
        # ############################### Buttons
        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon("icons/add.png"))
        self.addButton.setIconSize(QSize(48, 48))
        self.addButton.setToolTip("Add a Song")
        self.addButton.clicked.connect(self.AddSounds)

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon("icons/shuffle.png"))
        self.shuffleButton.setIconSize(QSize(48, 48))
        self.shuffleButton.setToolTip("shuffle The List")
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon("icons/previous.png"))
        self.previousButton.setIconSize(QSize(48, 48))
        self.previousButton.setToolTip("Play Previous")
        self.previousButton.clicked.connect(self.playPrevious)

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("icons/play.png"))
        self.playButton.setIconSize(QSize(48, 48))
        self.playButton.setToolTip("Play")
        self.playButton.clicked.connect(self.playSounds)

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon("icons/next.png"))
        self.nextButton.setIconSize(QSize(48, 48))
        self.nextButton.setToolTip("Play Next")
        self.nextButton.clicked.connect(self.NextSounds)

        self.cuntVolume = QLabel("100")
        self.cuntVolume.hide()

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon("icons/mute.png"))
        self.muteButton.setIconSize(QSize(20, 20))
        self.muteButton.setToolTip("Mute")
        self.muteButton.clicked.connect(self.muteSound)

        self.minimize = QToolButton()
        self.minimize.setToolTip("Minimize")
        self.minimize.setIcon(QIcon("icons/minimize (1).png"))
        self.minimize.setIconSize(QSize(15, 15))
        self.minimize.clicked.connect(self.Minimize)


        # ############################################ volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimumWidth(50)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.resize(10,10)
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        mixer.music.set_volume(0.7)
        self.volumeSlider.valueChanged.connect(self.setVolume)

        # ####################################  play List
        self.playList = QListWidget()
        
    
        self.playList.doubleClicked.connect(self.playSounds)
        # ############################################## Timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateSiderPlay)
        # ############################################# QTableWidget history
        self.historyTable = QTableWidget()
        self.historyTable.setColumnCount(2)
        self.historyTable.setHorizontalHeaderItem(0, QTableWidgetItem("Music"))
        self.historyTable.setHorizontalHeaderItem(1, QTableWidgetItem("Count"))
        self.historyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.historyTable.horizontalHeader().setStretchLastSection(True) 
        self.historyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.historyTable.verticalHeader().setStretchLastSection(True)
        self.historyTable.verticalHeader().hide()
        self.historyTable.hide()
        self.historyTable.doubleClicked.connect(self.playHistoryTable)
        # ###############  combo history
        self.combo = QComboBox()
        self.combo.addItems(["History Count","History Date"])
        self.combo.hide()
        self.combo.activated.connect(self.History)
        # ########################################## GroupBox history 
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.BackButton)
        
        self.deleteAll = QPushButton("Delele All")
        self.deleteAll.clicked.connect(self.DeleteAll)

        self.deleteItem = QPushButton("Delete")
        self.deleteItem.clicked.connect(self.DeleteItem)
        
        
    
    def layouts(self):
        ###################################
        self.mainLayout = QVBoxLayout()
        
        self.topmainLayout = QVBoxLayout()
        self.bottumLayout = QVBoxLayout()
        self.bottumHistory = QHBoxLayout()
        self.FilterHistory = QHBoxLayout()

        self.topGroupBox = QGroupBox("music Player")
        self.middleLayout = QHBoxLayout()
        self.topLayout = QHBoxLayout()
        self.QVVolume = QVBoxLayout()
        
        
        
        self.GbottumHistory = QGroupBox()
        self.GbottumHistory.setLayout(self.bottumHistory)
        self.GbottumHistory.hide()
        ###########################################

        self.topLayout.addWidget(self.siderPlay)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLentthLabel)
        self.topLayout.setContentsMargins(0,10, 0,0)

        # ##############
        self.QVVolume.setContentsMargins(0,0,0,0)
        self.QVVolume.addStretch()
        self.QVVolume.addWidget(self.volumeSlider)
        self.QVVolume.addWidget(self.cuntVolume)
        self.QVVolume.addStretch()
        # #################################### Middle layout widget
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addLayout(self.QVVolume)
        #self.middleLayout.addWidget(self.cuntVolume)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addWidget(self.minimize)
        self.middleLayout.setContentsMargins(0, 0, 0 ,0)
        self.middleLayout.addStretch()
        # #################################### Bottom Layout widget
        
        self.bottumLayout.addWidget(self.playList)
        
        
        self.topmainLayout.addLayout(self.topLayout)
        self.topmainLayout.addLayout(self.middleLayout)
        

        self.topGroupBox.setLayout(self.topmainLayout)

        self.mainLayout.addWidget(self.topGroupBox, 25)
        
        self.mainLayout.addLayout(self.bottumLayout, 75)
        self.mainLayout.addWidget(self.historyTable,90)
        self.mainLayout.addLayout(self.FilterHistory,5)
        self.mainLayout.addWidget(self.GbottumHistory, 5)
        self.mainLayout.addStretch()
        # ########################################### button History
        self.bottumHistory.addWidget(self.backButton)
        self.bottumHistory.addWidget(self.deleteAll)
        self.bottumHistory.addWidget(self.deleteItem)

        self.FilterHistory.addWidget(self.combo)

        
        self.widgett = QWidget()
        
        self.widgett.setLayout(self.mainLayout)
        self.setCentralWidget(self.widgett)
        
        
    def style(self):
        try:
            with open("StyleMusicPlayer\\main.css", "r") as L:
                self.setStyleSheet(L.read())
            #self.setStyleSheet(style.main())
            with open("StyleMusicPlayer\\Slider.css", "r") as L:
                self.volumeSlider.setStyleSheet(L.read())
            self.cuntVolume.setStyleSheet("""
            QLabel{padding-top: 0px;
            padding-right: 10px;
            padding-bottom: 0px;
            padding-left: 10px;}
            """)
        except Exception as E:
            print(E)


    def AddSound(self):
        file = "Sound Files (*.mp3 *.ogg *.wav *.mp4 *.wmv *.aac *.wma *m4a) ;;All Files (*)"
        directory, ok = QFileDialog.getOpenFileName(self, "Add Sound", "", file)
        if ok:
            fileName = os.path.basename(directory)
            self.playList.addItem(fileName)
            musicList.append(directory)
    
    def AddSounds(self):
        file = "Sound Files (*.mp3 *.ogg *.wav *.mp4 *.wmv *.aac *.wma *m4a) ;;All Files (*)"
        directory, ok = QFileDialog.getOpenFileNames(self, "Add Sound", "", file)

        if ok:
            for i in directory:
                fileName = os.path.basename(i)
                self.playList.addItem(fileName)
                musicList.append(i)

    def  Folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        
        name = os.listdir(directory)
        for I in name :
            x =  os.path.basename(I).split(".")[-1]
            if x=="m4a" or x == "m4a" or x == "mp3" or x == "wav" or x == "mp4" or x == "wmv" or x == "aac" or x == "wma" or x == "ogg":
                fileName = os.path.basename(I)
                self.playList.addItem(fileName)
                musicList.append(directory+"/"+I)


    
    def shufflePlayList(self):
        index = self.playList.currentRow()
        Text = musicList[index]
        random.shuffle(musicList)
        self.playList.clear()
        c = 0
        x = 0
        for i in musicList:
            name = os.path.basename(i)
            self.playList.addItem(name)
            if i == Text:
                x = c
            c += 1
        self.playList.setCurrentRow(x)

    def playSounds(self):
        global songLength, count, ind, nameplay, _historyCount,sliderChangeStop,_historyTime,musicList
        value = self.siderPlay.value()
        Time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if sliderChangeStop == True:
            self.playButton.setToolTip("Stop")
            self.PlaySound()
            self.SliderChange()
            sliderChangeStop = False
            
            return

        
        if ind == -99:
            index = self.playList.currentRow()
        else:
            index = ind
            ind = -99
        
        if index == -1:
            return
        

        stat = self.playButton.toolTip()
        if musicList[index] == nameplay:
            self.PlaySound()  
            if stat == "Stop":
                self.StopSound()
                self.playButton.setToolTip("Play")
                return
            else:
                self.playButton.setToolTip("Stop")
                count = self.siderPlay.value()
                if musicList[index] == nameplay:
                    self.PlaySound()
                    return
        else:
            self.playButton.setToolTip("Stop")        
            

        
        try:
            if musicList[index] in _historyCount:
                for i in _historyCount:
                    if i == musicList[index]:
                        _historyCount[i] += 1 
            else:
                _historyCount[f'{musicList[index]}'] = 1
            ############
            if musicList[index] in _historyTime:
                for i in _historyTime:
                    if i == musicList[index]:
                        _historyTime[i] = Time
            else:
                _historyTime[f'{musicList[index]}'] = Time
            ##########
            count = 0
            self.playButton.setIcon(QIcon("icons/stop.png"))
            nameplay = str(musicList[index])
            mixer.music.load(musicList[index])
            self.siderPlay.setEnabled(True)
            mixer.music.play()
            end = mixer.music.set_endevent(1)
            if end ==1 :
                self.NextSounds() 
            self.timer.start()
            sound = MP3(str(musicList[index]))
            songLength = sound.info.length
            songLength = round(songLength)

            Min, sec = divmod(songLength, 60)
            if len(str(sec)) == 1:
                sec = f'0{sec}'
            if len(str(Min)) == 1:
                Min == f'0{Min}'
            self.songLentthLabel.setText(f"/ {Min}:{sec}")
            self.siderPlay.setValue(0)
            self.siderPlay.setMaximum(songLength)
        
        except Exception as Error:
            print(Error)
            self.playButton.setToolTip("Play")
            self.playButton.setIcon(QIcon("icons/play.png"))
            src = str(musicList[index])
            if  "Unknown WAVE data format" in str(Error) or "ModPlug_Load failed" in str(Error):
                m = "There seems to be a codec issue that can be fixed by extracting a fresh copy of the audio clip to mp3\n"
                dst = src.split(".")[0] + '.mp3'
                if os.path.exists(dst):
                    print(1)
                    self.run_convert(dst, index)
                    
                else:
                    print(str(musicList[index]))
                    mss = QMessageBox.information(self,"Music Player",m, QMessageBox.Yes|QMessageBox.No , QMessageBox.Yes)
                    if mss == QMessageBox.Yes:
                        print("Yes")
                        src = str(musicList[index])
                        file = ["m4a","mp3","ogg" ,"wav" ,"mp4" ,"wmv" ,"aac" ,"wma"]
                        if src.split(".")[-1] in file:
                            print("run")
                            self.run_convert(src, index)
            elif "code 12" in str(Error):
                print("code 12")
                dst = src.split(".")[0] + '1.mp3'
                m = "There appears to be a problem with the codec. You can try to fix this by extracting a new copy of the audio clip to mp3\nThe Error:\n\t{str(Error)}"
                if os.path.exists(dst):
                    print(1)
                    self.run_convert(dst, index)
                    
                else:
                    mss = QMessageBox.information(self,"Music Player",m, QMessageBox.Yes|QMessageBox.No , QMessageBox.Yes)
                    if mss == QMessageBox.Yes:
                        src = str(musicList[index])
                        file = ["m4a","mp3","ogg" ,"wav" ,"mp4" ,"wmv" ,"aac" ,"wma"]
                        if src.split(".")[-1] in file:
                            self.run_convert(src, index)
            else:
                QMessageBox.information(self,"Music Player",f"{Error}")
                try:
                    item = self.playList.currentRow()
                    musicList.pop(item)
                    self.playList.takeItem(item)
                except:
                    pass

    def CuntVolume(self):
        try:
            time.sleep(2)
            self.cuntVolume.hide() 
        except:
            pass
    
    def setVolume(self):
        try: 
            self.cuntVolume.show()
            self.volume = self.volumeSlider.value()
            mixer.music.set_volume(self.volume /100)
            self.cuntVolume.setText(str(self.volume))
            self.run_CuntVolume()
        except:
            pass
        

    def muteSound(self):
        global muted, get

        if muted == False:
            get = mixer.music.get_volume()
            mixer.music.set_volume(0.0)
            muted = True
            self.muteButton.setIcon(QIcon("icons/unmuted.png"))
            self.muteButton.setToolTip("UnMute")
            self.volumeSlider.setValue(0)

        else:
            mixer.music.set_volume(get)
            muted = False
            self.muteButton.setIcon(QIcon("icons/mute.png"))
            self.muteButton.setToolTip("Mute")
            self.volumeSlider.setValue(int(get*100))

    
    def updateSiderPlay(self):
        global count, songLength, sliderChange
        count += 1
        sliderChange = count
        self.siderPlay.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
        if count == songLength:
            self.timer.stop()
            self.NextSounds()
    
    def SliderChange(self):
        global sliderChange, count, sliderChangeStop,ind
        value = self.siderPlay.value()
        stat = self.playButton.toolTip()
        if self.playList.currentRow() == (-1):
            return
        if stat == "Play":
            if sliderChange != value and sliderChange != value+1:
                pass
            sliderChangeStop = True
            count = value
            sliderChange = value
        
            self.songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
            return
            
        if (stat == "Stop"  and sliderChange != value and sliderChange != value+1) or sliderChangeStop == True:
            mixer.music.load(musicList[self.playList.currentRow()])
            mixer.music.play(0,value)
            count = value
            self.songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
            sliderChangeStop = False

    def playPrevious(self):
        global ind
        
        try :
            indeX = self.playList.currentRow()
            if indeX == 0:
                ind = indeX
            else:
                ind = indeX-1
            self.playList.setCurrentRow(ind)
            self.playSounds()
        except Exception as error:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")

    def NextSounds(self):
        global ind
        try:
            indeX = self.playList.currentRow()
            item = self.playList.count()
            if indeX == item-1:
                ind = 0
            else:
                ind = indeX+1
            self.playList.setCurrentRow(ind)
            self.playSounds()
        except Exception as error:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")
    
    def Minimize(self):
        global statuwindow, Geometry
        self.playList.hide()
        if statuwindow == False:
            statuwindow = True
            self.playList.hide()
            self.widgett.hide()
            self.resize(QSize(300,150))
            
            ge0 = self.geometry()
            geometry = str(ge0).split("(")[1].split(",")
            
            self.setGeometry(int(geometry[0]), int(geometry[1]), int(geometry[2]), 150)
            self.widgett.show()
            self.minimize.setIcon(QIcon("icons/maximize.png"))
            self.setWindowOpacity(0.9)
            

        else:
            statuwindow = False
            
            ge0 = self.geometry()
            geometry = str(ge0).split("(")[1].split(",")[2].strip()
            
            self.playList.show()
            self.resize(int(geometry),500)
            self.minimize.setIcon(QIcon("icons/minimize (1).png"))
            self.setWindowOpacity(1)
        
    
    def StopSound(self):
        global cuntprogre
        count = self.playList.currentRow()
        if count == -1:
            return
        self.timer.stop()
        self.playButton.setIcon(QIcon("icons/play.png"))
        mixer.music.pause()

    def PlaySound(self):
        global pause
        #################
        try :
            count = self.playList.currentRow()
            if count == -1:
                return
            self.timer.start()
            self.playButton.setIcon(QIcon("icons/stop.png"))
            mixer.music.unpause()
            if count == 0:
                self.updateSiderPlay()
            #################
            pause = False
        except:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again")
    def StopPlaySound(self):
        state = self.playButton.toolTip()
        if state == "Play":
            self.playButton.setToolTip("Stop")
            self.PlaySound()
            
        elif state == "Stop":
            self.playButton.setToolTip("Play")
            self.StopSound()


    def ClearList(self):
        global musicList
        musicList = []
        self.playList.clear()

    def ClearCacheing(self):
        global musicList
        db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        musicList = []
        self.playList.clear()
        try:
            db.execute("DELETE FROM open")
            db.commit()
        except Exception as error:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")
        db.close()
    
    def BackButton(self):
        self.playList.show()
        self.topGroupBox.show()
        self.historyTable.hide()
        self.GbottumHistory.hide()
        self.combo.hide()

    def DeleteAll(self):
        global _historyCount, _historyTime
        db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        mass = QMessageBox.information(self, "DELETE History", "Are you sure to delete history", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if mass == QMessageBox.Yes:
            db.execute("DELETE FROM history")
            db.commit()
            _historyCount = {}
            _historyTime = {}
            self.History()
        db.close()
    def DeleteItem(self):
        global _historyCount,_historyTime
        db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        HItme = []
        for item in self.historyTable.selectedItems():
            v= item.text()
            HItme.append(v)
        
        for I in HItme:
            X = ""
            for i in _historyCount:
                if I == i.split("/")[-1]:
                    X = i
            try :
                _historyCount.pop(X,"No item returned")
                _historyTime.pop(X,"No item returned")
                db.execute("DELETE from history WHERE music=?",(X,))
                db.commit()
                self.History()
            except Exception as error:
                QMessageBox.information(self,"Deletion failed", f"Deletion failed\nYou may select the item (s) from the (Music) field\n\n{error}")


    def DeleteIteM(self):
        global musicList
        try:
            item = self.playList.currentRow()
            musicList.pop(item)
            self.playList.takeItem(item)
        except:
            QMessageBox.information(self,"Deletion failed","Deletion failed,\nyou have to choose an era before deleting")
    
    def History(self):
        self.playList.hide()
        self.topGroupBox.hide()
        self.historyTable.show()
        self.GbottumHistory.show()
        self.combo.show()
        # ########################
        Filter = self.combo.currentText()
        if Filter == "History Count":
            self.historyTable.setHorizontalHeaderItem(1, QTableWidgetItem("Count"))
            self.historyTable.setRowCount(len(_historyCount))
            c = 0
            history = {k: v for k, v in sorted(_historyCount.items(), key=lambda item: item[1], reverse=True)}
            for i in history:
                self.historyTable.setItem(c,0, QTableWidgetItem(f"{os.path.basename(i)}"))
                self.historyTable.setItem(c,1, QTableWidgetItem(f"{_historyCount[i]}"))
                c += 1
        else:
            def extract(s):
                return datetime.strptime(s, '%d/%m/%Y %H:%M:%S')
            Time = []
            for i in _historyTime:
                Time.append(_historyTime[i])
            historyTime =sorted(Time, key=lambda s: extract(s[0:19]))
            self.historyTable.setHorizontalHeaderItem(1, QTableWidgetItem("Time"))
            self.historyTable.setRowCount(len(_historyTime))
            c = 0
            for i in historyTime[::-1]:
                x = ''
                for I in _historyTime:
                    if i == _historyTime[I]:
                        x = I
                self.historyTable.setItem(c,0, QTableWidgetItem(f"{os.path.basename(x)}"))
                self.historyTable.setItem(c,1, QTableWidgetItem(f"{i}"))
                c += 1
        

    def Next5(self):
        if self.playList.currentRow() == (-1):
            return
        value = self.siderPlay.value()
        self.siderPlay.setValue(value+5)
    
    def Back5(self):
        if self.playList.currentRow() == (-1):
            return
        value = self.siderPlay.value()
        self.siderPlay.setValue(value-5)

    def Playhistory(self):
        global musicList, index
        Filter = self.combo.currentText()
        if Filter == "History Count":
            history = {k: v for k, v in sorted(_historyCount.items(), key=lambda item: item[1], reverse=True)}

            musicList = []
            self.playList.clear()
            for i in history:
                fileName = os.path.basename(i)
                self.playList.addItem(fileName)
                musicList.append(i)
            self.playList.setCurrentRow(0)
            self.playSounds()
        else:
            def extract(s):      
                return datetime.strptime(s, '%d/%m/%Y %H:%M:%S')
            Time = []
            for i in _historyTime:
                Time.append(_historyTime[i])
            historyTime =sorted(Time, key=lambda s: extract(s[0:19]))

            musicList = []
            self.playList.clear()
            for i in historyTime:
                x = ''
                for I in _historyTime:
                    if i == _historyTime[I]:
                        x = I

                fileName = os.path.basename(x)
                self.playList.addItem(fileName)
                musicList.append(x)
            self.playList.setCurrentRow(0)
            self.playSounds()

    def playHistoryTable(self):
        global musicList, ind
        items = self.historyTable.selectedItems()
        item = []
        for i in items:
            if i.column() == 1:
                return
            item.append(i.text())

        for i in item:
            for u in _historyCount:
                if i in u:
                    self.playList.addItem(i)
                    musicList.append(u)
        ind = self.playList.count()-len(item)
        self.playList.setCurrentRow(self.playList.count()-len(item))
        self.BackButton()
        self.playSounds()


    def MenuBar(self):
        self.menbar = self.menuBar()
        file = self.menbar.addMenu("File")
        eidt = self.menbar.addMenu("Edit")
        helpM = self.menbar.addMenu("Help")
        # ####################
        addItem = QAction("Add Sound", self)
        addItem.setShortcut("ctrl+a")
        addItem.triggered.connect(self.AddSound)
        file.addAction(addItem)
        
        addSounds = QAction("Add Sounds", self)
        addSounds.setShortcut("ctrl+s")
        addSounds.triggered.connect(self.AddSounds)
        file.addAction(addSounds)
        
        folder = QAction("Add Folder", self)
        folder.setShortcut("ctrl+alt+s")
        folder.triggered.connect(self.Folder)
        file.addAction(folder)

        history = QAction("History", self)
        history.setShortcut("ctrl+h")
        history.triggered.connect(self.History)
        file.addAction(history)

        

        playhistory = QAction("Play Music History", self)
        playhistory.setShortcut("shift+h")
        playhistory.triggered.connect(self.Playhistory)
        eidt.addAction(playhistory)

        MuteSound = QAction("Mute", self)
        MuteSound.setShortcut("ctrl+m")
        MuteSound.triggered.connect(self.muteSound)
        eidt.addAction(MuteSound)
        
        StopPlaySpund = QAction("Stop\Play Sound", self)
        StopPlaySpund.setShortcut(QKeySequence(Qt.Key_Space))
        StopPlaySpund.triggered.connect(self.StopPlaySound)
        eidt.addAction(StopPlaySpund)

        next5 = QAction("Next 5s", self)
        next5.setShortcut("ctrl+Right")
        next5.triggered.connect(self.Next5)
        eidt.addAction(next5)

        back5 = QAction("Back 5s", self)
        back5.setShortcut("ctrl+Left")
        back5.triggered.connect(self.Back5)
        eidt.addAction(back5)

        deleteItem = QAction("Delete Item", self)
        deleteItem.setShortcut(QKeySequence(Qt.Key_Delete))
        deleteItem.triggered.connect(self.DeleteIteM)
        eidt.addAction(deleteItem)

        clearList = QAction("Clear List",self)
        clearList.setShortcut(QKeySequence(16777223 , 76))
        clearList.triggered.connect(self.ClearList)
        eidt.addAction(clearList)

        clearCacheing = QAction("Clear Cacheing", self)
        clearCacheing.triggered.connect(self.ClearCacheing)
        clearCacheing.setShortcut(QKeySequence(Qt.Key_Delete,Qt.Key_A))
        eidt.addAction(clearCacheing)

        githop = QAction("GitHub",self)
        githop.triggered.connect(self.Githop)
        githop.setIcon(QIcon("icons\github.png"))
        helpM.addAction(githop)

        support = QAction("Support",self)
        support.triggered.connect(self.Support)
        support.setIcon(QIcon("icons\paypal.png"))
        helpM.addAction(support)

        about = QAction("About", self)
        about.triggered.connect(self.About)
        about.setIcon(QIcon(r"icons\about.png"))
        helpM.addAction(about)


    def Convert(self,src, Id):
        global musicList, _historyCount, _historyTime, ConvertId, MESSAGE
        ConvertId = Id
        print(f"Id:{Id}\nConvertId:{ConvertId}")
        dst = src.split(".")[0] + '.mp3'
        print(dst)
        if os.path.exists(dst) == False :
            try:
                try:
                    videoclip = AudioFileClip(src)

                    audioclip = videoclip
                    audioclip.write_audiofile(dst)

                    audioclip.close()
                    videoclip.close()
                except Exception as E:
                    print(f"Video:{E}")
                    videoclip = VideoFileClip(src)

                    audioclip = videoclip.audio
                    audioclip.write_audiofile(dst)

                    audioclip.close()
                    videoclip.close()
                
            except Exception as E:
                print(sys.argv)
                print(E)
                MESSAGE = E
                self.finished1.emit()
                return
        musicList[Id] = dst
        try:
            _historyCount.pop(src)
            _historyTime.pop(src)
        except:
            pass
        return self.finished.emit()

    def run_convert(self, src, index):
        global MESSAGE
        try:
            sel_items = self.playList.selectedItems()
            for item in sel_items:
                item.setText("Processing ...")
            Thread(target=self.Convert, args=(src, index)).start()
            
        except Exception as E :
            MESSAGE = E
            self.finished1.emit()
        return 


    def run_CuntVolume(self):
        try:
            Thread(target=self.CuntVolume).start() 
        except:
            pass
    def closeEvent(self, event):
        db = sqlite3.connect(f"{pathDB}\\Music Player\\Music.db")
        if len(musicList) != 0:
            try:
                db.execute("DELETE FROM open")
                db.commit()
            except Exception as error:
                QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")
            try:
                for i in musicList:
                    db.execute("INSERT INTO open(music) VALUES(?)",(i,))
                db.commit()
                
                
            
            except Exception as error:
                QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")

            try:
                db.execute("DELETE FROM history")
                db.commit()
                for i in _historyCount:
                    db.execute("INSERT INTO history(music,count) values (?,?)",(i,_historyCount[i]))
                    db.commit()

                for i in _historyTime:
                    db.execute("UPDATE history SET Time=? WHERE music = ?",(_historyTime[i],i))
                db.commit()

            except Exception as error:
                QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again\n\n{error}")
            db.close()
        sys.exit()
        
    def About(self):
        help_message = QMessageBox()
        help_message.setWindowIcon(QIcon(r"icons\icon.png"))
        with open("StyleMusicPlayer\\QMessgesBox.css", "r") as L:
            help_message.setStyleSheet(L.read())
        help_message.setWindowTitle('Music Player About')
        help_message.setText( "\t\tMusic Player\t\t <br>Version : 1.0<br><br>A completely free, open-source, ad-free song-playing program\n\n")
        help_message.setTextFormat(Qt.RichText)
        help_message.setInformativeText("<a style='color: #ff6666;' href='https://www.colonal.codes/search/label/MyPrograms'>Check for updates and discover other apps</a><br><br>COLONAL")
        help_message.exec_()
        

    def Githop(self):
        Mess = QMessageBox()
        Mess.question(self,"Support","My account will open on (GitHop) from the browser", QMessageBox.Yes|QMessageBox.Cancel,QMessageBox.Yes)
        with open("StyleMusicPlayer\\QMessgesBox.css", "r") as L:
            Mess.setStyleSheet(L.read())
        if Mess == QMessageBox.Yes:
            new = 2
            url = "https://github.com/colonal/My-projects"
            webbrowser.open(url,new=new)

    def Support(self):
        Mess = QMessageBox.question(self,"Support","\t\t\tThanks for your\t\t\n\nsupport it means a lot to me,a link from your browser will open to support\t", QMessageBox.Yes|QMessageBox.Cancel,QMessageBox.Yes)
        if Mess == QMessageBox.Yes:
            new = 2
            url = "https://paypal.me/mohammadch?locale.x=ar_EG"
            webbrowser.open(url,new=new)

    def OpenMusic(self):
        global openMusic
        if len(openMusic) > 0:
            pass


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            if "." in file_path.split("\\")[-1]: 
                i = os.path.basename(file_path).split(".")[-1]
                
                if i == "m4a" or i == "mp3" or i == "wav" or i == "mp4" or i == "wmv" or i == "aac" or i == "wma" or i == "ogg":
                    
                    fileName = os.path.basename(file_path)
                    self.playList.addItem(fileName)
                    musicList.append(file_path)
            else:
                name = os.listdir(file_path)
                for I in name :
                    x =  os.path.basename(I).split(".")[-1]
                    if x== "m4a"or x == "mp3" or x == "wav" or x == "mp4" or x == "wmv" or x == "aac" or x == "wma" or x == "ogg":
                        fileName = os.path.basename(I)
                        self.playList.addItem(fileName)
                        musicList.append(file_path+"/"+I)

            event.accept()
        else:
            event.ignore()
def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())

if __name__ == "__main__":
    path = sys.argv
    try:
        if len(path) > 1:
            for i in path:
                x =  os.path.basename(i).split(".")[-1]
                if x == "exe":
                    i = os.path.dirname(i)
                    os.chdir(i)
                if x == "m4a" or x == "mp3" or x == "wav" or x == "mp4" or x == "wmv" or x == "aac" or x == "wma" or x == "ogg":
                    openMusic = i
    except:
        pass
    try:
        main()
    except Exception as error:
        A.alert( f"{error}", "eroor")
