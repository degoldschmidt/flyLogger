import tkinter as tk
import tkinter.ttk as ttk
import pandastable as pdt
import pandas as pd
import json
from pprint import pprint
from tkinter.filedialog import askopenfilename
from pandastable import Table
import gspread

class FlyloggerData(object):
    def __init__(self):
        pass

class FlyloggerTable(object):
    def __init__(self):
        pass

COLUMNS = ['Stock ID', 'GAL4/SplitGAL4', 'Genotype']
TITLE = "CR Lab Foraging Screen Stocks"

def filter_E(df, col):
    for index, row in df.iterrows():
        if type(row[col]) is not str:
            if str(df.loc[index,col]).count('0') > 1:
                df.loc[index,col] = str(df.loc[index,col])[:2]+'E{:02d}'.format(str(df.loc[index,col]).count('0')-1)
            else:
                df.loc[index,col] = str(df.loc[index,col])
            #print('Changed to', df.loc[index,col])
    return df

class FlyloggerApp(ttk.Frame):
        """Basic test frame for the table"""
        def __init__(self, parent, creds):
            self.parent = parent
            ttk.Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Table app')
            f = ttk.Frame(self.main)
            f.pack(fill=tk.BOTH,expand=1)

            self.gc = gspread.authorize(creds)

            self.wks = self.gc.open(TITLE).sheet1
            self.df = pd.DataFrame(self.wks.get_all_records())
            self.df = filter_E(self.df, 'GAL4/SplitGAL4')
            self.df = self.df.loc[:,COLUMNS]
            self.table = Table(f, dataframe=self.df,
                                    showtoolbar=False, showstatusbar=True)
            self.table.editable = False
            self.table.show()

            self.counter = 0
            self.update()
            self.parent.mainloop()

        def update(self):
            if self.counter == 5000:
                self.wks = self.gc.open(TITLE).sheet1
                self.df = pd.DataFrame(self.wks.get_all_records())
                self.df = filter_E(self.df, 'GAL4/SplitGAL4')
                self.df = self.df.loc[:,COLUMNS]
                self.table.model.df = self.df
                self.table.redraw()
                self.counter = 0
            self.counter +=1
            self.parent.after(1, self.update)
