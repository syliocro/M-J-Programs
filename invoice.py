import sqlite3
import tkinter
import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkdocviewer import *
from tempfile import NamedTemporaryFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# root window
window = Tk()
window.geometry("1366x768")
window.title("M&J Invoicing")

# connect to db
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

# [ FUNCTIONS ]

# validates input of entered data when creating a new invoice
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

# returns a tuple of the current data selected
def get_selected_data():
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

    data_tuple = (invoice_id, first_name, last_name, date, company, street, city, state, zip, description, amount)

    return data_tuple

# enters the form data into db after submit is pressed + generates pdf
def enter_data():
    data_insert_tuple = get_selected_data()

    # checking data
    is_correct_input = validate(data_insert_tuple)

    if (is_correct_input):
        # insert data
        try:
            # send data to db
            data_insert_query = '''INSERT INTO invoices (invoice_id, first_name, last_name, date, company, street, city, state, zip, description, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit() # save changes to database

            # generate pdf
            create_pdf(data_insert_tuple)
            tkinter.messagebox.showinfo(title="Success", message="Invoice successfully added.")
            clear()
        # alerts user if invoice_id already exists
        except sqlite3.IntegrityError:
            tkinter.messagebox.showwarning(title="Error: Existing Entry", message="An invoice with this Invoice ID already exists.")

# generates pdf based on values given
def create_pdf(values):
    # getting variables to use
    invoice_id = values[0]
    first_name = values[1]
    last_name = values[2]
    date = values[3]
    company = values[4]
    street = values[5]
    city = values[6]
    state = values[7]
    zip = values[8]
    description = values[9]
    amount = values[10]

    # setting up where to save pdf
    # invoiceid_firstname_lastname_date
    filename = str(invoice_id) + "_" + str(first_name) + "_" + str(last_name) + "_" + str(date)
    c = canvas.Canvas(f"invoices/{filename}.pdf", pagesize=letter)
    c.setFont('Helvetica', 12)

    # company logo
    c.drawImage("mjlogo.png", 100, 600, width=128, height=85)

    # top right text
    c.setFillColor("gray")
    c.drawString(400, 660, 'Invoice #:')
    c.setFillColor("black")
    c.drawString(460, 660, f'{invoice_id}')

    c.setFillColor("gray")
    c.drawString(423, 640, 'Date:')
    c.setFillColor("black")
    c.drawString(460, 640, f'{date}')

    # company information
    c.drawString(100, 550, 'M&J Loudoun LLC')
    c.drawString(100, 530, '7 Loudoun St SW')
    c.drawString(100, 510, 'Leesburg, VA 20175')
    c.drawString(100, 490, '(703) 669-6400')

    # customer information
    c.setFillColor("black")
    c.drawString(400, 550, f'{company}')
    c.drawString(400, 530, f'{first_name} {last_name}')
    c.drawString(400, 510, f'{street}')
    c.drawString(400, 490, f'{city}, {state} {zip}')

    # table headers
    c.setFillColor("gray")
    c.drawString(100, 440, 'DESCRIPTION')
    c.drawString(280, 440, 'AMOUNT')
    c.drawString(420, 440, 'SUBTOTAL')

    # add line
    c.setStrokeColor('gray')
    c.setLineWidth(.3)
    # (x1,y1, x2,y2)
    c.line(100, 430, 500, 430)

    # billing items
    c.setFillColor("black")
    c.drawString(100, 410, f'{description}')
    c.drawString(280, 410, f'${amount}')
    c.setFillColor("red")
    c.drawString(420, 410, f'${amount}')


    # total due section
    c.setFont('Helvetica', 15)
    c.setFillColor("gray")
    c.drawString(325, 100, 'TOTAL DUE:')
    c.setFillColor("red")
    c.drawString(425, 100, f'${amount}')

    c.showPage() # writes to canvas
    c.save() # saves file and closes canvas


# opens the invoice pdf in another window
def view_pdf():
    id = invoice_id_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    date = date_entry.get()

    path = "invoices/" + id + "_" + first_name + "_" + last_name + "_" + date + ".pdf"
    isExist = os.path.exists(path)

    # check if empty entry boxes to prevent empty pdf generation
    isEmpty = False
    for var in get_selected_data():
        if len(var) == 0:
            isEmpty = True

    # checks if file exists, if not then it makes one for you after a prompt
    if isEmpty:
        tkinter.messagebox.showwarning(title="Error: Empty Entry", message="Select an invoice first to view its PDF.")
    elif isExist:
        newWindow = Toplevel(window)
        newWindow.title("Invoice PDF")
        newWindow.geometry("612x792")

        v = DocViewer(newWindow)
        v.pack(expand=True, fill="both")
        return v.display_file(f'{path}')
    else:
        if messagebox.askyesno("Missing PDF", "A PDF does not exist for this invoice. Create one?"):
            create_pdf(get_selected_data())
            tkinter.messagebox.showinfo(title="Success", message="PDF successfully created.")
            view_pdf()
        else:
            return 0

# clears current text in entry boxes
def clear_entry():
    invoice_id_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    description_entry.delete(0, 'end')
    amount_entry.delete(0, 'end')
    first_name_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    company_entry.delete(0, 'end')
    state_combobox.delete(0, 'end')
    street_entry.delete(0, 'end')
    city_entry.delete(0, 'end')
    zip_entry.delete(0, 'end')

# =========================================================================

# [ PAGE CONTENT ]
frame = tkinter.Frame(window) # setting frame to be contained inside window
frame.pack(expand=True)

# [ NAVIGATION SECTION ] --------------------------------------------
# text entry + button to search
search_frame = tkinter.Frame(frame)
search_frame.pack(ipadx=20, ipady=20, anchor=N, expand=TRUE)

search_entry = tkinter.Entry(search_frame)
search_entry.pack(ipadx=30, padx=10, pady=20, side=LEFT)

search_btn = tkinter.Button(search_frame, text="Search", command=lambda:search(search_entry.get()), bg="#a0d88a")
search_btn.pack(padx=10, pady=20, side=LEFT)

# button to show all invoices
showall_btn = tkinter.Button(search_frame, text="Show All", command=lambda:display_data(), bg="#a0d88a")
showall_btn.pack(padx=10, pady=20, side=LEFT)

# button to open cost estimation calculator
calculator_btn = tkinter.Button(search_frame, text="Cost Estimation Calculator", command="", bg="#a0d88a")
calculator_btn.pack(padx=10, pady=20, side=RIGHT)

# [ VIEW ALL INVOICES CURRENTLY IN DATABASE SECTION ] -------------------------
invoice_list_frame = tkinter.LabelFrame(frame, text="Invoices", padx=20, pady=20)
invoice_list_frame.pack(padx=20, pady=20, fill=BOTH, side=LEFT, expand=TRUE)

# [ INVOICE DATA SECTION ] ------------------------------------
invoice_data_frame = tkinter.LabelFrame(frame, text="Invoice Data", padx=20, pady=20)
invoice_data_frame.pack(padx=20, pady=20, fill=BOTH, side=RIGHT, expand=TRUE)

# clear button
clear_btn_frame = tkinter.Frame(invoice_data_frame)
clear_btn_frame.grid(row=0, column=0)
# button to clear current entry boxes
clear_btn = tkinter.Button(clear_btn_frame, text="Clear", command=lambda:clear_entry(), bg="#a0d88a")
clear_btn.grid(row=0, column=0)

# invoice information
invoice_info_frame = tkinter.LabelFrame(invoice_data_frame, text="Invoice Information")
invoice_info_frame.grid(row=1, column=0)

invoice_id_label = tkinter.Label(invoice_info_frame, text="Invoice ID")
invoice_id_label.grid(row=0, column=0)
invoice_id_entry = tkinter.Entry(invoice_info_frame)
invoice_id_entry.grid(row=0, column=1)

date_label = tkinter.Label(invoice_info_frame, text="Date (MM-DD-YYYY)")
date_label.grid(row=1, column=0)
date_entry = tkinter.Entry(invoice_info_frame)
date_entry.grid(row=1, column=1)

description_label = tkinter.Label(invoice_info_frame, text="Description")
description_label.grid(row=2, column=0)
description_entry = tkinter.Entry(invoice_info_frame)
description_entry.grid(row=2, column=1)

amount_label = tkinter.Label(invoice_info_frame, text="Amount")
amount_label.grid(row=3, column=0)
amount_entry = tkinter.Entry(invoice_info_frame)
amount_entry.grid(row=3, column=1)

# customer information
customer_info_frame = tkinter.LabelFrame(invoice_data_frame, text="Customer Information")
customer_info_frame.grid(row=2, column=0)

first_name_label = tkinter.Label(customer_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
first_name_entry = tkinter.Entry(customer_info_frame)
first_name_entry.grid(row=0, column=1)

last_name_label = tkinter.Label(customer_info_frame, text="Last Name")
last_name_label.grid(row=1, column=0)
last_name_entry = tkinter.Entry(customer_info_frame)
last_name_entry.grid(row=1, column=1)

company_label = tkinter.Label(customer_info_frame, text="Company")
company_label.grid(row=2, column=0)
company_entry = tkinter.Entry(customer_info_frame)
company_entry.grid(row=2, column=1)

street_label = tkinter.Label(customer_info_frame, text="Street Address")
street_label.grid(row=3, column=0)
street_entry = tkinter.Entry(customer_info_frame)
street_entry.grid(row=3, column=1)

city_label = tkinter.Label(customer_info_frame, text="City")
city_label.grid(row=4, column=0)
city_entry = tkinter.Entry(customer_info_frame)
city_entry.grid(row=4, column=1)

state_label = tkinter.Label(customer_info_frame, text="State")
state_combobox = ttk.Combobox(customer_info_frame, values=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TX","UT","VT","VA","WA","WV","WI","WY"])
state_label.grid(row=5, column=0)
state_combobox.grid(row=5, column=1)

zip_label = tkinter.Label(customer_info_frame, text="ZIP Code")
zip_label.grid(row=6, column=0)
zip_entry = tkinter.Entry(customer_info_frame)
zip_entry.grid(row=6, column=1)

# buttons
invoice_buttons_frame = tkinter.Frame(invoice_data_frame)
invoice_buttons_frame.grid(row=3, column=0)

# button to view invoice as pdf
view_invoice_pdf_btn = tkinter.Button(invoice_buttons_frame, text="View PDF", command=lambda:view_pdf(), bg="#a0d88a")
view_invoice_pdf_btn.grid(row=0, column=0)

# button to create invoice form
createnewinvoice_btn = tkinter.Button(invoice_buttons_frame, text="Create", command=lambda:enter_data(), bg="#a0d88a")
createnewinvoice_btn.grid(row=0, column=1)

# button to update invoice
update_invoice_btn = tkinter.Button(invoice_buttons_frame, text="Update", command=lambda:update_invoice(), bg="#e9e29c")
update_invoice_btn.grid(row=0, column=2)

# button to delete invoice
delete_invoice_btn = tkinter.Button(invoice_buttons_frame, text="Delete", command=lambda:delete_invoice(), bg="#e99c9c")
delete_invoice_btn.grid(row=0, column=3)


# re-sizing the elements
for widget in invoice_data_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
for widget in customer_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
for widget in invoice_buttons_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)


# [ SET UP INVOICES TABLE TO DISPLAY ]

# define columns to choose from
columns = ('invoice_id', 'date', 'first_name', 'last_name', 'company', 'description', 'amount')
col_headings = ('ID', 'Date', 'First Name', 'Last Name', 'Company', 'Description', 'Amount')

# create tree to display data
tree_invoices = ttk.Treeview(invoice_list_frame, selectmode="browse", columns=columns, show='headings')

for c in columns:
    # setting widths of all columns to be 100 wide
    tree_invoices.column(f"{c}", width=100)\
    # setting the column headers to be sortable by clicking on them
    tree_invoices.heading(c, text=col_headings[columns.index(c)], command=lambda _col=c: \
                     sort_column(tree_invoices, _col, False))

# define the headers
tree_invoices.heading('invoice_id', text='ID')
tree_invoices.heading('date', text='Date')
tree_invoices.heading('first_name', text='First Name')
tree_invoices.heading('last_name', text='Last Name')
tree_invoices.heading('company', text='Company')
tree_invoices.heading('description', text='Description')
tree_invoices.heading('amount', text='Amount')

tree_invoices.pack()

# [ TREE FUNCTIONS ]

# update rows (for search)
def update(rows):
    tree_invoices.delete(*tree_invoices.get_children())
    for i in rows:
        tree_invoices.insert('', 'end', values=i)

# refreshes list of rows
def clear():
    query = "SELECT invoice_id, date, first_name, last_name, company, description, amount FROM invoices"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

# displays list of all invoices
def display_data():
    tree_invoices.delete(*tree_invoices.get_children())
    query_results = cursor.execute('''SELECT
                                    invoice_id,
                                    date,
                                    first_name,
                                    last_name,
                                    company,
                                    description,
                                    amount
                                   FROM invoices''')
    for result in query_results:
        tree_invoices.insert('', 'end', values=result)

# sorts list based on column
def sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time clicked
    tv.heading(col, text=col_headings[columns.index(col)], command=lambda _col=col: \
                 sort_column(tv, _col, not reverse))

# search results
def search(txt):
    query = f"""SELECT
                    invoice_id,
                    date,
                    first_name,
                    last_name,
                    company,
                    description,
                    amount
                FROM invoices
                WHERE 
                    invoice_id LIKE '%{txt}%' OR
                    first_name LIKE '%{txt}%' OR
                    last_name LIKE '%{txt}%' OR
                    date LIKE '%{txt}%' OR
                    company LIKE '%{txt}%'
                """
    cursor.execute(query)
    rows = cursor.fetchall()

    # counting how many results are returned
    query_length = 0
    for result in rows:
        query_length += 1

    if (query_length > 0):
        update(rows)
    else:
        tkinter.messagebox.showwarning(title="Error: No Results Found", message=f"There are no matching search results for '{txt}'.")

# selects row
def select_row():
    # clear entry boxes
    invoice_id_entry.delete(0, END)
    date_entry.delete(0, END)
    description_entry.delete(0, END)
    amount_entry.delete(0, END)
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    company_entry.delete(0, END)
    street_entry.delete(0, END)
    city_entry.delete(0, END)
    zip_entry.delete(0, END)
    state_combobox.delete(0, END)

    # get the record number
    selected = tree_invoices.focus()
    # get the record values
    values = tree_invoices.item(selected, 'values')
    # get the rest of the data from database based on invoice_id (which is values[0])
    query_results = cursor.execute(f"SELECT * FROM invoices WHERE invoice_id = {values[0]}")
    # store values of the results
    query_values = []
    for invoice in query_results: # for each invoice returned by the query
        for j in range(len(invoice)): # for each field in the column
            query_values.append(invoice[j])

    # ouput to entry boxes
    invoice_id_entry.insert(0, query_values[0])
    first_name_entry.insert(0, query_values[1])
    last_name_entry.insert(0, query_values[2])
    date_entry.insert(0, query_values[3])
    company_entry.insert(0, query_values[4])
    street_entry.insert(0, query_values[5])
    city_entry.insert(0, query_values[6])
    state_combobox.insert(0, query_values[7])
    zip_entry.insert(0, query_values[8])
    description_entry.insert(0, query_values[9])
    amount_entry.insert(0, query_values[10])

# binding click function (double click to select row)
def clicker(event):
    select_row()

# bindings
# double-1 is double click event, "when i double click, activate clicker function"
tree_invoices.bind("<Double-1>", clicker)

def delete_invoice():
    id = invoice_id_entry.get()
    if messagebox.askyesno("Confirm invoice deletion", "Are you sure you want to delete this invoice?"):
        cursor.execute(f"DELETE FROM invoices WHERE invoice_id = {id}")
        cursor.execute("COMMIT")
        tkinter.messagebox.showinfo(title="Success", message="Invoice successfully deleted.")
        print(id)
        clear()
    else:
        return 0

# updates invoice (invoice id won't update)
def update_invoice():
    id = invoice_id_entry.get()
    query = f"""UPDATE invoices
                SET
                    first_name = '{first_name_entry.get()}',
                    last_name = '{last_name_entry.get()}',
                    date = '{date_entry.get()}',
                    company = '{company_entry.get()}',
                    street = '{street_entry.get()}',
                    city = '{city_entry.get()}',
                    state = '{state_combobox.get()}',
                    zip = {zip_entry.get()},
                    description = '{description_entry.get()}',
                    amount = {amount_entry.get()}
                WHERE
                    invoice_id = {id}"""
    cursor.execute(query)
    # save changes to db
    cursor.execute("COMMIT;")

    # makes new pdf based off of new edit
    create_pdf(get_selected_data())

    tkinter.messagebox.showinfo(title="Success", message="Invoice successfully updated.")
    clear()

# display current database data
display_data()

# ==========================================================================

window.mainloop()