
#Rent calc program
import tkinter
from  tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

dateValue = datetime.datetime.now()
dateDay =dateValue.strftime("%d")
dateMonth =dateValue.strftime("%m")
dateYear =dateValue.strftime("%Y")
finalDate=dateMonth+'-'+dateDay+'-'+dateYear

def calcRent():
	sqFootMoney=sqFootMoneyInput.get()
	sqFoot=sqFootInput.get()
	Utility=UtilityInput.get()
	company=companyInput.get()
	customer=customerInput.get()
	address=addressInput.get()
	city=cityInput.get()
	state=stateInput.get()
	zipNum=zipInput.get()
	invoice=invoiceInput.get()

	if sqFootMoney=="" or sqFoot=="" or Utility=="":
		tkinter.messagebox.showwarning(title="Empty Input", message="Enter values for all the input fields.")
	elif sqFootMoney.isnumeric()==False or sqFoot.isnumeric()==False or Utility.isnumeric()==False:
		tkinter.messagebox.showwarning(title="Invalid Input", message="Only enter Numbers")
	else:
		monthRent=int(sqFootMoney) * int(sqFoot)
		monthRentWithUtility=monthRent+int(Utility)
		weekRent=monthRentWithUtility/4
		yearRent=monthRentWithUtility*12
		outMessage='Monthly Rent is:$'+ str(monthRentWithUtility) + '\nWeekly Rent is:$'+ str(weekRent)+ '\nYearly Rent Is:$'+ str(yearRent)
		labelOutput = Label(GUI, text=outMessage)
		labelOutput.grid(row=6, column=1)


		splitName=customer.split()

		# letter size 612 x 792

		# set the file name
		filename = invoice+'_'+splitName[0]+'_'+splitName[1]+'_'+finalDate

		# create a canvas
		c = canvas.Canvas(f"output/{filename}.pdf", pagesize=letter)

		# set the font
		c.setFont('Helvetica', 12)

		# company logo
		c.drawImage("mjlogo.png", 100, 600, width=128, height=85)

		# top right text
		c.setFillColor("gray")
		c.drawString(400, 660, 'Invoice #:')
		c.setFillColor("black")
		c.drawString(460, 660, invoice)

		c.setFillColor("gray")
		c.drawString(423, 640, 'Date:')
		c.setFillColor("black")
		c.drawString(460, 640, finalDate)

		# company information
		c.drawString(100, 550, 'M&J Loudoun LLC')
		c.drawString(100, 530, '7 Loudoun St SW')
		c.drawString(100, 510, 'Leesburg, VA 20175')
		c.drawString(100, 490, '(703) 669-6400')

		# customer information
		c.setFillColor("black")
		c.drawString(400, 550, company)
		c.drawString(400, 530, customer)
		c.drawString(400, 510, address)
		c.drawString(400, 490, city +', '+state+' '+zipNum)

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
		c.drawString(100, 410, 'Monthly Rent')
		c.drawString(280, 410, '1')
		c.setFillColor("red")
		c.drawString(420, 410, '$'+str(monthRent))

		c.setFillColor("black")
		c.drawString(100, 390, 'Utility Cost')
		c.drawString(280, 390, '1')
		c.setFillColor("red")
		c.drawString(420, 390, '$'+str(Utility))


		# total due section
		c.setFont('Helvetica', 15)
		c.setFillColor("gray")
		c.drawString(325, 100, 'TOTAL DUE:')
		c.setFillColor("red")
		c.drawString(425, 100, '$'+str(monthRentWithUtility))

		# -------------------------------------------------
		c.showPage() # writes stuff to canvas
		c.save() # saves file and closes canvas

	


GUI=Tk()
GUI.geometry("1000x400")

GUI.title("Rent Calculation")

sqFootMoneyLabel=Label(GUI, text='Enter the amount of money per Sq. foot: ')
sqFootLabel=Label(GUI, text='Enter Sq. footage of the property: ')
utilityLabel=Label(GUI, text='Enter utilities cost per month: ')
companyLabel=Label(GUI, text='Enter the name of the company: ')
customerLabel=Label(GUI, text='Enter the name of the customer: ')
addressLabel=Label(GUI, text='Enter the address of the customer: ')
cityLabel=Label(GUI, text='Enter the city of the customer: ')
stateLabel=Label(GUI, text='Enter the state of the customer: ')
zipLabel=Label(GUI, text='Enter the zip code of the customer: ')
invoiceLabel=Label(GUI, text='Enter the invoice nunmber for the document: ')

sqFootMoneyLabel.grid(row=0, column=0)
sqFootLabel.grid(row=1, column=0)
utilityLabel.grid(row=2, column=0)
companyLabel.grid(row=3, column=0)
customerLabel.grid(row=4, column=0)
addressLabel.grid(row=0, column=2)
cityLabel.grid(row=1, column=2)
stateLabel.grid(row=2, column=2)
zipLabel.grid(row=3, column=2)
invoiceLabel.grid(row=4, column=2)

sqFootMoneyInput = tkinter.Entry(GUI)
sqFootInput = tkinter.Entry(GUI)
UtilityInput = tkinter.Entry(GUI)
companyInput = tkinter.Entry(GUI)
customerInput = tkinter.Entry(GUI)
addressInput = tkinter.Entry(GUI)
cityInput = tkinter.Entry(GUI)
stateInput = tkinter.Entry(GUI)
zipInput = tkinter.Entry(GUI)
invoiceInput = tkinter.Entry(GUI)

sqFootMoneyInput.grid(row=0, column=1)
sqFootInput.grid(row=1, column=1)
UtilityInput.grid(row=2, column=1)
companyInput.grid(row=3, column=1)
customerInput.grid(row=4, column=1)
addressInput.grid(row=0, column=3)
cityInput.grid(row=1, column=3)
stateInput.grid(row=2, column=3)
zipInput.grid(row=3, column=3)
invoiceInput.grid(row=4, column=3)

button1 = tkinter.Button(GUI, text='Calculate', width=30, command=calcRent, activebackground="green", activeforeground="white")
button1.grid(row=5, column=1)
GUI.mainloop()