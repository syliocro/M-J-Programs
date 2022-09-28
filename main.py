import os
from tkinter import *
from tkinter import messagebox

# --------------------------------------------------
# [ WINDOW SETUP ]
main = Tk()
main.geometry("1366x768")
main.title("M&J Invoicing / Calculations")
main.resizable(True,True) # allows window to change size

# exit confirmation window
def exit():
    msg = messagebox.askyesno("Quit", "Are you sure you want to exit?", parent=main)
    if (msg):
        main.destroy()

# deletes the window
main.protocol("WM_DELETE_WINDOW", exit)

# --------------------------------------------------
# [ FUNCTIONS TO OPEN INVOICING OR CALCULATOR ]

def invoice():
    main.withdraw() # removes window from screen without destroying it
    os.system("python invoice.py") # executes command (string) in a subshell
    main.deiconify() # displays the window after the withdraw method

def calculator():
    main.withdraw() # removes window from screen without destroying it
    os.system("python calculator.py") # executes command (string) in a subshell
    main.deiconify() # displays the window after the withdraw method

#----------------------------------------------------
# [ LABELS / BUTTONS ]

invoice_btn = Button(main, text="Invoices", command=invoice)
# positioning
invoice_btn.pack(side="top", fill="none", expand="True")
# button stylings
invoice_btn.configure(padx=100, pady=50)
invoice_btn.configure(relief="flat")
invoice_btn.configure(cursor="hand2")
invoice_btn.configure(bg="#ffffff")
invoice_btn.configure(borderwidth="0")

calculator_btn = Button(main, text="Calculator", command=calculator)
# positioning
calculator_btn.pack(side="top", fill="none", expand="True")
# button stylings
calculator_btn.configure(padx=100, pady=50)
calculator_btn.configure(relief="flat")
calculator_btn.configure(cursor="hand2")
calculator_btn.configure(bg="#ffffff")
calculator_btn.configure(borderwidth="0")

#----------------------------------------------------

main.mainloop()