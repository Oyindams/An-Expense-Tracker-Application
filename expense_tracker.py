import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, Scrollbar
from PIL import Image, ImageTk
import csv
import os

FILENAME = "expenses.csv"
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x600")
expenses = []

def add_opacity(image, opacity):
    image = image.convert("RGBA")
    alpha = image.split()[3]
    alpha = alpha.point(lambda p: p * opacity)
    image.putalpha(alpha)
    return image

# To place McU logo
watermark_image = Image.open("The McPherson University logo.jpg")
watermark_image = watermark_image.resize((600, 600))  # For Resizing if necessary
watermark_image = add_opacity(watermark_image, opacity = 0.2)
watermark_photo = ImageTk.PhotoImage(watermark_image)


label_watermark = tk.Label(root, image=watermark_photo)
label_watermark.place(x=0, y=0, relwidth=1, relheight=1)





# For loading existing expenses from Csv file
def load_expenses():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                expenses.append({"description": row[0], "amount": float(row[1])})
            update_expense_list()

def update_expense_list():
    listbox_expenses.delete(0, tk.END)
    for expense in expenses:
        listbox_expenses.insert(tk.END, f"{expense['description']}: #{expense['amount']:.2f}")

def save_expenses():
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        for expense in expenses:
            writer.writerow([expense["description"], expense["amount"]])

def add_expense():
    description = entry_description.get().strip()
    amount_text = entry_amount.get().strip()

    if not description or not amount_text:
        messagebox.showerror("Input Error", "Please enter a description and an amount.")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for amount.")
        return

    expenses.append({"description": description, "amount": amount})
    update_expense_list()
    save_expenses()
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

def delete_expense():
    try:
        selected_index = listbox_expenses.curselection()[0]
        del expenses[selected_index]
        update_expense_list()
        save_expenses()
    except IndexError:
        messagebox.showerror("Delete Error", "Please select an expense to delete.")

def edit_expense():
    try:
        selected_index = listbox_expenses.curselection()[0]
        new_description = entry_description.get().strip()
        new_amount_text = entry_amount.get().strip()

        if not new_description or not new_amount_text:
            messagebox.showerror("Input Error", "Please enter a description and an amount.")
            return

        try:
            new_amount = float(new_amount_text)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for amount.")
            return

        expenses[selected_index] = {"description": new_description, "amount": new_amount}
        update_expense_list()
        save_expenses()
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
    except IndexError:
        messagebox.showerror("Edit Error", "Please select an expense to edit.")

def view_summary():
    total_amount = sum(expense["amount"] for expense in expenses)
    messagebox.showinfo("Summary", f"Total Expenses: ${total_amount:.2f}")

def view_creators():
    messagebox.showinfo("Creator Names", "Yakubu Goodness Olufunmilayo - 220202002\nAfolabi Oreoluwa Rachel - 220202035\nBabatunde Oyindamola Feranmi - 220202014\nJohn Esther Kumey - 220202025\nOnakorame Ejiro Esther - 220202015\nOlafioye Sikemi Grace - 220202032\nEkoko Taiwo - 220202038\nOjo Oluwadamilola Morenikeji - 220202020")

def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "Amount"])
            for expense in expenses:
                writer.writerow([expense["description"], expense["amount"]])
        messagebox.showinfo("Export", "Data exported successfully.")

def filter_expenses():
    threshold = simpledialog.askfloat("Filter", "Enter the least amount to filter expenses:")
    if threshold is not None:
        filtered_expenses = [expense for expense in expenses if expense["amount"] >= threshold]
        listbox_expenses.delete(0, tk.END)
        for expense in filtered_expenses:
            listbox_expenses.insert(tk.END, f"{expense['description']}: ${expense['amount']:.2f}")

def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                expenses.append({"description": row[0], "amount": float(row[1])})
        update_expense_list()
        save_expenses()
        messagebox.showinfo("Import", "Data imported successfully.")

def settings():
    messagebox.showinfo("Settings", "Settings not implemented yet.")

def view_charts():
    messagebox.showinfo("Charts", "Chart viewing not implemented yet.")

def backup_data():
    backup_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if backup_path:
        with open(backup_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "Amount"])
            for expense in expenses:
                writer.writerow([expense["description"], expense["amount"]])
        messagebox.showinfo("Backup", "Data backed up successfully.")

def restore_data():
    restore_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if restore_path:
        global expenses
        expenses = []
        with open(restore_path, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                expenses.append({"description": row[0], "amount": float(row[1])})
        update_expense_list()
        messagebox.showinfo("Restore", "Data restored successfully.")


frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Description").grid(row=0, column=0)
entry_description = tk.Entry(frame, width=20)
entry_description.grid(row=0, column=1)

tk.Label(frame, text="Amount").grid(row=1, column=0)
entry_amount = tk.Entry(frame, width=20)
entry_amount.grid(row=1, column=1)

# Add buttons
btn_add = tk.Button(frame, text="Add Expense", command=add_expense,)
btn_add.grid(row=2, columnspan=2, pady=5)


listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10)

listbox_expenses = tk.Listbox(listbox_frame, width=40, height=10)
listbox_expenses.pack(side=tk.LEFT)

scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_expenses.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_expenses.yview)

menu_frame = tk.Frame(root, bg="#F5F5F5", padx=20, pady=20)
menu_frame.pack(pady=20)

buttons = [
    ("View Summary", view_summary, "#4caf50"),
    ("Export Data", export_data, "#f44336"),
    ("Filter Expenses", filter_expenses, "#2196f3"),
    ("Import Data", import_data, "#9c27b0"),
    ("Settings", settings, "#009688"),
    ("Delete Expense", delete_expense, "#673ab7"),
    ("Edit Expense", edit_expense, "#3f51b5"),
    ("View Charts", view_charts, "#607d8b"),
    ("Backup Data", backup_data, "#795548"),
    ("Restore Data", restore_data, "#795548"),
    ("View Creators", view_creators, "#607d8b"),
]

for index, (text, command, color) in enumerate(buttons):
    button = tk.Button(menu_frame, text=text, command=command, bg=color, fg="white", font=("Arial", 10), width=20, pady=5)
    button.grid(row=index // 2, column=index % 2, padx=5, pady=5)

load_expenses()
root.mainloop()
