
import tkinter as tk
from tkinter import filedialog,Text
import os

root = tk.Tk()
canvas = tk.Canvas(root,height=500,width=500, bg='#171717')
canvas.pack()

frame = tk.Frame(root,bg='white')
frame.place()

streamButton = tk.Button(root,text='Stream',padx=10,pady=5,fg='#171717')
streamButton.pack()


root.mainloop()


