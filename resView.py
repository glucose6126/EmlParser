try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
import sqlite3
import os
import sys
def get_list_data(source) :
    global dbfile
    dbfile = source
    conn = sqlite3.connect(source)
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute('select lid, sendName, sendID, recvName, recvID, subject from data')

    # select count() from attach where emlNumber=69 and filename NOT LIKE 'EMLParser%';
    datalist = cur.fetchall()
    res = []
    for i in datalist :
        count = cur.execute("select count() from attach where emlNumber=" + str(i[0]) + " and filename NOT LIKE 'EMLParser%'").fetchone()[0]
        res.append(i + (count,))
    return res

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def OnDoubleClick(self, event):
        global dbfile
        item = self.tree.selection()[0]
        # print "start pythonw fileviewer.py " + str(self.tree.item(item)['values'][0]) + " " + dbfile
        os.system("start pythonw fileviewer.py " + str(self.tree.item(item)['values'][0]) + " " + dbfile)

    def _setup_widgets(self):
        # s = ""
        # msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
        #     padding=(10, 2, 10, 6), text=s)
        # msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=data_header, show="headings")
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        data_header = ['number', 'send_Name', 'send_ID', 'recv_Name', 'recv_ID', 'subject', 'file_count']
        data_list   = get_list_data(dbfile) #dummy
        # widthSet = [20, 40, 40, 40, 40,40,40, 80]
        for col in data_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        # for i in range(0, 8) :
        #     self.tree.column(col, width=widthSet[i])
        for item in data_list:
            try:
                self.tree.insert('', 'end', values=item)
            except :
                try :
                    self.tree.insert('', 'end', values=item[0:5] + (item[5].decode('euc-kr'),) + (item[6:]))
                except :
                    print item
            # adjust column's width if necessary to fit each value
            # count = 0
            for ix, val in enumerate(item):
            #     if count == 0 :
            #         col_w = 20
            #     elif count >= 1 and count <= 5 :
            #         col_w = 40
            #     else :
            #         col_w = 80
                col_w = tkFont.Font().measure(val)
                if col_w > 300 :
                    col_w = 300
                if self.tree.column(data_header[ix],width=None)<col_w:
                    self.tree.column(data_header[ix], width=col_w)
            #     count = count + 1

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

# the test data ...

data_header = ['number', 'send_Name', 'send_ID', 'recv_Name', 'recv_ID', 'subject', 'file_count']
# data_list = [
# ('Hyundai', 'brakes') ,
# ('Honda', 'light') ,
# ('Lexus', 'battery') ,
# ('Benz', 'wiper') ,
# ('Ford', 'tire') ,
# ('Chevy', 'air') ,
# ('Chrysler', 'piston') ,
# ('Toyota', 'brake pedal') ,
# ('BMW', 'seat')
# ]
data_list = []


root = tk.Tk()
root.title("resViewer - Glucose")
global dbfile
now ='2017_03_16_05_40_06.db'
dbfile = sys.argv[1]
listbox = MultiColumnListbox()
root.mainloop()