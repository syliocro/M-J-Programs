import sqlite3
import tkinter
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkdocviewer import *

# connect to db
conn = sqlite3.connect("./databases/invoices.db")
with conn:
    cursor = conn.cursor()

# [ FUNCTIONS ]

# opens create invoice window with form
def createinvoice():
    window.withdraw()
    os.system("python createinvoice.py")
    window.deiconify()

# brings up search results
def search(input):
    has_a_match = False
    query_length = 0

    query_results = cursor.execute(f"""
                                    SELECT * FROM invoices
                                    WHERE 
                                        invoice_id LIKE '%{input}%' OR
                                        first_name LIKE '%{input}%' OR
                                        last_name LIKE '%{input}%' OR
                                        date LIKE '%{input}%' OR
                                        company LIKE '%{input}%'
                                    """)

    # counting how many results came up
    for result in query_results:
        query_length+= 1

    if query_length > 0:
        has_a_match = True

    # the search has a match
    if (has_a_match): 
        all_invoices_frame.grid_forget()
        search_results_frame = tkinter.Frame(invoice_list_frame)
        search_results_frame.grid(row=0, column=0, sticky="N")
        search_results_frame.tkraise()

        # row headers
        invoice_id_label = tkinter.Label(search_results_frame, text="ID", bg="#cecece")
        invoice_id_label.grid(row=0, column=0, sticky = "NEWS")
        date_label = tkinter.Label(search_results_frame, text="Date", bg="#cecece")
        date_label.grid(row=0, column=1, sticky = "NEWS")
        fname_label = tkinter.Label(search_results_frame, text="First Name", bg="#cecece")
        fname_label.grid(row=0, column=2, sticky = "NEWS")
        lname_label = tkinter.Label(search_results_frame, text="Last Name", bg="#cecece")
        lname_label.grid(row=0, column=3, sticky = "NEWS")
        company_label = tkinter.Label(search_results_frame, text="Company", bg="#cecece")
        company_label.grid(row=0, column=4, sticky = "NEWS")
        desc_label = tkinter.Label(search_results_frame, text="Description", bg="#cecece")
        desc_label.grid(row=0, column=5, sticky = "NEWS")
        amt_label = tkinter.Label(search_results_frame, text="Amount", bg="#cecece")
        amt_label.grid(row=0, column=6, sticky = "NEWS")

        field = tkinter.Label(search_results_frame, text="to fix", bg="white")
        field.grid(row=1, column=0, pady=5, sticky="NEWS")
        # search results display logic
        # for each loops to set up table displaying information
        #i = 1
        #for invoice in query_results: # for each invoice returned by the query
        #    for j in range(len(invoice)): # for each field in the column
        #        field = tkinter.Label(search_results_frame, text=invoice[j], bg="white") # invoice[j] = the field within the row
        #        field.grid(row=i, column=j, pady=5, sticky="NEWS")
        #    # [ VIEW BUTTON TO EACH ROW ]
        #    file_path = "invoices/" + str(invoice[0]) + "_" + str(invoice[2]) + "_" + str(invoice[3]) + "_" + str(invoice[1]) + ".pdf"
        #    view_btn = tkinter.Button(search_results_frame, text="View", pady=5, command=lambda invoice=invoice:view_pdf(invoice), bg="#a0d88a")
        #    view_btn.grid(row=i, column=7)
        #    i+=1
    # search has no match
    else:
        tkinter.messagebox.showwarning(title="Error: No Results Found", message=f"There are no matching search results for '{input}'.")

# get pdf view in GUI
def view_pdf(invoice):
    id = str(invoice[0])
    first_name = invoice[2]
    last_name = invoice[3]
    date = invoice[1]
    path = "invoices/" + id + "_" + first_name + "_" + last_name + "_" + date + ".pdf"
    v = DocViewer(pdf_frame)
    v.grid(row=0, column=0, sticky="NEWS")
    return v.display_file(f"{path}")

# edits invoice information
def edit_invoice(invoice):
    id = str(invoice[0])
    get_query = f"""SELECT * FROM invoices WHERE invoice_id = {id}"""
    query_results = cursor.execute(get_query)
    
    edit_frame = tkinter.Frame(frame)
    edit_frame.grid(row=3, column=0)
    edit_frame.tkraise()

    # ------------- testing, put button at end tat submits new inputs, follow with rest ---
    # [ LABELS ]
    date_label = tkinter.Label(edit_frame, text="Date (MM-DD-YYYY)")
    date_label.grid(row=1, column=0)

    # [ INPUT FIELDS ]
    date_entry = tkinter.Entry(edit_frame)
    date_entry.insert(0, f"{invoice[1]}")
    date_entry.grid(row=1, column=1)

    # re-sizing the elements
    for widget in edit_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # user can see all fields pre-filled out from grabbing data and can erase and type new (can't change invoice id number)
    # gets the new inputs from user on what to update
    # selects invoice to update
    # sql query update set where id is equal to num
    #----------------------------------------------------------------------------
    return 0

# deletes invoice from database
def delete_invoice(invoice):
    id = invoice[0]
    delete_query = f"""DELETE FROM invoices WHERE invoice_id = {id}"""
    cursor.execute(delete_query)
    cursor.execute("COMMIT")
    tkinter.messagebox.showinfo(title="Success", message="Invoice successfully deleted. Please Refresh to see changes.")

# refreshes invoice list
def get_invoice_list():
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

    all_invoices_frame = tkinter.Frame(invoice_list_frame)
    all_invoices_frame.grid(row=0, column=0, sticky="N")
    #all_invoices_frame.tkraise()

    # row headers
    invoice_id_label = tkinter.Label(all_invoices_frame, text="ID", bg="#cecece")
    invoice_id_label.grid(row=0, column=0, sticky = "NEWS")
    date_label = tkinter.Label(all_invoices_frame, text="Date", bg="#cecece")
    date_label.grid(row=0, column=1, sticky = "NEWS")
    fname_label = tkinter.Label(all_invoices_frame, text="First Name", bg="#cecece")
    fname_label.grid(row=0, column=2, sticky = "NEWS")
    lname_label = tkinter.Label(all_invoices_frame, text="Last Name", bg="#cecece")
    lname_label.grid(row=0, column=3, sticky = "NEWS")
    company_label = tkinter.Label(all_invoices_frame, text="Company", bg="#cecece")
    company_label.grid(row=0, column=4, sticky = "NEWS")
    desc_label = tkinter.Label(all_invoices_frame, text="Description", bg="#cecece")
    desc_label.grid(row=0, column=5, sticky = "NEWS")
    amt_label = tkinter.Label(all_invoices_frame, text="Amount", bg="#cecece")
    amt_label.grid(row=0, column=6, sticky = "NEWS")

    # for each loops to set up table displaying information
    i = 1
    for invoice in query_results: # for each invoice returned by the query
        for j in range(len(invoice)): # for each field in the column
            field = tkinter.Label(all_invoices_frame, text=invoice[j], bg="white") # invoice[j] = the field within the row
            field.grid(row=i, column=j, pady=5, sticky="NEWS")
        # [ VIEW BUTTON TO EACH ROW ]
        file_path = "invoices/" + str(invoice[0]) + "_" + str(invoice[2]) + "_" + str(invoice[3]) + "_" + str(invoice[1]) + ".pdf"
        view_btn = tkinter.Button(all_invoices_frame, text="View", command=lambda invoice=invoice:view_pdf(invoice), bg="#a0d88a")
        view_btn.grid(row=i, column=7)
        # [ EDIT BUTTON TO EACH ROW ]
        edit_btn = tkinter.Button(all_invoices_frame, text="Edit", command=lambda invoice=invoice:edit_invoice(invoice), bg="#e2e99c")
        edit_btn.grid(row=i, column=8)
        # [ DELETE BUTTON TO EACH ROW ]
        delete_btn = tkinter.Button(all_invoices_frame, text="X", command=lambda invoice=invoice:delete_invoice(invoice), bg="#e99c9c")
        delete_btn.grid(row=i, column=9)
        i+=1

# =========================================================================

# root window
window = Tk()
window.geometry("1366x768")
window.title("M&J Invoicing")

# [ PAGE CONTENT ]
frame = tkinter.Frame(window) # setting frame to be contained inside window
frame.pack(expand=True)

# [ SEARCH BUTTON ]
search_frame = tkinter.Frame(frame)
search_frame.grid(row=0, column=0)

search_entry = tkinter.Entry(search_frame)
search_entry.grid(row=0, column=0, padx=20, pady=20)

search_btn = tkinter.Button(search_frame, text="Search", command=lambda:search(search_entry.get()), bg="#a0d88a")
search_btn.grid(row=0, column=1)

# [ BUTTON TO REFRESH INVOICE LIST ]
refresh_btn = tkinter.Button(search_frame, text="Show All/Refresh", command=get_invoice_list, bg="#a0d88a")
refresh_btn.grid(row=0, column=2, padx=20, pady=20)

# [ BUTTON TO OPEN CREATE INVOICE FORM ]
createnewinvoice_btn = tkinter.Button(frame, text="Create New Invoice", command=createinvoice, bg="#a0d88a")
createnewinvoice_btn.grid(row=0, column=1, sticky = "NEWS", padx=20, pady=20)

# [ VIEW ALL INVOICES CURRENTLY IN DATABASE SECTION ]
invoice_list_frame = tkinter.LabelFrame(frame, text="Invoices", padx=20, pady=20)
invoice_list_frame.grid(row=1, column=0)

#all_invoices_frame = tkinter.Frame(invoice_list_frame)
#all_invoices_frame.grid(row=0, column=0)

#get_invoice_list()

# [ PDF PREVIEW SECTION ]
pdf_frame = tkinter.Frame(frame, width=300, height=600)
pdf_frame.grid(row=1, column=1)

#v = DocViewer(pdf_frame)
#v.grid(row=0, column=0)
#v.display_file("invoices/invoice_1.pdf")


# ==========================================================================

window.mainloop()