import sqlite3
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# [ INVOICE DB CONNECTION / INITIALIZATION ]
conn = sqlite3.connect("./databases/invoices.db")
with conn:
    cursor = conn.cursor()

# [ INVOICE TABLE ]
create_table_query = """CREATE TABLE IF NOT EXISTS invoices (
                            invoice_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            date DATE,
                            company TEXT,
                            street TEXT,
                            city TEXT,
                            state TEXT,
                            zip TEXT,
                            description TEXT,
                            amount REAL
                            )"""
cursor.execute(create_table_query)

# validates input
def validate(list):
    is_empty = False
    is_number = True
    is_date_correct = True
    is_zip_correct = True

    for var in list:
        # checking if variable is empty
        if len(var) == 0:
            is_empty = True
        # checking if numerical variables are numbers (invoice_id, zip, amount)
        elif (var == list[0] or var == list[8] or var == list[10]):
            try:
                val = float(var)
            except ValueError:
                is_number = False
        # checking if date entered correctly
        elif (var == list[3]):
            if (len(var) != 10):
                is_date_correct = False
            else:
                nums = [var[0], var[1], var[3], var[4], var[6], var[7], var[8], var[9]]
                dashes = [var[2], var[5]]
                for n in nums:
                    try:
                        val = int(n)
                    except ValueError:
                        is_date_correct = False
                for d in dashes:
                    if (d != '-'):
                        is_date_correct = False
        # checking if zip code entered correctly
        elif (var == list[8]):
            if (len(var) != 5):
                is_zip_correct = False

    if (is_empty):
        tkinter.messagebox.showwarning(title="Error: Missing Fields", message="Make sure all fields are filled out.")
    elif (is_number == False):
        tkinter.messagebox.showwarning(title="Error: Invalid Input", message="Make sure numerical fields (Invoice_ID, ZIP Code, and Amount) have number inputs.")
    elif (is_date_correct == False):
        tkinter.messagebox.showwarning(title="Error: Invalid Input", message="Make sure the date is in the correct format (DD-MM-YYYY).")
    elif (is_zip_correct == False):
        tkinter.messagebox.showwarning(title="Error: Invalid Input", message="Invalid ZIP code (Must be 5 numbers).")
    else:
        return True

# [ CREATE/STORE INVOICE ]
# enters the form data after submit is pressed
def enter_data():
    # invoice information
    invoice_id = invoice_id_entry.get()
    date = date_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    # customer information
    state = state_combobox.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    company = company_entry.get()
    street = street_entry.get()
    city = city_entry.get()
    zip = zip_entry.get()

    data_insert_tuple = (invoice_id, first_name, last_name, date, company, street, city, state, zip, description, amount)

    # checking data
    is_correct_input = validate(data_insert_tuple)

    if (is_correct_input):
        # insert data
        try:
            data_insert_query = '''INSERT INTO invoices (invoice_id, first_name, last_name, date, company, street, city, state, zip, description, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit() # save changes to database
            tkinter.messagebox.showinfo(title="Success", message="Invoice successfully added.")
        # alerts user if invoice_id already exists
        except sqlite3.IntegrityError:
            tkinter.messagebox.showwarning(title="Error: Existing Entry", message="An invoice with this Invoice ID already exists.")



# ==========================================================================
# [ TKINTER FORMATTING ]

# root window
window = Tk()
window.geometry("1366x768")
window.title("M&J Invoice Form")

# [ DATA ENTRY FORM ]
# frame is contained inside window
frame = tkinter.Frame(window)
frame.pack()

# [ INVOICE INFO SECTION ]
invoice_info_frame = tkinter.LabelFrame(frame, text="Invoice Information", padx=20, pady=20)
invoice_info_frame.grid(row=0, column=0)

# [ LABELS ]
invoice_id_label = tkinter.Label(invoice_info_frame, text="Invoice ID")
invoice_id_label.grid(row=0, column=0)

date_label = tkinter.Label(invoice_info_frame, text="Date (MM-DD-YYYY)")
date_label.grid(row=1, column=0)

description_label = tkinter.Label(invoice_info_frame, text="Description")
description_label.grid(row=2, column=0)

amount_label = tkinter.Label(invoice_info_frame, text="Amount")
amount_label.grid(row=3, column=0)

# [ INPUT FIELDS ]
invoice_id_entry = tkinter.Entry(invoice_info_frame)
invoice_id_entry.grid(row=0, column=1)

date_entry = tkinter.Entry(invoice_info_frame)
date_entry.grid(row=1, column=1)

description_entry = tkinter.Entry(invoice_info_frame)
description_entry.grid(row=2, column=1)

amount_entry = tkinter.Entry(invoice_info_frame)
amount_entry.grid(row=3, column=1)

# re-sizing the elements
for widget in invoice_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# --------------------------------------------------------------------------
# [ CUSTOMER INFO SECTION ]
customer_info_frame = tkinter.LabelFrame(frame, text="Customer Information", padx=20, pady=20)
customer_info_frame.grid(row=1, column=0)

# [ LABELS ]
first_name_label = tkinter.Label(customer_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)

last_name_label = tkinter.Label(customer_info_frame, text="Last Name")
last_name_label.grid(row=0, column=2)

company_label = tkinter.Label(customer_info_frame, text="Company")
company_label.grid(row=1, column=0)

street_label = tkinter.Label(customer_info_frame, text="Street Address")
street_label.grid(row=2, column=0)

city_label = tkinter.Label(customer_info_frame, text="City")
city_label.grid(row=3, column=0)

state_label = tkinter.Label(customer_info_frame, text="State")
state_combobox = ttk.Combobox(customer_info_frame, values=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TX","UT","VT","VA","WA","WV","WI","WY"])
state_label.grid(row=3, column=2)
state_combobox.grid(row=3, column=3)

zip_label = tkinter.Label(customer_info_frame, text="ZIP Code")
zip_label.grid(row=4, column=0)

# [ INPUT FIELDS ]
first_name_entry = tkinter.Entry(customer_info_frame)
first_name_entry.grid(row=0, column=1)

last_name_entry = tkinter.Entry(customer_info_frame)
last_name_entry.grid(row=0, column=3)

company_entry = tkinter.Entry(customer_info_frame)
company_entry.grid(row=1, column=1)

street_entry = tkinter.Entry(customer_info_frame)
street_entry.grid(row=2, column=1)

city_entry = tkinter.Entry(customer_info_frame)
city_entry.grid(row=3, column=1)

zip_entry = tkinter.Entry(customer_info_frame)
zip_entry.grid(row=4, column=1)

# re-sizing the elements
for widget in customer_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# [ SUBMIT BUTTON ]
submit_btn = tkinter.Button(frame, text="Submit", command=enter_data, bg="#a0d88a")
submit_btn.grid(row=4, column=0, sticky = "NEWS", padx=20, pady=20)

# ==========================================================================

window.mainloop()