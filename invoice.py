import sqlite3
import tkinter
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# [ FUNCTION TO OPEN CREATE INVOICE FORM ]
def createinvoice():
    window.withdraw()
    os.system("python createinvoice.py")
    window.deiconify()

# =========================================================================

# root window
window = Tk()
window.geometry("1366x768")
window.title("M&J Invoicing")

# [ PAGE CONTENT ]
frame = tkinter.Frame(window) # setting frame to be contained inside window
frame.pack(expand=True)

# [ BUTTON TO OPEN CREATE INVOICE FORM ]
createnewinvoice_btn = tkinter.Button(frame, text="Create New Invoice", command=createinvoice, bg="#a0d88a")
createnewinvoice_btn.grid(row=0, column=0, sticky = "NEWS", padx=20, pady=20)

# [ VIEW ALL INVOICES CURRENTLY IN DATABASE SECTION ]
invoice_list_frame = tkinter.LabelFrame(frame, text="All Invoices", padx=20, pady=20)
invoice_list_frame.grid(row=1, column=0)

invoice_id_label = tkinter.Label(invoice_list_frame, text="ID", bg="#cecece")
invoice_id_label.grid(row=0, column=0, sticky = "NEWS")
date_label = tkinter.Label(invoice_list_frame, text="Date", bg="#cecece")
date_label.grid(row=0, column=1, sticky = "NEWS")
fname_label = tkinter.Label(invoice_list_frame, text="First Name", bg="#cecece")
fname_label.grid(row=0, column=2, sticky = "NEWS")
lname_label = tkinter.Label(invoice_list_frame, text="Last Name", bg="#cecece")
lname_label.grid(row=0, column=3, sticky = "NEWS")
company_label = tkinter.Label(invoice_list_frame, text="Company", bg="#cecece")
company_label.grid(row=0, column=4, sticky = "NEWS")
desc_label = tkinter.Label(invoice_list_frame, text="Description", bg="#cecece")
desc_label.grid(row=0, column=5, sticky = "NEWS")
amt_label = tkinter.Label(invoice_list_frame, text="Amount", bg="#cecece")
amt_label.grid(row=0, column=6, sticky = "NEWS")

# connect to db
conn = sqlite3.connect("./databases/invoices.db")
with conn:
    cursor = conn.cursor()

# retrieve all rows from db
query_results = cursor.execute('''SELECT
                                    invoice_id,
                                    date,
                                    first_name,
                                    last_name,
                                    company,
                                    description,
                                    amount
                                   FROM invoices''')

# for each loops to set up table displaying information
i = 1
for invoice in query_results: # for each invoice returned by the query
    for j in range(len(invoice)): # for each field in the column
        field = tkinter.Label(invoice_list_frame, text=invoice[j], bg="white") # invoice[j] = the field within the row
        field.grid(row=i, column=j, pady=5, sticky="NEWS")
    i+=1
# ==========================================================================

window.mainloop()