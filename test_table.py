from tkinter import *
from pandastable import Table, TableModel
import pandas as pd
from flylogger import authorize
from flylogger import experiment
from flylogger import load
from flylogger import show
from flylogger import app

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        # create a toplevel menu
        menubar = Menu(self)
        menubar.add_command(label="Load", command=self.data_window)
        menubar.add_command(label="Quit", command=self.quit)
        self.parent.config(menu=menubar)

        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)

        #print(show.sheets(my_client))
        df = pd.DataFrame({'EMPTY' : ['NA']})
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=False, showstatusbar=True)
        pt.show()
        return

    def data_window(self):
        global id_entry
        self.window_entry = Toplevel()   # Change to Toplevel (a popup) instead of a new Tk instance
        self.window_entry.title('Load googlesheet by ID or name')
        Label(self.window_entry, text = 'Enter the google spreadsheet ID or name:').grid(sticky = W, columnspan = 2)
        id_entry = Entry(self.window_entry, width = 55)
        id_entry.grid(sticky = W, columnspan = 2)
        Button(self.window_entry, text = 'Submit', command = self.submit_id).grid(row = 10, column = 0, sticky = W + E)
        Button(self.window_entry, text = 'Cancel', command = self.window_entry.destroy).grid(row = 10, column = 1, sticky = W + E)

    def submit_id(self):
        global id_entry
        _ID = str(id_entry.get())
        my_client = authorize.me()
        sht = my_client.open(_ID)
        worksheet = sht.worksheet()
        df = worksheet.get_as_df()
        model = TableModel(dataframe=df)
        self.table.updateModel(model)
        self.window_entry.destroy()

root = Tk()
app = TestApp(parent=root)
#launch the app
app.mainloop()
