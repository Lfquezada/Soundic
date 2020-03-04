
import tkinter as tk
from tkinter import filedialog,Text
import os
import psycopg2 as pg

'''
root = tk.Tk()
canvas = tk.Canvas(root,height=500,width=500, bg='#171717')
canvas.pack()

frame = tk.Frame(root,bg='white')
frame.place()

streamButton = tk.Button(root,text='Stream',padx=10,pady=5,fg='#171717')
streamButton.pack()
root.mainloop()
'''

connection = pg.connect(user='postgres',host='localhost',port='5432',database='test',password='dbpass20')
cursor = connection.cursor()

# testing queries
cursor.execute("SELECT name,artist FROM track WHERE name='Levels'")
rows = cursor.fetchall()

for r in rows:
	print(r)


cursor.execute("SELECT name,artist FROM track WHERE artist='Coldplay'")
rows = cursor.fetchall()

for r in rows:
	print(r)

cursor.close()
connection.close()