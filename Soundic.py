
import tkinter as tk
import os
import psycopg2 as pg

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

	if username == 'user20' and password == 'pass20':
		confirmationLabel['text'] = 'Login Successful'
		confirmationLabel['fg'] = '#2ecc71'
		mainApp()
	else:
		confirmationLabel['text'] = 'Invalid username or password'
		confirmationLabel['fg'] = '#e74c3c'


def createUser(firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email):

	print(firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email)

	query = """

	PERFORM INSERT HERE

	"""

	#cursor.execute(query)
	#rows = cursor.fetchall()

	loginApp(reload=True)


def testQuery():
	# testing queries
	cursor.execute("SELECT * FROM Customer LIMIT 5")
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

		output = []
		for tuple in rows:
			output.append(str(tuple))
		
		outputText = ['Songs: ']
		outputText.append("\n".join(output))
		outputText = "\n".join(outputText)

		outputLabel['text'] = outputText


'''
------------------------------------------
				GUI Setup
------------------------------------------
'''

global loginLogo,logo,searchIcon,userIcon

# Login Screen
def loginApp(reload):
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
	confirmationLabel.place(relx=0.4,rely=0.8)

	loginButton = tk.Button(text='Login',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: authenticate(username.get(),password.get()))
	loginButton.place(relx=0.35,rely=0.68,relwidth=0.15)

	registerButton = tk.Button(text='Register',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: register())
	registerButton.place(relx=0.55,rely=0.68,relwidth=0.15)


# Register Screen
def register():
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
	password = tk.Entry(show='*',fg='#ffffff',bg='#171717')
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
	regConfLabel.place(relx=0.4,rely=0.9)

	loginButton = tk.Button(text='Create',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: createUser(firstName.get(),lastName.get(),company.get(),address.get(),city.get(),state.get(),country.get(),postalCode.get(),phone.get(),fax.get(),email.get()))
	loginButton.place(relx=0.35,rely=0.95,relwidth=0.15)

	registerButton = tk.Button(text='Go Back',bg='#121212',borderwidth=0, highlightthickness=0,command=lambda: loginApp(reload=True))
	registerButton.place(relx=0.55,rely=0.95,relwidth=0.15)


# Stream Screen
def mainApp():
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

	# Temporary query output label
	global outputLabel
	outputLabel = tk.Label(frame,text=' Welcome to Soundic! ',fg='#ffffff',bg='#171717')
	outputLabel.place(relx=0.25,rely=0.2,relwidth=0.5,relheight=0.6)


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

loginApp(reload=False)
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()









