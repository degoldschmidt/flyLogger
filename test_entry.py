import tkinter as tk
import os, shelve

food_entry = None

# Opens a new window for entering food items
def data_window():
    global food_entry
    new_window_entry = Toplevel()   # Change to Toplevel (a popup) instead of a new Tk instance
    new_window_entry.title('Load googlesheet by ID or name')
    Label(new_window_entry, text = 'Enter the google spreadsheet ID or name:').grid(sticky = W, columnspan = 2)
    food_entry = Text(new_window_entry, width = 55, height = 2, wrap = WORD)
    food_entry.grid(sticky = W, columnspan = 2)
    Button(new_window_entry, text = 'Submit', command = check_data).grid(row = 10, column = 0, sticky = W + E)
    Button(new_window_entry, text = 'Cancel', command = new_window_entry.destroy).grid(row = 10, column = 1, sticky = W + E)

def check_data():
    global food_entry
    print(food_entry.get(1.0, END))
    """
    if food_entry.get(1.0, END).strip() == '':
       print('Nothing Entered')
    else:
        print('Next Function')
    """

root = Tk()
root.title('')
# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label="Load", command=data_window)
menubar.add_command(label="Quit", command=root.quit)

# display the menu
root.config(menu=menubar)
Label(root, text = 'Food Tracker v3.0').grid(columnspan = 2)
#Button(root, text = 'Enter Data', command = data_window).grid(row = 1, column = 0, sticky = W)
#Button(root, text = 'View Data', command = view_window).grid(row = 1, column = 1, sticky = E)
root.mainloop()
