import sqlite3
import tkinter
import os
import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkdocviewer import *
from tempfile import NamedTemporaryFile
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# root window
window = Tk()
window.geometry("1366x768")
window.title("M&J Invoicing")
window.configure(bg = "#0F1A20")
window.iconbitmap("mjlogo.ico")
window.option_add('*Font', '12')

# setting frame to be contained inside window
frame = tkinter.Frame(window) 
frame.pack(expand=True)

# background
canvasgui = Canvas(
    window,
    bg = "#0F1A20",
    height = 768,
    width = 1366,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvasgui.place(x = 0, y = 0)

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
    c.drawString(420, 440, 'AMOUNT')
    #c.drawString(280, 440, 'AMOUNT')
    #c.drawString(420, 440, 'SUBTOTAL')

    # add line
    c.setStrokeColor('gray')
    c.setLineWidth(.3)
    # (x1,y1, x2,y2)
    c.line(100, 430, 500, 430)

    # billing items
    c.setFillColor("black")
    c.drawString(100, 410, f'{description}')
    c.drawString(420, 410, f'${amount}')
    #c.drawString(280, 410, f'${amount}')
    #c.setFillColor("red")
    #c.drawString(420, 410, f'${amount}')


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

def open_calculator():
    #calculator_window = Toplevel(window)
    #calculator_window.title("Invoice PDF")
    #calculator_window.geometry("612x792")
    #os.system("python rentCalc.py")
    tkinter.messagebox.showinfo(title="Calculator", message="Calculator view will be added soon.")

# =========================================================================

# [ SET UP INVOICES TABLE TO DISPLAY ]

# define columns to choose from
columns = ('invoice_id', 'date', 'first_name', 'last_name', 'company', 'description', 'amount')
col_headings = ('ID', 'Date', 'First Name', 'Last Name', 'Company', 'Description', 'Amount')

# create tree to display data
tree_invoices = ttk.Treeview(canvasgui, selectmode="browse", columns=columns, show='headings', style="mystyle.Treeview")

# style the tree view
style = ttk.Style()
style.theme_use("clam")
style.configure("mystyle.Treeview", font=('Microsoft Sans Serif', 12))
style.configure("mystyle.Treeview.Heading", font=('Microsoft Sans Serif', 15,'bold'), background="#742438", foreground="white")
style.configure("mystyle.Treeview", rowheight=30)


for c in columns:
    # setting widths of all columns to be 100 wide
    tree_invoices.column(f"{c}", width=100)\
    # setting the column headers to be sortable by clicking on them
    tree_invoices.heading(c, text=col_headings[columns.index(c)], command=lambda _col=c: \
                     sort_column(tree_invoices, _col, False))

# define the headers
tree_invoices.heading('invoice_id', text='ID')
tree_invoices.column("invoice_id", width=25)
tree_invoices.heading('date', text='Date')
tree_invoices.heading('first_name', text='First Name')
tree_invoices.heading('last_name', text='Last Name')
tree_invoices.heading('company', text='Company')
tree_invoices.heading('description', text='Description')
tree_invoices.heading('amount', text='Amount')

# place on gui
tree_invoices.place(
    x=40,
    y=114,
    width=800,
    height=620
)

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
    invoice_id_entry.insert(0, query_values[0]) # 5
    first_name_entry.insert(0, query_values[1]) # Jessica
    last_name_entry.insert(0, query_values[2]) # Sampson
    date_entry.insert(0, query_values[3]) # 07-15-2022
    company_entry.insert(0, query_values[4]) # Today Inc
    street_entry.insert(0, query_values[5]) # 1806 Eva Pearl St
    city_entry.insert(0, query_values[6]) # Leesburg
    state_combobox.insert(0, query_values[7]) # VA
    zip_entry.insert(0, query_values[8]) # 20176
    description_entry.insert(0, query_values[9]) # monthly rent
    amount_entry.insert(0, query_values[10]) # 1500

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

# opens file explorer to where all the invoice pdfs are stored
def open_invoice_folder():
    os.startfile(r'invoices')

# display current database data
display_data()

# [ TKINTER GUI ] ===============================================================

# [ PAGE CONTENT ]

# search box
search_entry_img = PhotoImage(
    file="assets/search_entry.png")
entry_bg_1 = canvasgui.create_image(
    175.5,
    49.5,
    image=search_entry_img
)
search_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
search_entry.place(
    x=46.5,
    y=32.0,
    width=258.0,
    height=33.0
)

# search button
search_btn_img = PhotoImage(
    file="assets/search_btn.png")
search_btn = Button(
    image=search_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:search(search_entry.get()),
    relief="flat"
)
search_btn.place(
    x=342.0,
    y=32.0,
    width=131.0,
    height=35.0
)

# show all button
showall_btn_img = PhotoImage(
    file="assets/showall_btn.png")
showall_btn = Button(
    image=showall_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:display_data(),
    relief="flat"
)
showall_btn.place(
    x=493.0,
    y=32.0,
    width=150.0,
    height=35.0
)
# open invoice pdf folder button
invoice_folder_btn_img = PhotoImage(file="assets/openfolder.png")
invoice_folder_btn = Button(
    image = invoice_folder_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:open_invoice_folder(),
    relief="flat"
)
invoice_folder_btn.place(
    x=664.0,
    y=32.0,
    width=88.0,
    height=35.0
)

# calculator button
calculator_btn_img = PhotoImage(
    file="assets/calculator_btn.png")
calculator_btn = Button(
    image=calculator_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:open_calculator(),
    relief="flat"
)
calculator_btn.place(
    x=876.0,
    y=32.0,
    width=454.0,
    height=35.0
)

# white box
#canvas.create_rectangle(
#    17.0,
#    96.0,
#    1349.0,
#    753.0,
#    fill="#FFFFFF",
#    outline="")

# INVOICE INFO SECTION ----------------------------------

# gray box
canvasgui.create_rectangle(
    875.0,
    114.0,
    1330.0,
    735.0,
    fill="#ECECEC",
    outline="")

canvasgui.create_text(
    889.0,
    129.0,
    anchor="nw",
    text="Invoice Data",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 24 * -1)
)

# clear button
clear_btn_img = PhotoImage(
    file="assets/clear_btn.png")
clear_btn = Button(
    image=clear_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:clear_entry(),
    relief="flat"
)
clear_btn.place(
    x=1061.0,
    y=129.0,
    width=91.0,
    height=35.0
)

# view button
view_invoice_pdf_btn_img = PhotoImage(
    file="assets/viewpdf_btn.png")
view_invoice_pdf_btn = Button(
    image=view_invoice_pdf_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:view_pdf(),
    relief="flat"
)
view_invoice_pdf_btn.place(
    x=1168.0,
    y=129.0,
    width=141.0,
    height=35.0
)

# invoice ID
canvasgui.create_text(
    914.0,
    187.0,
    anchor="nw",
    text="Invoice ID",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)

invoice_id_entry_img = PhotoImage(
    file="assets/invoice_id_entry.png")
entry_bg_2 = canvasgui.create_image(
    1184.5,
    204.5,
    image=invoice_id_entry_img
)
invoice_id_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
invoice_id_entry.place(
    x=1097.5,
    y=187.0,
    width=174.0,
    height=33.0
)

# date
canvasgui.create_text(
    913.0,
    222.0,
    anchor="nw",
    text="Date",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
canvasgui.create_text(
    913, # 915
    245.0, # 235
    anchor="nw",
    text="(mm-dd-yyyy)",
    fill="#9F9F9F",
    font=("MicrosoftSansSerif", 14 * -1)
)

date_entry_img = PhotoImage(
    file="assets/date_entry.png")
entry_bg_3 = canvasgui.create_image(
    1184.5,
    286.5,
    image=date_entry_img
)
date_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
date_entry.place(
    x=1097.5,
    y=228.0,
    width=174.0,
    height=33.0
)

# description
canvasgui.create_text(
    914.0,
    269.0,
    anchor="nw",
    text="Description",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)

description_entry_img = PhotoImage(
    file="assets/description_entry.png")
entry_bg_4 = canvasgui.create_image(
    1186.5,
    391.5,
    image=description_entry_img
)
description_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
description_entry.place(
    x=1097.5,
    y=269.0,
    width=174.0,
    height=33.0
)


# amount
canvasgui.create_text(
    914.0,
    310.0,
    anchor="nw",
    text="Amount",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
amount_entry_img = PhotoImage(
    file="assets/amount_entry.png")
entry_bg_5 = canvasgui.create_image(
    1186.5,
    473.5,
    image=amount_entry_img
)
amount_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
amount_entry.place(
    x=1097.5,
    y=310.0,
    width=174.0,
    height=33.0
)

# first name
canvasgui.create_text(
    916.0,
    374.0,
    anchor="nw",
    text="First Name",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
first_name_entry_img = PhotoImage(
    file="assets/first_name_entry.png")
entry_bg_6 = canvasgui.create_image(
    1186.5,
    555.5,
    image=first_name_entry_img
)
first_name_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
first_name_entry.place(
    x=1099.5,
    y=374.0,
    width=174.0,
    height=33.0
)

# last name
canvasgui.create_text(
    916.0,
    415.0,
    anchor="nw",
    text="Last Name",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
last_name_entry_img = PhotoImage(
    file="assets/last_name_entry.png")
entry_bg_7 = canvasgui.create_image(
    1184.5,
    327.5,
    image=last_name_entry_img
)
last_name_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
last_name_entry.place(
    x=1099.5,
    y=415.0,
    width=174.0,
    height=33.0
)

# company
canvasgui.create_text(
    916.0,
    456.0,
    anchor="nw",
    text="Company",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
company_entry_img = PhotoImage(
    file="assets/company_entry.png")
entry_bg_8 = canvasgui.create_image(
    1186.5,
    432.5,
    image=company_entry_img
)
company_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
company_entry.place(
    x=1099.5,
    y=456.0,
    width=174.0,
    height=33.0
)

# street
canvasgui.create_text(
    916.0,
    497.0,
    anchor="nw",
    text="Street Address",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
street_entry_img = PhotoImage(
    file="assets/street_entry.png")
entry_bg_9 = canvasgui.create_image(
    1186.5,
    514.5,
    image=street_entry_img
)
street_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
street_entry.place(
    x=1099.5,
    y=497.0,
    width=174.0,
    height=33.0
)

# city
canvasgui.create_text(
    916.0,
    538.0,
    anchor="nw",
    text="City",
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
city_entry_img = PhotoImage(
    file="assets/city_entry.png")
entry_bg_10 = canvasgui.create_image(
    1186.5,
    596.5,
    image=city_entry_img
)
city_entry = Entry(
    bd=0,
    bg="white",
    highlightthickness=0
)
city_entry.place(
    x=1099.5,
    y=538.0,
    width=174.0,
    height=33.0
)

# state
canvasgui.create_text(
    916.0,
    579.0,
    anchor="nw",
    text="ZIP", #State
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)
state_entry_img = PhotoImage(
    file="assets/state_entry.png")
entry_bg_11 = canvasgui.create_image(
    1186.5,
    637.5,
    image=state_entry_img
)
state_combobox = ttk.Combobox(
    values=["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TX","UT","VT","VA","WA","WV","WI","WY"]#,
    #bd=0,
    #bg="#FFFFFF",
    #highlightthickness=0
)
state_combobox.place(
    x=1099.5,
    y=620.0,
    width=174.0,
    height=33.0
)

# zip
canvasgui.create_text(
    916.0,
    620.0,
    anchor="nw",
    text="State",  #ZIP
    fill="#0F1A20",
    font=("MicrosoftSansSerif", 20 * -1)
)

zip_entry_img = PhotoImage(
    file="assets/zip_entry.png")
entry_bg_12 = canvasgui.create_image(
    1184.5,
    245.5,
    image=zip_entry_img
)
zip_entry = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
zip_entry.place(
    x=1099.5,
    y=579.0,
    width=174.0,
    height=33.0
)

# create
createnewinvoice_btn_img = PhotoImage(
    file="assets/createnewinvoice_btn.png")
createnewinvoice_btn = Button(
    image=createnewinvoice_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:enter_data(),
    relief="flat"
)
createnewinvoice_btn.place(
    x=901.0,
    y=679.0,
    width=114.0,
    height=35.0
)

# update
update_invoice_btn_img = PhotoImage(
    file="assets/update_invoice_btn.png")
update_invoice_btn = Button(
    image=update_invoice_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:update_invoice(),
    relief="flat"
)
update_invoice_btn.place(
    x=1054.0,
    y=679.0,
    width=114.0,
    height=35.0
)

# delete
delete_invoice_btn_img = PhotoImage(
    file="assets/delete_invoice_btn.png")
delete_invoice_btn = Button(
    image=delete_invoice_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:delete_invoice(),
    relief="flat"
)
delete_invoice_btn.place(
    x=1202.0,
    y=679.0,
    width=114.0,
    height=35.0
)

# -------------------------------------------------------------------------
# ===============================================================================

window.mainloop()