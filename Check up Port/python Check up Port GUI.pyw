from tkinter import *
from tkinter import ttk
import socket
import threading
import keyboard
import time

root = Tk()
root.title('Check up Port test')
root.geometry("295x230+400+200")
root.resizable(0, 0)
root.configure(bg='gray37')
# _________________________________
varH = StringVar()
varP = StringVar()


def search():
	global varH
	global varP
	global t_search
	try:
		root.geometry('295x353')
		t_search.delete(1.0, 'end')
		host = varH.get()
		Rport = varP.get()
		time = 0.5
		# -------------------------
		c = 0
		h = 0
		for i in host.strip():
			if i in 'qwertyuioplkjhgfdsazxcvbnm':
				c += 1

		if c == 0:
			time = 0.01
		else:
			host = socket.gethostbyname(host)
		t_search.insert(END, f'the target: {host}\n')
		# -------------------------
		try:
			if varH.get() != '' and varP.get() != '' and varP.get() != '0':# and int(varP.get()) <= 65535 :
				rang = str(varP.get())
				rang = list(rang)
				if '.' not in  rang:
					varP.set('')
					with open("port.txt", "r")as Nport:
						N = Nport.read()
						for port in range(1, int(Rport) + 1):
							varP.set(str(port))
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							socket.setdefaulttimeout(time)
							result = s.connect_ex((host, port))
							if result == 0:
								for n in N.split('\n'):
									for g in n.split():
										if g == str(port):
											t_search.insert(END, f'The port  {n}  is open.\n')
											h += 1
				else:
					Rport = varP.get()
					port = []
					for i in Rport.split('.'):
						port.append(i)
					try:
						with open("port.txt", "r")as Nport:
							N = Nport.read()
							for port in port:
								varP.set(str(port))
								s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								socket.setdefaulttimeout(time)
								result = s.connect_ex((host, int(port)))
								if result == 0:
									for n in N.split('\n'):
										for g in n.split():
											if g == str(port):
												t_search.insert(END, f'The port  {n}  is open.\n')
												h += 1
					except:
						pass
			else:
				pass
		except Exception as x:
			t_search.insert(END, f'Error tray again \n{x}')
		varP.set("")
		if h == 0:
			t_search.insert(END, '\nDone\t\'There is no port open\'')
		else:
			t_search.insert(END, '\nDone')
	except Exception as x:
		t_search.insert(END, 'Please enter valid data')


def run():
	threading.Thread(target=search).start()


def Enter():
	if str(e_host.focus_get()) == '.!entry':
		e_port.select_range(0, END)
		e_port.focus()
	elif str(e_port.focus_get()) == '.!entry2':
		run()
		e_host.select_range(0, END)
		e_host.focus()
	else:
		e_host.select_range(0, END)
		e_host.focus()
keyboard.add_hotkey('enter', lambda: Enter())

# _________________________________

h = socket.gethostname()
i = socket.gethostbyname(h)
varH.set(i)

l_hello = Label(root, text=f'Hello {h}', font=('arial', 10, 'bold'), bg='gray37', )
l_hello.place(x=90, y=3)
l_host = Label(root, text='host', font=('arial', 11, 'bold'), bg='gray37')
l_host.place(x=120, y=30)
e_host = Entry(root, font=("arial", 12, 'bold'), textvariable=varH, bg='gray57')
e_host.place(x=50, y=55)
l_port = Label(root, text='Range in port', font=('arial', 11, 'bold'), bg='gray37')
l_port.place(x=90, y=100)
e_port = Entry(root, font=("arial", 12, 'bold'), textvariable=varP, bg='gray57')
e_port.place(x=50, y=125)
b_search = Button(root, text='Search', font=('arial', 10, 'bold'), command=lambda: run(), bg='gray37')
b_search.place(x=110, y=180)
###################################
fr = ttk.Frame(root, width=120, height=40, relief=RIDGE)
fr.place(x=0, y=240)
t_search = Text(fr, width=39, height=7, wrap='word', font=('arial', 10, 'bold'), bg='black', fg='green')
t_search.pack(side='left')
sb = Scrollbar(fr)
sb.pack(side='right', fill='y')

t_search.config(yscrollcommand='sb.set')
sb.config(command=t_search.yview)

if __name__ == "__main__":
	e_host.select_range(0, END)
	e_host.focus()
	root.mainloop()
