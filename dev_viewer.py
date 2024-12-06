import json
import tkinter as tk
from tkinter import ttk, scrolledtext

# Load JSON data
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Create the main window
root = tk.Tk()
root.title("Timetable Viewer")

# Create a treeview to display the timetable
tree = ttk.Treeview(root)
tree.pack(expand=True, fill='both')

# Define columns
tree["columns"] = ("events", "3_grade", "2G_grade", "2I_grade", "1_grade")
tree.column("#0", width=100, minwidth=100)
tree.column("events", width=200, minwidth=200)
tree.column("3_grade", width=200, minwidth=200)
tree.column("2G_grade", width=200, minwidth=200)
tree.column("2I_grade", width=200, minwidth=200)
tree.column("1_grade", width=200, minwidth=200)

# Define headings
tree.heading("#0", text="Date")
tree.heading("events", text="Events")
tree.heading("3_grade", text="3 Grade")
tree.heading("2G_grade", text="2G Grade")
tree.heading("2I_grade", text="2I Grade")
tree.heading("1_grade", text="1 Grade")

# Populate the treeview with data
for month, days in data.items():
    for day, details in days.items():
        date = f"{month}/{day}"
        events = ", ".join(details.get("events", []))
        grade_3 = ", ".join(details.get("3_grade", []))
        grade_2G = ", ".join(details.get("2G_grade", []))
        grade_2I = ", ".join(details.get("2I_grade", []))
        grade_1 = ", ".join(details.get("1_grade", []))
        tree.insert("", "end", text=date, values=(events, grade_3, grade_2G, grade_2I, grade_1))

# Run the application
root.mainloop()