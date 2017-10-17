import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.menubar = self.get_topmenu({   'Load stocks': self.open_sheet,
                                            'Cross': [('New', None)],
                                            'Experiment': [('New', None)],
                                            'Show': self.show,
                                            })

        try:
            self.parent.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.parent.tk.call(master, "config", "-menu", self.menubar)

        self.canvas = tk.Canvas(self, bg="white", width=400, height=400,
                             bd=0, highlightthickness=0)
        self.canvas.pack()

        ### data
        self.id = None ## current spreadsheet id

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

    def open_sheet(self):
        window = tk.Tk()
        window.title("Load Google sheets by name/id")
        lbl = tk.Label(window, text='Please type in a name or id of your Google spreadsheet')
        ent = tk.Entry(window, textvariable=self.id)
        btn = tk.Button(window, text='Submit', command=window.destroy)
        lbl.pack()
        ent.pack()
        btn.pack()

    def show(self):
        print(self.id)

def run():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.title("flyLogger 0.0.1")
    root.mainloop()
