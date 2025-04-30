import tkinter as tk #import ui
from tkinter import messagebox
import random
#got it from google
logged_in_user = None
accounts = {}
#create new function
def main():
    root = tk.Tk() #creates main window
    root.title("Banking System")   #title screen


    tk.Label(root, text="Welcome to the Banking System", font=("Arial", 16)).pack(pady=10) # title screen displays various options
    tk.Button(root, text="Create Account", command=create_account).pack(pady=5)
    tk.Button(root, text="Login", command=login).pack(pady=5)


    root.mainloop()
#loop the function
def create_account():      #Creating an account function
    win = tk.Toplevel()    # creates a new window
    win.title("Create Account")


    tk.Label(win, text="Name:").grid(row=0, column=0)  #label name
    name_entry = tk.Entry(win)   #create rows and columns for user to inpt account name
    name_entry.grid(row=0, column=1)


    tk.Label(win, text="PIN:").grid(row=1, column=0)  #rows and columns for user to input Pin
    pin_entry = tk.Entry(win, show="*")
    pin_entry.grid(row=1, column=1)


    def submit():   #runs when the reader creates an account and stores information
        name = name_entry.get()
        pin = pin_entry.get()
        if name and pin:
            acc_num = f"ACC{random.randint(1000,9999)}"
            accounts[acc_num] = {"name": name, "pin": pin, "balance": 0}
            messagebox.showinfo("Success", f"Account created! Number: {acc_num}")
            win.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")


    tk.Button(win, text="Create", command=submit).grid(row=2, columnspan=2, pady=10)


def login():
    win = tk.Toplevel()
    win.title("Login")


    tk.Label(win, text="Account Number:").grid(row=0, column=0)
    acc_entry = tk.Entry(win)
    acc_entry.grid(row=0, column=1)


    tk.Label(win, text="PIN:").grid(row=1, column=0)
    pin_entry = tk.Entry(win, show="*")
    pin_entry.grid(row=1, column=1)


    def submit():
        acc = acc_entry.get()
        pin = pin_entry.get()
        if acc in accounts and accounts[acc]["pin"] == pin:
            global logged_in_user
            logged_in_user = acc
            messagebox.showinfo("Welcome", f"Logged in as {acc}")
            win.destroy()
            show_menu()
        else:
            messagebox.showerror("Error", "Invalid account or PIN.")


    tk.Button(win, text="Login", command=submit).grid(row=2, columnspan=2, pady=10)


def show_menu():
    if not logged_in_user:
        messagebox.showerror("Error", "Please login first.")
        return


    win = tk.Toplevel()
    win.title("Main Menu")


    tk.Label(win, text=f"Account: {logged_in_user}", font=("Arial", 12)).grid(row=0, columnspan=2, pady=10)


    def deposit():
        accounts[logged_in_user]["balance"] += 10  # Just add fixed amount for simplicity
        messagebox.showinfo("Deposited", "Added $10.")


    def withdraw():  #withdraw money
        if accounts[logged_in_user]["balance"] >= 10:
            accounts[logged_in_user]["balance"] -= 10
            messagebox.showinfo("Withdrawn", "Removed $10.")
        else:
            messagebox.showerror("Error", "Not enough balance.")


    def check_balance():  #check how much money you have
        bal = accounts[logged_in_user]["balance"]
        messagebox.showinfo("Balance", f"Your balance is ${bal}")


    def logout():  #logout of account
        global logged_in_user
        logged_in_user = None
        win.destroy()


    tk.Button(win, text="Deposit", command=deposit).grid(row=1, column=0, pady=5)
    tk.Button(win, text="Withdraw", command=withdraw).grid(row=1, column=1, pady=5)
    tk.Button(win, text="Check Balance", command=check_balance).grid(row=2, column=0, pady=5)
    tk.Button(win, text="Logout", command=logout).grid(row=2, column=1, pady=5)


if __name__ == "__main__":
    main()


