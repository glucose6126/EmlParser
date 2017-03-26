from Tkinter import *
import tkFileDialog
import emlModule
import os

def fileAdd() :
	filez = tkFileDialog.askopenfilenames(parent=F, title="Choose EML files")
	filez = F.tk.splitlist(filez)

	for i in filez :
		listbox.insert(END, i)

def fileDel() :
	lambda lb=listbox: listbox.delete(lb)

def Make() :
	res = emlModule.emlparser(listbox.get(0, END))
	os.system("start pythonw resView.py " + res)

def Open() :
	filez = tkFileDialog.askopenfilename(parent=F, title="Select DB")
	os.system("start pythonw resView.py " + filez)

def Export() :
	filez = tkFileDialog.askopenfilename(parent=F, title="Select DB")
	os.system("start pythonw csvExport.py " + filez)

def fileselect(evt) :
	index = int(listbox.curselection()[0])
	value = listbox.get(index)

	L = Tk()
	L.minsize(width=100, height=300)
	L.wm_title(value)

	fileText = Text(L, height=100, width=200)
	fileText.pack()
	fileText.insert(END, open(value, 'rb').read())
	L.mainloop()

###############################################################

T = Tk()
T.title("EML Parser - Glucose")
T.resizable(width=False, height=False)
T.minsize(width=500, height=500)

F = Frame(T, width=500, height=300)
F.pack()

Fbtn = Frame(T, width=500, height=200)
Fbtn.pack()

###############################################################

###############################################################

listbox = Listbox(F, selectmode=EXTENDED, width=120, height=30)
listbox.pack(side=LEFT)

###############################################################

###############################################################

addBtn = Button(Fbtn, text='Select File', width=23, height=5, command=fileAdd)
addBtn.pack(side=LEFT, pady=5)
delBtn = Button(Fbtn, text="Delete File", width=23, height=5, command=lambda lb=listbox: listbox.delete(ANCHOR))
delBtn.pack(side=LEFT, pady=5)
runBtn = Button(Fbtn, text="make DB", width=23, height=5, command=Make)
runBtn.pack(side=LEFT, pady=5)
openBtn = Button(Fbtn, text="DB Open", width=23, height=5, command=Open)
openBtn.pack(side=LEFT, pady=5)
exportBtn = Button(Fbtn, text="Export", width=23, height=5, command=Export)
exportBtn.pack(side=LEFT, pady=5)

###############################################################

###############################################################
T.mainloop()

###############################################################