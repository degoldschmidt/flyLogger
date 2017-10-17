import pygsheets
import tkinter as tk
from tkinter import filedialog, messagebox

def me():
    try:
        return pygsheets.authorize()
    except FileNotFoundError:
        tk.Tk().withdraw()
        messagebox.showwarning("client_secret json file could not be found.",
                               "Please follow the instructions.")
        loaded = False
        while not loaded:
            if messagebox.askyesno("Load json file", "Have you downloaded a client json file for authorizing credentials?"):
                filename = filedialog.askopenfilename(title="Load json file", defaultextension='.json')
                return pygsheets.authorize(outh_file=filename)
            else:
                messagebox.showwarning("Please create and download Google API credentials.",
                                       "Please follow the instructions in following website for Step 1.")
                import webbrowser
                webbrowser.open('https://developers.google.com/sheets/api/quickstart/python')
