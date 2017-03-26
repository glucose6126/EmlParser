try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
import sqlite3
import sys
import os

def get_list_data() :
    conn = sqlite3.connect(dbfile)
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute('select lid, filename, ext, filememe from attach where emlNumber=' + str(eml))
    data_list = cur.fetchall()
    return data_list

class filelist(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print "start " + dbfile.split('.')[0] + '_output/' + eml + "/" + self.tree.item(item)['values'][1]
        os.system("start " + dbfile.split('.')[0] + '_output/' + eml + "/" + self.tree.item(item)['values'][1])

    def _setup_widgets(self):
        # s = ""
        # msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
        #     padding=(10, 2, 10, 6), text=s)
        # msg.pack(fill='x')
        viewercontainer = ttk.Frame()
        viewercontainer.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=data_header, show="headings")
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=viewercontainer)
        vsb.grid(column=1, row=0, sticky='ns', in_=viewercontainer)
        hsb.grid(column=0, row=1, sticky='ew', in_=viewercontainer)
        viewercontainer.grid_columnconfigure(0, weight=1)
        viewercontainer.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        data_header = ['lid', 'fileName', 'ext', 'meme']
        data_list   = get_list_data() #dummy
        # widthSet = [20, 40, 40, 40, 40,40,40, 80]
        for col in data_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        # for i in range(0, 8) :
        #     self.tree.column(col, width=widthSet[i])
        for item in data_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            # count = 0
            for ix, val in enumerate(item):
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

data_header = ['lid', 'fileName', 'ext', 'meme']
data_list = ['1', '1', '1']

global dbfile
dbfile = sys.argv[2]
global eml
eml = sys.argv[1]

fileviewr = tk.Tk()
fileviewr.title("fileViewer - Glucose")
listbox = filelist()
fileviewr.mainloop()