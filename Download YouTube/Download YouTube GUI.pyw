from __future__ import unicode_literals
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import youtube_dl
import threading
import time
import os
from tkinter.filedialog import askdirectory
import keyboard

root = Tk()
root.title("Downloade YOUTUBE")
root.geometry("400x100+400+200")
root.resizable(0, 0)
root.config(bg = 'red3')
var = StringVar()

x = 1


def Download():
	global x
	try:
		ydl_opts = {}
		dirk = askdirectory()
		os.chdir(dirk)
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			x = ydl.download([str(e.get())])
		messagebox.showinfo('succeeded', 'The download was successful\n{}'.format(dirk))
		var.set('')
	except:
		e.configure(fg='red')
		var.set('Error URL')
		x = 0


def Progressbar():
	global x
	progressbar.place(x=90, y=65)
	c = 0
	while c < 101:
		if x != 0:
			if c == 100:
				break
			progressbar['value'] = c
			c += 1
			time.sleep(1)
		else:
			progressbar['value'] = 100
			break


def run():
	if var.get() != '' and var.get() != 'Error URL':
		threading.Thread(target=Download).start()
		time.sleep(4)
		threading.Thread(target=Progressbar).start()
	else:
		e.configure(fg='red')
		var.set('Error URL')


def Enter():
	if var.get() != '' and var.get() != 'Error URL':
		run()


keyboard.add_hotkey('enter', lambda: Enter())

b = Button(root, text='downloade',
           command=run, bg='red',
           fg='white', font=('arial', 10, 'bold'),
           activebackground='white',
           activeforeground='red'
           )

e = Entry(root, width=30,
          font=('arial', 10, 'bold'),
          textvariable=var,
          bg='white'
          )

progressbar = ttk.Progressbar(root, orient=HORIZONTAL,
                              length=250,
                              mode='determinate',
                              maximum=100, value=0
                              )

e.place(x=110, y=20)
b.place(x=10, y=17)
e.focus()

root.mainloop()
