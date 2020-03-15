
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

	#print('usr: ',username,'\npasswd: ',password)

	if username == 'user20' and password == 'pass20':
		mainApp()
	else:
		return False

def testQuery():
	# testing queries
	cursor.execute("SELECT * FROM track LIMIT 2")
	rows = cursor.fetchall()
	for tuple in rows:
		print(tuple)

def search(entry):

	if len(entry) > 0:
		query = "SELECT name FROM track WHERE artist= '" + str(entry).lower() + "'"
		cursor.execute(query)
		rows = cursor.fetchall()

		output = []
		for tuple in rows:
			output.append(str(tuple[0]))
		
		outputText = ['Songs: ']
		outputText.append(", ".join(output))
		outputText = "".join(outputText)

		outputLabel['text'] = outputText


'''
------------------------------------------
				GUI Setup
------------------------------------------
'''

global loginLogo,logo,searchIcon

# Login Screen
def loginApp():
	root.title('Soundic Login')

	canvas = tk.Canvas(root,height=200,width=500,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	loginLogoLabel = tk.Label(frame,image=loginLogo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	loginLogoLabel.place(relx=0.45,rely=0.05)

	usernameLabel = tk.Label(text = ' Username ',fg='#ffffff',bg='#121212')
	usernameLabel.place(relx=0.25,rely=0.4,relwidth=0.25,relheight=0.05)
	username = tk.Entry(fg='#ffffff',bg='#171717')
	username.place(relx=0.45,rely=0.38,relwidth=0.25,relheight=0.1)

	passwordLabel = tk.Label(text = ' Password ',fg='#ffffff',bg='#121212')
	passwordLabel.place(relx=0.25,rely=0.55,relwidth=0.25,relheight=0.05)
	password = tk.Entry(show='*',fg='#ffffff',bg='#171717')
	password.place(relx=0.45,rely=0.53,relwidth=0.25,relheight=0.1)

	loginButton = tk.Button(text='Login',bg='#121212',command=lambda: authenticate(username.get(),password.get()))
	loginButton.place(relx=0.45,rely=0.7)


# Stream Screen
def mainApp():
	root.title('Soundic')

	# Canvas setup
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()

	# Main frame
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Test queries
	testButton = tk.Button(frame,text='Query',command=testQuery,width=10,height=2,fg='#575757',bg='#101010')
	testButton.pack(side='right')
	#testButton.place(relx=0.25,rely=0.7,relwidth=0.5,relheight=0.2)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)

	# Search text field
	searchEntry = tk.Entry(frame,text='search...',fg='#ffffff',bg='#171717')
	searchEntry.place(relx=0.005,rely=0.01,relwidth=0.25,relheight=0.05)

	# Search Button
	searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get()))
	searchButton.place(relx=0.265,rely=0.015,relwidth=0.025,relheight=0.035)

	# Temporary query output label
	outputLabel = tk.Label(frame,text='Output',fg='#ffffff',bg='#171717')
	outputLabel.place(relx=0.25,rely=0.2,relwidth=0.5,relheight=0.2)


'''
------------------------------------------
				Run App
------------------------------------------
'''

root = tk.Tk()
loginLogo = tk.PhotoImage(file='logo-login.png')
logo = tk.PhotoImage(file='logo-soundic.png')
searchIcon = tk.PhotoImage(file='icon-search.png')

loginApp()
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()









