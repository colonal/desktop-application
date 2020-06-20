from tkinter import*
from tkinter import messagebox
from typing import TextIO

win = Tk()
win.geometry('600x110+400+200')
win.title('save password')
win.configure(bg = 'gray26')
win.resizable(0, 0)
############################
varP = StringVar()
varRP = StringVar()
#######
varS = StringVar()
varD = StringVar()
varM = StringVar()
varP1 = StringVar()
########
##############################

with open('Name.txt', 'a')as txt:
    pass
with open('NDomain.txt', 'a')as txt:
    pass
with open('db.txt', 'a')as txt:
    pass


def save():
    d = open('NDomain.txt', 'r')
    u = d.readlines()
    laSu = Label(win, text = 'Fill out all fields   ',
                bg = 'gray26',
                fg = 'gray26',
                font = ('arial', 10))
    laSu.place(x = 140, y = 240)
    c = 0
    c1 = 0
    if varD.get() != '':
        c += 1
    if varM.get() != '':
        c += 1
    if varP1.get() != '':
        c += 1
    for i in u:
        for i1 in i.split('\n'):
            if varD.get() == i1:
                c1 += 1
    if c == 3 and c1 == 0:
        db = open('db.txt', 'a+')
        D = open('NDomain.txt', 'a+')
        D.write(varD.get() + '\n')
        db.write('#'*15 + '\n')
        db.write(varD.get()+ '\n')
        db.write(varM.get() + '\n')
        db.write(varP1.get() + '\n')
        db.write('#'*15 + '\n')
        varD.set('')
        varM.set('')
        varP1.set('')
        db.close()
        D.close()
        laSu = Label(win, text = 'successful',
                   bg = 'gray26',
                   fg = 'hot pink',
                   font = ('arial', 10))
        laSu.place(x = 155, y = 240)
    elif c != 3:
        laSu.configure(fg = 'hot pink')
    else:
        laSu.configure(fg = 'hot pink', text = 'Already registered')


def ShowAllCod():
    db = open('db.txt', 'r')
    text = db.read()
    te.insert(INSERT, text)
    db.close()
    
 
def sarsh():
    l32 = Label(win, text = 'Not Find',
                bg = 'gray26',
                fg = 'gray26',
                font = ('arial', 10))
    l32.place(x = 155, y = 360)
        #############
    
    global te
    
    win.geometry('580x400+400+200')
    te = Text(win, width = 35, height = 27,
                wrap = 'word',
                bg  = '#b6b6b6',
                font = ('arial', 9, 'bold'))
                       
    te.place(x = 330, y = 0)
    te.insert(INSERT, 'bbb')
        ##############
        ##############
    try:
        te.delete("1.0","end")
        D = open('NDomain.txt', 'r')
        x = D.readlines()
        D.close()
        l32.configure(fg = 'gray26')
        def S():
            
            db = open('db.txt', 'r')
            u = db.readlines()
            c = 0
            v = 0
            b = 0
            if varS.get() != '':
                for i in u:
                    for i1 in i.split('\n'):
                        if b == 0:
                            if i1 == varS.get():
                                v += c
                                x = u[(v-1)]+u[(v)]+u[(v+1)]+u[(v+2)]+u[(v+3)]                 
                                te.insert(INSERT, x)
                                db.close()
                                b += 1
                    c += 1
            else:
                te.delete("1.0","end")
                l32.configure(fg = 'hot pink', text = 'Not Find')
                
                
    
        xx = 0
        for i in x:
            for i1 in i.split('\n'):
                if i1 == varS.get():
                    S()
                    xx += 1
        if xx == 0:
            te.delete("1.0","end")
            l32.configure(fg = 'hot pink', text = 'Not Find')
            
             
                    
        
    except Exception as a:
        pass


c = 0
def ShowAll():
    
    def p():
        global c
        c += 1

    def ShowAl():
        
        global c
        global te
        varS.set('')
        win.geometry('580x400+400+200')
        te = Text(win, width = 35, height = 27,
                    wrap = 'word',
                    bg  = '#b6b6b6',
                    font = ('arial', 9, 'bold'))
            
        sb = Scrollbar(win)
        sb.pack(side = 'right', fill ='y')
        if c > 1:
            sb.pack_forget()
            
        te.place(x = 330, y = 0)

        sb.config(command = te.yview)
        te.config(yscrollcommand = sb.set)
        db = open('db.txt', 'r')
        text = db.read()
        te.insert(INSERT, text)
        db.close()
        c = 1
    p()
    ShowAl()
    
        
    
def cacklogin():
    global l22
    ###################
    
    ##############################
    pa = ''
    with open('Name.txt', 'r')as pas:
        pa += pas.read()
    if varP.get() == pa:
        l22.place_forget()
        lP.place_forget()
        eP.place_forget()
        bu.place_forget()
        scren()
    else:
        l22.configure(text = 'Please enter a valid password')
        varP.set('')
        



def cacksinup():
    global l23
    if varP.get() != '':
        if varP.get() == varRP.get():
            megb = messagebox.showinfo('title', '''Remember Password well
You will not be able to reset Password again''')
            with open('Name.txt', 'a')as pas:
                pas.write(varP.get())
            lPS.place_forget()
            lRPS.place_forget()
            ePS.place_forget()
            eRPS.place_forget()
            buS.place_forget()
            l23.place_forget()
            login()
        else:
            l23.configure(text = 'Please enter a valid password')
            varP.set('')
            varRP.set('')
            

####################################
def login():
    global lP
    global eP
    global bu
    global l22
    win.geometry('400x130+400+200')
    
    lP = Label(win, text = 'Password',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 14, 'bold'))

    
    eP = Entry(win, bg = '#b6b6b6',
               fg = 'black',
               font = ('airal', 13 , 'bold'),
               show = '*',
               textvariable = varP)
    bu = Button(win, text = 'Login',
                bg = 'gray26',
                fg = 'gray3',
                font = ('airal', 10 , 'bold'),
                command = cacklogin)
    l22 = Label(win, 
                    bg = 'gray26',
                    fg = 'hot pink',
                    font = ('arial', 10))
    
    ######################################
    
    lP.place(x = 30, y = 30)
    eP.place(x = 160, y = 32)
    bu.place(x = 180, y = 75)
    l22.place(x = 130, y = 105)

def sinup():
    
    win.geometry('300x210+400+200')
    global lPS
    global lRPS
    global ePS
    global eRPS
    global buS
    global l23
    lPS = Label(win, text = 'Password',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 14, 'bold'))
    lRPS = Label(win, text = 'Rewriting',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 14, 'bold'))
    
    ePS = Entry(win, bg = '#b6b6b6',
               fg = 'black',
               font = ('airal', 10 , 'bold'),
               textvariable = varP)
    eRPS = Entry(win, bg = '#b6b6b6',
               fg = 'black',
               font = ('airal', 10 , 'bold'),
               textvariable = varRP)
    buS = Button(win, text = 'Sinup',
                bg = 'gray26',
                fg = 'gray3',
                font = ('airal', 12 , 'bold'),
                command = cacksinup)
    l23 = Label(win, 
                        bg = 'gray26',
                        fg = 'hot pink',
                        font = ('arial', 10))
    
    ####################################################
    lPS.place(x = 10, y = 30)
    lRPS.place(x = 10, y = 100)
    ePS.place(x = 130, y = 30)
    eRPS.place(x = 130, y = 100)
    buS.place(x = 120, y = 150)
    l23.place(x = 80, y = 183)



def scren():
    global buA

  
    win.geometry('370x390+400+200')
        
    lD = Label(win, text = 'Web site name',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 11, 'bold'))
    lM = Label(win, text = 'Emile',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 14, 'bold'))
    lP1 = Label(win, text = 'Password',
                bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 12, 'bold'))
    lS = Label(win, text = 'Web site name',
               bg = 'gray26',
               fg = 'gray5',
               font = ('arial', 11, 'bold'))
        
    eD = Entry(win, bg = '#b6b6b6',
                fg = 'black',
                font = ('airal', 10 , 'bold'),
                textvariable = varD)
    eM = Entry(win, bg = '#b6b6b6', 
                fg = 'black',
                font = ('airal', 10 , 'bold'),
                textvariable = varM)
    eP = Entry(win, bg = '#b6b6b6',
                fg = 'black',
                font = ('airal', 10 , 'bold'),
                textvariable = varP1)
    eS = Entry(win, bg = '#b6b6b6', 
                fg = 'black',
                font = ('airal', 10 , 'bold'),
                textvariable = varS)
        
    bu = Button(win, text = 'Save',
                bg = 'gray26',
                fg = 'gray3',
                font = ('airal', 10 , 'bold'),
                command = save)
    buS = Button(win, text = 'Sarsh',
                bg = 'gray26',
                fg = 'gray3',
                font = ('airal', 10 , 'bold'),
                 command = sarsh)
    buA = Button(win, text = 'Show all',
                bg = 'gray26',
                fg = 'gray3',
                font = ('airal', 10 , 'bold'),
                command = ShowAll)
    
##########################################               
    lD.place(x = 15, y = 30)
    lM.place(x = 30, y = 100)
    lP1.place(x = 30, y = 170)
    lS.place(x = 15, y = 280)
    eD.place(x = 130, y = 30)
    eM.place(x = 130, y = 100)
    eP.place(x = 130, y = 170)
    eS.place(x = 130, y = 280)
    bu.place(x = 165, y = 210)
    buS.place(x = 145, y = 320)
    buA.place(x = 193, y=320)
##########################################

with open('Name.txt', 'r')as FN:
    d = FN.read()
    if len(d) == 0:
        sinup()
    
    else:
        
        login()


win.mainloop()
