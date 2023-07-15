import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Scrollbar Example")

# Create a frame
frame = ttk.Frame(window)
frame.grid(row=0, column=0, sticky="nsew")

# Create a scrollbar
scrollbar = ttk.Scrollbar(frame)
scrollbar.grid(row=0, column=1, sticky="ns")

# Create a Treeview widget within the frame
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
tree.grid(row=0, column=0, sticky="nsew")

# Configure the scrollbar to work with the Treeview widget
scrollbar.config(command=tree.yview)

# Add columns to the Treeview
tree["columns"] = ("Name", "Age")

# Format the columns
tree.column("#0", width=100)
tree.column("Name", width=100)
tree.column("Age", width=100)

# Add headings to the columns
tree.heading("#0", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")

# Add 20 items to the Treeview
for i in range(1, 21):
    tree.insert("", tk.END, text=str(i), values=("Name " + str(i), str(i * 5)))

# Configure grid weights to make the frame expandable
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Start the main event loop
window.mainloop()
