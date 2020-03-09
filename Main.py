
import tkinter as tk
import os
import psycopg2 as pg

'''
------------------------------------------
			Conection to DB
------------------------------------------
'''
connection = pg.connect(user='postgres',host='localhost',port='5432',database='test',password='dbpass20')
cursor = connection.cursor()

def testQuery():
	# testing queries
	cursor.execute("SELECT * FROM tracks")
	rows = cursor.fetchall()
	for tuple in rows:
		print(tuple)

def search(entry):

	if len(entry) > 0:
		query = "SELECT name FROM tracks WHERE artist= '" + str(entry).lower() + "'"
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
root = tk.Tk()
root.title('Soundic')

# Canvas setup
canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
canvas.pack()

# Main frame
frame = tk.Frame(root,bg='#121212')
frame.place(relx=0,rely=0,relwidth=1,relheight=1)

# Test queries
testButton = tk.Button(root,text='Query',command=testQuery,width=10,height=2,fg='#575757',bg='#101010')
testButton.pack(side='right')

# Soundic Logo
logo = tk.PhotoImage(file='logo-soundic.png')
logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
logoLabel.place(relx=0.82,rely=0.01)

# Search text field
searchEntry = tk.Entry(frame,text='entry',fg='#ffffff',bg='#171717')
searchEntry.place(relx=0.005,rely=0.01,relwidth=0.25,relheight=0.05)

# Search Button
searchIcon = tk.PhotoImage(file='icon-search.png')
searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get()))
searchButton.place(relx=0.265,rely=0.015,relwidth=0.025,relheight=0.04)

# Temporary query output label
outputLabel = tk.Label(frame,text='Output',fg='#ffffff',bg='#171717')
outputLabel.place(relx=0.25,rely=0.2,relwidth=0.5,relheight=0.2)


'''
------------------------------------------
				Run App
------------------------------------------
'''
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()









