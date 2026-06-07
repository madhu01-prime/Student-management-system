import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

FILE_NAME = "students.xlsx"

def load_data():
    for item in tree.get_children():
        tree.delete(item)

    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

def save_dataframe(df):
    df.to_excel(FILE_NAME, index=False)

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

def add_student():
    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    dept = dept_entry.get().strip()
    age = age_entry.get().strip()

    if not all([name, roll, dept, age]):
        messagebox.showerror("Error", "Fill all fields")
        return

    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
    else:
        df = pd.DataFrame(columns=["Name", "Roll No", "Department", "Age"])

    if roll in df["Roll No"].astype(str).values:
        messagebox.showerror("Error", "Roll No already exists")
        return

    df.loc[len(df)] = [name, roll, dept, age]
    save_dataframe(df)
    load_data()
    clear_fields()
    messagebox.showinfo("Success", "Student Added")

def select_record(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    clear_fields()
    name_entry.insert(0, values[0])
    roll_entry.insert(0, values[1])
    dept_entry.insert(0, values[2])
    age_entry.insert(0, values[3])

def update_student():
    roll = roll_entry.get().strip()

    if not os.path.exists(FILE_NAME):
        return

    df = pd.read_excel(FILE_NAME, dtype=str)

    mask = df["Roll No"].astype(str) == str(roll)

    if not mask.any():
        messagebox.showerror("Error", "Student not found")
        return

    df.loc[mask, "Name"] = str(name_entry.get().strip())
    df.loc[mask, "Department"] = str(dept_entry.get().strip())
    df.loc[mask, "Age"] = str(age_entry.get().strip())

    df.to_excel(FILE_NAME, index=False)

    load_data()
    clear_fields()

    messagebox.showinfo("Success", "Student Updated")
def delete_student():
    roll = roll_entry.get().strip()

    if not os.path.exists(FILE_NAME):
        return

    df = pd.read_excel(FILE_NAME)

    df = df[df["Roll No"].astype(str) != roll]

    save_dataframe(df)
    load_data()
    clear_fields()
    messagebox.showinfo("Success", "Student Deleted")

def search_student():
    roll = roll_entry.get().strip()

    for item in tree.get_children():
        tree.selection_remove(item)

    for item in tree.get_children():
        values = tree.item(item, "values")
        if str(values[1]) == roll:
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            return

    messagebox.showinfo("Search", "Student Not Found")

root = tk.Tk()
root.title("Student Management System V2")
root.geometry("900x600")

title = tk.Label(root, text="Student Management System", font=("Arial", 18, "bold"))
title.pack(pady=10)

form = tk.Frame(root)
form.pack(pady=10)

tk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form, width=30)
name_entry.grid(row=0, column=1)

tk.Label(form, text="Roll No").grid(row=1, column=0, padx=5, pady=5)
roll_entry = tk.Entry(form, width=30)
roll_entry.grid(row=1, column=1)

tk.Label(form, text="Department").grid(row=2, column=0, padx=5, pady=5)
dept_entry = tk.Entry(form, width=30)
dept_entry.grid(row=2, column=1)

tk.Label(form, text="Age").grid(row=3, column=0, padx=5, pady=5)
age_entry = tk.Entry(form, width=30)
age_entry.grid(row=3, column=1)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=12, command=add_student).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", width=12, command=update_student).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_student).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Search", width=12, command=search_student).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Clear", width=12, command=clear_fields).grid(row=0, column=4, padx=5)

columns = ("Name", "Roll No", "Department", "Age")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", select_record)

load_data()

root.mainloop()
