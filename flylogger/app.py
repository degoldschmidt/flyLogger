import tkinter as tk
import pandastable as pdt
import pandas as pd
import json
from pprint import pprint
from tkinter.filedialog import askopenfilename

class MainApplication(tk.Frame):
    def __init__(self, parent, client=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.menubar = self.get_topmenu({   'File': [ ('Open file...', self.open_file),
                                                      ('Save as...', self.parent.quit),
                                                      ('Quit flyLogger', self.parent.quit)]
                                            })
        try:
            self.parent.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.parent.tk.call(master, "config", "-menu", self.menubar)

        self.main = self.master
        self.main.geometry('600x400+200+100')
        f = tk.Frame(self.main)
        f.pack(fill=tk.BOTH,expand=1)

        #EMPTY TABLE
        df = pd.DataFrame({'' : []})
        self.table = pt = pdt.Table(f, dataframe=df, showtoolbar=False, showstatusbar=False)
        pt.show()

        ### data
        #self.client = client
        #self.id = tk.StringVar() ## current spreadsheet id
        return

    def get_topmenu(self, menu_dict):
        menubar = tk.Menu(self)
        for k, val in menu_dict.items():
            menu = tk.Menu(menubar, tearoff=0)
            if type(val) is list:
                menubar.add_cascade(label=k, menu=menu)
                for v in val:
                    menu.add_command(label=v[0], command=v[1])
            else:
                menubar.add_command(label=k, command=val)

        return menubar

    def entry_id(self):
        global id_entry
        self.window_entry = tk.Toplevel()   # Change to Toplevel (a popup) instead of a new Tk instance
        self.window_entry.title('Load googlesheet by ID or name')
        tk.Label(self.window_entry, text = 'Enter the google spreadsheet ID or name:').grid(sticky = tk.W, columnspan = 2)
        id_entry = tk.Entry(self.window_entry, width = 55)
        id_entry.grid(sticky = tk.W, columnspan = 2)
        tk.Button(self.window_entry, text = 'Submit', command = self.submit_id).grid(row = 10, column = 0, sticky = tk.W + tk.E)
        tk.Button(self.window_entry, text = 'Cancel', command = self.window_entry.destroy).grid(row = 10, column = 1, sticky = tk.W + tk.E)

    def open_file(self):
        filename = askopenfilename(title='Open experiment file', filetypes=[("JSON files","*.json"), ("Text files","*.txt"), ("YAML files","*.yaml")])
        if filename.endswith('json'):
            with open(filename) as f:
                data = json.load(f)
        elif filename.endswith('txt'):
            with open(filename) as f:
                d = dict(x.rstrip().split(None, 1) for x in f)
        elif filename.endswith('yaml'):
            with open(_file, 'r') as f:
                data = yaml.load(f)
        pprint(data)

    def submit_id(self):
        global id_entry
        _ID = str(id_entry.get())
        sht = self.client.open(_ID)
        worksheet = sht.worksheet()
        df = worksheet.get_as_df()
        model = pdt.TableModel(dataframe=df)
        self.table.updateModel(model)
        self.window_entry.destroy()

    def show(self):
        print(self.id.get())


def run(client=None):
    root = tk.Tk()
    MainApplication(root, client).pack(side="top", fill="both", expand=True)
    root.title("flyLogger 0.0.1")
    root.mainloop()
