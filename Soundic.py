
import tkinter as tk
from tkinter import ttk
import os
import psycopg2 as pg
import random

'''
------------------------------------------
			Conection to DB
------------------------------------------
'''
connection = pg.connect(user='postgres',host='localhost',port='5432',database='Proyecto',password='dbpass20')
cursor = connection.cursor()


'''
------------------------------------------
			Functions
------------------------------------------
'''
def authenticate(username,password):

	if username == 'masteruser' and password == 'masterpass':
		confirmationLabel['text'] = 'Login Successful'
		confirmationLabel['fg'] = '#2ecc71'
		mainApp(username)

	query = """
	SELECT DISTINCT c.passwrd
	FROM Customer c
	WHERE c.username = '""" + username + """'
	"""

	cursor.execute(query)
	rows = cursor.fetchall()

	if len(rows) == 0:
		confirmationLabel['text'] = 'Invalid username'
		confirmationLabel['fg'] = '#e74c3c'
	else:
		if password == rows[0][0]:
			confirmationLabel['text'] = 'Login Successful'
			confirmationLabel['fg'] = '#2ecc71'
			mainApp(username)
		else:
			confirmationLabel['text'] = 'Invalid password'
			confirmationLabel['fg'] = '#e74c3c'


def createUser(username,password,firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email):

	if len(firstName) <= 1 or len(lastName) <= 1 or len(username) <= 1 or len(password) <= 1 or len(username) > 10 or len(password) > 20:
		# not a valid register, show a red warning
		regConfLabel['text'] = 'Invalid data lenght'
		regConfLabel['fg'] = '#e74c3c'
	else:
		# valid register but username may already exist

		query = """
		SELECT c.username
		FROM Customer c
		WHERE c.username = '""" + username + """'
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		
		if len(rows) > 0:
			# then username already exists, show red warning
			regConfLabel['text'] = 'Username already exists'
			regConfLabel['fg'] = '#e74c3c'

		else:
			# its a valid register with a unique username
			regConfLabel['text'] = 'Successful Registration'
			regConfLabel['fg'] = '#2ecc71'

			# get the last custumer id added
			query = """
			SELECT c.CustomerId
			FROM Customer c
			ORDER BY c.CustomerId DESC
			LIMIT 1
			"""
			cursor.execute(query)
			rows = cursor.fetchall()
			newCustomerId = rows[0][0] + 1
			newCustomerId = str(newCustomerId)

			# get a random employee id
			query = """
			SELECT e.EmployeeId
			FROM Employee e
			"""
			cursor.execute(query)
			rows = cursor.fetchall()
			newSupportRepId = rows[random.randint(1,len(rows)-1)][0]
			newSupportRepId = str(newSupportRepId)

			query = """

			INSERT INTO Customer (username,passwrd,CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId) 
			VALUES ('""" + username + """','""" + password + """',""" + newCustomerId + """,'""" + firstName + """','""" + lastName + """','""" + company + """','""" + address + """','""" + city + """','""" + state + """','""" + country + """','""" + postalCode + """','""" + phone + """','""" + fax + """','""" + email + """',""" + newSupportRepId + """);

			"""

			cursor.execute(query)
			connection.commit()
			login(reload=True)


def testQuery():
	# testing queries

	query = """
	SELECT *
	FROM Customer
	ORDER BY Customer.CustomerId DESC
	LIMIT 1
	"""

	cursor.execute(query)
	rows = cursor.fetchall()
	for tuple in rows:
		print(tuple)


def search(entry):

	entry = str(entry)

	if len(entry) > 0:

		query = """
		SELECT Track.Name,Artist.Name,Album.Title,Genre.Name
		FROM Track
		JOIN Album ON Album.AlbumId = Track.AlbumId
		JOIN Artist ON Artist.ArtistId = Album.ArtistId
		JOIN Genre ON Genre.GenreId = Track.GenreId
		WHERE Album.Title = '""" + entry + """'
		"""

		cursor.execute(query)
		rows = cursor.fetchall()

		# Search for anything else (artist or track or genre)
		if len(rows) == 0:

			query = """
			SELECT Track.Name,Artist.Name,Album.Title,Genre.Name
			FROM Track
			JOIN Album ON Album.AlbumId = Track.AlbumId
			JOIN Artist ON Artist.ArtistId = Album.ArtistId
			JOIN Genre ON Genre.GenreId = Track.GenreId
			WHERE Artist.Name = '""" + entry + """' OR Track.Name = '""" + entry + """' OR Genre.Name = '""" + entry + """'
			"""

			cursor.execute(query)
			rows = cursor.fetchall()
		displaySearchResult(rows)


# Fill listboxes with the query result
def displaySearchResult(rows):
	outputTable.updateData(rows)


'''
------------------------------------------
				Clases
------------------------------------------
'''
class MultiColumnListbox(object):

	def __init__(self,frame,headings,rows):
		self.frame = frame
		self.tree = None
		self.columnsToShow = headings
		self._setup_widgets(frame)
		self._build_tree(rows)

	def _setup_widgets(self,frame):
		container = ttk.Frame(frame)
		container.place(relx=0.025,rely=0.1,relwidth=0.85,relheight=0.8)

		style = ttk.Style()
		style.configure("darkStyle.Treeview",font=('Arial', 14),fieldbackground="#121212",background="#121212", foreground="white", relief="flat",rowheight=30)
		style.configure("darkStyle.Treeview.Heading", font=('Arial', 15,'bold'),fieldbackground="#121212",background="white", foreground="#0f0f0f", relief="flat")

		self.tree = ttk.Treeview(columns=self.columnsToShow, show="headings",style="darkStyle.Treeview")

		vsb = ttk.Scrollbar(orient="vertical",command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
		vsb.grid(column=1, row=0, sticky='ns', in_=container)
		hsb.grid(column=0, row=1, sticky='ew', in_=container)
		container.grid_columnconfigure(0, weight=1)
		container.grid_rowconfigure(0, weight=1)

		self.tree.tag_configure('odd',background='#171717')
		self.tree.tag_configure('even',background='#121212')

	def _build_tree(self,rows):
		for col in self.columnsToShow:
			self.tree.heading(col, text=col.title())
			self.tree.column(col,width=40)

		index = 0
		for row in rows:
			index += 1
			if index%2 == 0:
				self.tree.insert('', 'end', values=row,tags=('even'))
			else:
				self.tree.insert('', 'end', values=row,tags=('odd'))

			for ix, val in enumerate(row):
				self.tree.column(self.columnsToShow[ix], width=251)

	def updateData(self,rows):
		for i in self.tree.get_children():
			self.tree.delete(i)

		index = 0
		for row in rows:
			index += 1
			if index%2 == 0:
				self.tree.insert('', 'end', values=row,tags=('even'))
			else:
				self.tree.insert('', 'end', values=row,tags=('odd'))

			for ix, val in enumerate(row):
				self.tree.column(self.columnsToShow[ix], width=251)




'''
------------------------------------------
				GUI Setup
------------------------------------------
'''

global loginLogo,logo,searchIcon,userIcon

# Login Screen
def login(reload):
	root.title('Soundic Login')

	global canvas

	if reload:
		canvas.destroy()

	canvas = tk.Canvas(root,height=300,width=500,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	loginLogoLabel = tk.Label(frame,image=loginLogo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	loginLogoLabel.place(relx=0.45,rely=0.05)

	usernameLabel = tk.Label(text = ' Username ',fg='#ffffff',bg='#121212')
	usernameLabel.place(relx=0.25,rely=0.35,relwidth=0.25,relheight=0.05)
	username = tk.Entry(fg='#ffffff',bg='#171717')
	username.place(relx=0.45,rely=0.33,relwidth=0.25,relheight=0.09)

	passwordLabel = tk.Label(text = ' Password ',fg='#ffffff',bg='#121212')
	passwordLabel.place(relx=0.25,rely=0.5,relwidth=0.25,relheight=0.05)
	password = tk.Entry(show='*',fg='#ffffff',bg='#171717')
	password.place(relx=0.45,rely=0.48,relwidth=0.25,relheight=0.09)

	global confirmationLabel
	confirmationLabel = tk.Label(text = ' ',font='Arial 12',fg='#121212',bg='#121212')
	confirmationLabel.place(relx=0.34,rely=0.78)

	loginButton = tk.Button(text='Login',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: authenticate(username.get(),password.get()))
	loginButton.place(relx=0.35,rely=0.68,relwidth=0.15)

	registerButton = tk.Button(text='Sign In',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: signin())
	registerButton.place(relx=0.55,rely=0.68,relwidth=0.15)


# Register Screen
def signin():
	root.title('Soundic Register')

	boxWidth = 0.25
	boxHeight = 0.05

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=900,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	loginLogoLabel = tk.Label(frame,image=loginLogo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	loginLogoLabel.place(relx=0.47,rely=0.04)

	usernameLabel = tk.Label(text = 'Username',fg='#ffffff',bg='#121212')
	usernameLabel.place(relx=0.45,rely=0.15,relwidth=0.25,relheight=0.05)
	username = tk.Entry(fg='#ffffff',bg='#171717')
	username.place(relx=0.65,rely=0.15,relwidth=boxWidth,relheight=boxHeight)

	passwordLabel = tk.Label(text = 'Password',fg='#ffffff',bg='#121212')
	passwordLabel.place(relx=0.45,rely=0.22,relwidth=0.25,relheight=0.05)
	password = tk.Entry(fg='#ffffff',bg='#171717')
	password.place(relx=0.65,rely=0.22,relwidth=boxWidth,relheight=boxHeight)

	firstNameLabel = tk.Label(text = 'First Name',fg='#ffffff',bg='#121212')
	firstNameLabel.place(relx=0.05,rely=0.15,relwidth=0.25,relheight=0.05)
	firstName = tk.Entry(fg='#ffffff',bg='#171717')
	firstName.place(relx=0.25,rely=0.15,relwidth=boxWidth,relheight=boxHeight)

	lastNameLabel = tk.Label(text = 'Last Name',fg='#ffffff',bg='#121212')
	lastNameLabel.place(relx=0.05,rely=0.22,relwidth=0.25,relheight=0.05)
	lastName = tk.Entry(fg='#ffffff',bg='#171717')
	lastName.place(relx=0.25,rely=0.22,relwidth=boxWidth,relheight=boxHeight)

	companyLabel = tk.Label(text = 'Company',fg='#ffffff',bg='#121212')
	companyLabel.place(relx=0.05,rely=0.29,relwidth=0.25,relheight=0.05)
	company = tk.Entry(fg='#ffffff',bg='#171717')
	company.place(relx=0.25,rely=0.29,relwidth=boxWidth,relheight=boxHeight)

	addressLabel = tk.Label(text = 'Address',fg='#ffffff',bg='#121212')
	addressLabel.place(relx=0.05,rely=0.36,relwidth=0.25,relheight=0.05)
	address = tk.Entry(fg='#ffffff',bg='#171717')
	address.place(relx=0.25,rely=0.36,relwidth=boxWidth,relheight=boxHeight)

	cityLabel = tk.Label(text = 'City',fg='#ffffff',bg='#121212')
	cityLabel.place(relx=0.05,rely=0.43,relwidth=0.25,relheight=0.05)
	city = tk.Entry(fg='#ffffff',bg='#171717')
	city.place(relx=0.25,rely=0.43,relwidth=boxWidth,relheight=boxHeight)

	stateLabel = tk.Label(text = 'State',fg='#ffffff',bg='#121212')
	stateLabel.place(relx=0.05,rely=0.5,relwidth=0.25,relheight=0.05)
	state = tk.Entry(fg='#ffffff',bg='#171717')
	state.place(relx=0.25,rely=0.5,relwidth=boxWidth,relheight=boxHeight)

	countryLabel = tk.Label(text = 'Country',fg='#ffffff',bg='#121212')
	countryLabel.place(relx=0.05,rely=0.57,relwidth=0.25,relheight=0.05)
	country = tk.Entry(fg='#ffffff',bg='#171717')
	country.place(relx=0.25,rely=0.57,relwidth=boxWidth,relheight=boxHeight)

	postalCodeLabel = tk.Label(text = 'Postal Code',fg='#ffffff',bg='#121212')
	postalCodeLabel.place(relx=0.05,rely=0.64,relwidth=0.25,relheight=0.05)
	postalCode = tk.Entry(fg='#ffffff',bg='#171717')
	postalCode.place(relx=0.25,rely=0.64,relwidth=boxWidth,relheight=boxHeight)

	phoneLabel = tk.Label(text = 'Phone',fg='#ffffff',bg='#121212')
	phoneLabel.place(relx=0.05,rely=0.71,relwidth=0.25,relheight=0.05)
	phone = tk.Entry(fg='#ffffff',bg='#171717')
	phone.place(relx=0.25,rely=0.71,relwidth=boxWidth,relheight=boxHeight)

	faxLabel = tk.Label(text = 'Fax',fg='#ffffff',bg='#121212')
	faxLabel.place(relx=0.05,rely=0.78,relwidth=0.25,relheight=0.05)
	fax = tk.Entry(fg='#ffffff',bg='#171717')
	fax.place(relx=0.25,rely=0.78,relwidth=boxWidth,relheight=boxHeight)

	emailLabel = tk.Label(text = 'Email',fg='#ffffff',bg='#121212')
	emailLabel.place(relx=0.05,rely=0.85,relwidth=0.25,relheight=0.05)
	email = tk.Entry(fg='#ffffff',bg='#171717')
	email.place(relx=0.25,rely=0.85,relwidth=boxWidth,relheight=boxHeight)

	global regConfLabel
	regConfLabel = tk.Label(text = ' ',font='Arial 12',fg='#2ecc71',bg='#121212')
	regConfLabel.place(relx=0.7,rely=0.3)

	loginButton = tk.Button(text='Create',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: createUser(username.get(),password.get(),firstName.get(),lastName.get(),company.get(),address.get(),city.get(),state.get(),country.get(),postalCode.get(),phone.get(),fax.get(),email.get()))
	loginButton.place(relx=0.35,rely=0.95,relwidth=0.15)

	signInButton = tk.Button(text='Go Back',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: login(reload=True))
	signInButton.place(relx=0.55,rely=0.95,relwidth=0.15)


# Stream Screen
def mainApp(currentUsername):
	root.title('Soundic')

	# Canvas setup
	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()

	# Main frame
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Test queries
	testButton = tk.Button(frame,text='Query',command=testQuery,width=10,height=2,fg='#575757',bg='#101010')
	testButton.pack(side='right')

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)

	# Search text field
	searchEntry = tk.Entry(frame,text='search...',fg='#ffffff',bg='#171717')
	searchEntry.place(relx=0.005,rely=0.01,relwidth=0.25,relheight=0.05)

	# Search Button
	searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get()))
	searchButton.place(relx=0.265,rely=0.015,relwidth=0.025,relheight=0.042)

	# Profile Button
	profileButton = tk.Button(frame,image=userIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	profileButton.place(relx=0.75,rely=0.02,relwidth=0.025,relheight=0.042)

	# Logged in Label
	loggedLabel = tk.Label(frame,text=' Logged in as  '+ currentUsername,font='Arial 12',fg='#2ecc71',bg='#101010')
	loggedLabel.place(relx=0.55,rely=0.03)

	global outputTable
	outputTable = MultiColumnListbox(frame,['Songs','Artists','Albums','Genres'],[])



'''
------------------------------------------
				Run App
------------------------------------------
'''

root = tk.Tk()
root.configure(background='black')

# preload assets
loginLogo = tk.PhotoImage(file='logo-login.png')
logo = tk.PhotoImage(file='logo-soundic.png')
searchIcon = tk.PhotoImage(file='icon-search.png')
userIcon = tk.PhotoImage(file='icon-user.png')

login(reload=False)
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()









