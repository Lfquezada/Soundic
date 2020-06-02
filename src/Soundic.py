
import tkinter as tk
from tkinter import ttk,messagebox
import os
import psycopg2 as pg
import random
import csv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib.request,urllib.parse,re
import webbrowser as wb

'''
------------------------------------------
			Conection to DB
------------------------------------------
'''
connection = pg.connect(user='postgres',host='localhost',port='5432',database='Soundic',password='dbpass20')
cursor = connection.cursor()


'''
------------------------------------------
			Functions
------------------------------------------
'''
def authenticate(username,password):
	query = """
	SELECT c.passwrd
	FROM Customer c
	WHERE c.username = %s
	LIMIT 1
	"""
	cursor.execute(query,[username])
	rows = cursor.fetchall()

	if len(rows) == 0: # means no username in customers was found, we search if its an employee
		query = """
		SELECT e.passwrd
		FROM Employee e
		WHERE e.username = %s
		LIMIT 1
		"""

		cursor.execute(query,[username])
		rows = cursor.fetchall()

		if len(rows) == 0: # no username match was made so its an invalid username
			confirmationLabel['text'] = 'Invalid username'
		else:
			if password == rows[0][0]:
				mainApp(username,isEmployee=True)
			else:
				confirmationLabel['text'] = 'Invalid password'
	else:
		if password == rows[0][0]:
			mainApp(username,isEmployee=False)
		else:
			confirmationLabel['text'] = 'Invalid password'

def logout():
	login(reload=True)


def showProfile(username,isEmployee):

	# Set up window
	profileWindow = tk.Tk()
	windowTitle = username + "'s Profile"
	profileWindow.title(windowTitle)
	canvas2 = tk.Canvas(profileWindow,height=125,width=300,bg='#101010')
	canvas2.pack()
	frame2 = tk.Frame(profileWindow,bg='#121212')
	frame2.place(relx=0,rely=0,relwidth=1,relheight=1)

	if isEmployee:
		query = """
		SELECT e.EmployeeId, e.FirstName, e.LastName
		FROM Employee e
		WHERE e.username = %s
		"""
	else:
		query = """
		SELECT c.CustomerId, c.FirstName, c.LastName
		FROM Customer c
		WHERE c.username = %s
		"""

	cursor.execute(query,[username])
	rows = cursor.fetchall()

	if len(rows) > 0:
		spacer = tk.Label(frame2,text = ' ',fg='#ffffff',bg='#121212')
		spacer.pack(side='top')

		userIdLabel = tk.Label(frame2,text = 'User ID: ' + str(rows[0][0]),fg='#ffffff',bg='#121212')
		userIdLabel.pack(side='top')

		userFNLabel = tk.Label(frame2,text = 'First Name: ' + str(rows[0][1]),fg='#ffffff',bg='#121212')
		userFNLabel.pack(side='top')

		userLNLabel = tk.Label(frame2,text = 'Last Name: ' + str(rows[0][2]),fg='#ffffff',bg='#121212')
		userLNLabel.pack(side='top')


def registerPage(username,isEmployee):
	root.title('Register')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Register',font='Arial 41 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')
	spacer1 = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacer1.pack(side='top')

	regArtistButton = tk.Button(frame,text='Artist',command=lambda: registerArtist(username,isEmployee),width=20,height=2,fg='#575757')
	regArtistButton.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer2.pack(side='top')

	regAlbumButton = tk.Button(frame,text='Album',command=lambda: registerAlbum(username,isEmployee),width=20,height=2,fg='#575757')
	regAlbumButton.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer3.pack(side='top')

	regTrackButton = tk.Button(frame,text='Track',command=lambda: registerTrack(username,isEmployee),width=20,height=2,fg='#575757')
	regTrackButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',borderwidth=0, highlightthickness=0,command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def registerArtist(username,isEmployee):
	root.title('Register Artist')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global registerArtistWarning
	registerArtistWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	registerArtistWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	regArtistButton = tk.Button(frame,text='Register',command=lambda: createArtist(username,isEmployee,artistNameEntry.get()),width=15,height=2,fg='#575757')
	regArtistButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def registerAlbum(username,isEmployee):
	root.title('Register Album')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Album Title',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	albumTitleEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	albumTitleEntry.pack(side='top')

	global registerAlbumWarning
	registerAlbumWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	registerAlbumWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	regAlbumButton = tk.Button(frame,text='Register',command=lambda: createAlbum(username,isEmployee,albumTitleEntry.get(),artistNameEntry.get()),width=15,height=2,fg='#575757')
	regAlbumButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def registerTrack(username,isEmployee):
	root.title('Register Track')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	boxWidth = 0.28
	col1Xpos = 0.23

	instruction1 = tk.Label(frame,text = 'Enter Track Name *',fg='#ffffff',bg='#121212')
	instruction1.place(relx=col1Xpos,rely=0.1)
	trackNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	trackNameEntry.place(relx=col1Xpos,rely=0.13,relwidth=boxWidth)

	instruction2 = tk.Label(frame,text = 'Enter Album Title *',fg='#ffffff',bg='#121212')
	instruction2.place(relx=col1Xpos,rely=0.2)
	albumTitleEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	albumTitleEntry.place(relx=col1Xpos,rely=0.23,relwidth=boxWidth)

	global albumNotFoundWarning
	albumNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	albumNotFoundWarning.place(relx=col1Xpos,rely=0.27)

	instruction3 = tk.Label(frame,text = 'Select Media Type *',fg='#ffffff',bg='#121212')
	instruction3.place(relx=col1Xpos,rely=0.3)

	mediaTypes = ['MPEG audio file','Protected AAC audio file','Protected MPEG-4 video file','Purchased AAC audio file','AAC audio file']
	varMediaType = tk.StringVar(frame)
	varMediaType.set(mediaTypes[0])
	dropDownMenuMediaType = tk.OptionMenu(frame,varMediaType,mediaTypes[0],mediaTypes[1],mediaTypes[2],mediaTypes[3],mediaTypes[4])
	dropDownMenuMediaType.config(bg='#121212')
	dropDownMenuMediaType.place(relx=col1Xpos,rely=0.34,relwidth=boxWidth)

	instruction4 = tk.Label(frame,text = 'Enter Genre *',fg='#ffffff',bg='#121212')
	instruction4.place(relx=col1Xpos,rely=0.4)
	genreEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	genreEntry.place(relx=col1Xpos,rely=0.43,relwidth=boxWidth)

	global genreNotFoundWarning
	genreNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	genreNotFoundWarning.place(relx=col1Xpos,rely=0.47)

	instruction5 = tk.Label(frame,text = 'Enter Composer',fg='#ffffff',bg='#121212')
	instruction5.place(relx=col1Xpos,rely=0.5)
	composerEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	composerEntry.place(relx=col1Xpos,rely=0.53,relwidth=boxWidth)

	# Col 2

	instruction6 = tk.Label(frame,text = 'Enter Milliseconds *',fg='#ffffff',bg='#121212')
	instruction6.place(relx=0.55,rely=0.1)
	millisecEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	millisecEntry.place(relx=0.55,rely=0.13)

	global millisecErrorWarning
	millisecErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	millisecErrorWarning.place(relx=0.55,rely=0.17)

	instruction7 = tk.Label(frame,text = 'Enter Bytes',fg='#ffffff',bg='#121212')
	instruction7.place(relx=0.55,rely=0.2)
	bytesEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	bytesEntry.place(relx=0.55,rely=0.23)

	global bytesErrorWarning
	bytesErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	bytesErrorWarning.place(relx=0.55,rely=0.27)

	instruction8 = tk.Label(frame,text = 'Enter Unit Price *',fg='#ffffff',bg='#121212')
	instruction8.place(relx=0.55,rely=0.3)
	unitPriceEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	unitPriceEntry.place(relx=0.55,rely=0.33)

	global unitPriceErrorWarning
	unitPriceErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	unitPriceErrorWarning.place(relx=0.55,rely=0.37)

	regTrackButton = tk.Button(frame,text='Register',command=lambda: createTrack(username,isEmployee,trackNameEntry.get(),albumTitleEntry.get(),varMediaType.get(),genreEntry.get(),composerEntry.get(),millisecEntry.get(),bytesEntry.get(),unitPriceEntry.get()),width=15,height=2,fg='#575757')
	regTrackButton.place(relx=0.55,rely=0.45)

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def createArtist(username,isEmployee,artistName):
	registerArtistWarning['text'] = ''

	if len(artistName) > 0:

		query = """
		SELECT *
		FROM Artist a
		WHERE a.Name = %s
		"""
		cursor.execute(query,[artistName])
		rows = cursor.fetchall()

		if len(rows) > 0:
			registerArtistWarning['text'] = 'Artist already exists'
		else:

			# get the last ArtistId added and add 1 to make the new one
			query = """
			SELECT a.ArtistId
			FROM Artist a
			ORDER BY a.ArtistId DESC
			LIMIT 1
			"""
			cursor.execute(query)
			rows = cursor.fetchall()
			newArtistId = rows[0][0] + 1

			query = """
			INSERT INTO Artist (ArtistId,Name,lastModBy) 
			VALUES (%s,%s,%s);
			"""
			cursor.execute(query,[newArtistId,artistName,username])
			connection.commit()
			mainApp(username,isEmployee)
	else:
		registerArtistWarning['text'] = 'Please enter a name'


def createAlbum(username,isEmployee,albumTitle,artistName):
	registerAlbumWarning['text'] = ''
	artistNotFoundWarning['text'] = ''

	if len(albumTitle) > 0 and len(artistName) > 0:

		query = """
		SELECT a.ArtistId
		FROM Artist a
		WHERE a.Name = %s
		"""
		cursor.execute(query,[artistName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			artistNotFoundWarning['text'] = 'Artist not found'
		else:
			#get the ArtistId
			artistId = rows[0][0]

			# get the last AlbumId added and add 1 to make the new one
			query = """
			SELECT a.AlbumId
			FROM Album a
			ORDER BY a.AlbumId DESC
			LIMIT 1
			"""
			cursor.execute(query)
			rows = cursor.fetchall()
			newAlbumId = rows[0][0] + 1

			query = """
			INSERT INTO Album (AlbumId,Title,ArtistId,lastModBy) 
			VALUES (%s,%s,%s,%s);
			"""
			cursor.execute(query,[newAlbumId,albumTitle,artistId,username])
			connection.commit()
			mainApp(username,isEmployee)
	else:
		registerAlbumWarning['text'] = 'Some required field is empty'
		artistNotFoundWarning['text'] = 'Some required field is empty'


def createTrack(username,isEmployee,trackName,albumTitle,mediaType,genreName,composer,millisec,bytes,unitPrice):

	# Show nothing on all warnings (reset per click)
	warnings = [albumNotFoundWarning,genreNotFoundWarning,millisecErrorWarning,bytesErrorWarning,unitPriceErrorWarning]
	for w in warnings:
		w['text'] = ''

	if len(trackName) <= 0 or len(millisec) <= 0 or len(unitPrice) <= 0 or len(albumTitle) <= 0 or len(genreName) <= 0:
		albumNotFoundWarning['text'] = 'Some required field is empty'
		genreNotFoundWarning['text'] = 'Some required field is empty'
		millisecErrorWarning['text'] = 'Some required field is empty'
		unitPriceErrorWarning['text'] = 'Some required field is empty'
	else:

		# CHECK IF ALBUM EXISTS
		query = """
		SELECT a.AlbumId
		FROM Album a
		WHERE a.Title = %s
		LIMIT 1
		"""
		cursor.execute(query,[albumTitle])
		rows = cursor.fetchall()

		if len(rows) <= 0 and albumTitle != '':
			albumNotFoundWarning['text'] = 'Album not found'
		else:
			if albumTitle == '':
				albumId = None
			else:
				albumId = rows[0][0]

			# get the mediatypeid
			query = """
			SELECT m.MediaTypeId
			FROM MediaType m
			WHERE m.Name = %s
			LIMIT 1
			"""
			cursor.execute(query,[mediaType])
			rows = cursor.fetchall()
			mediaTypeId = rows[0][0]

			# CHECK IF GENRE EXISTS
			query = """
			SELECT g.GenreId
			FROM Genre g
			WHERE g.Name = %s
			LIMIT 1
			"""
			cursor.execute(query,[genreName])
			rows = cursor.fetchall()

			if len(rows) <= 0 and genreName != '':
				genreNotFoundWarning['text'] = 'Genre not found'
			else:
				genreId = None if genreName == '' else rows[0][0]
				composer = None if composer == '' else composer
				bytes = None if bytes == '' else bytes

				if isInt(millisec):
					if isInt(bytes) or bytes == None:
						if isFloat(unitPrice):

							# EVERY ENTRY IS CORRECT

							# get the new TrackId
							query = """
							SELECT t.TrackId
							FROM Track t
							ORDER BY t.TrackId DESC
							LIMIT 1
							"""
							cursor.execute(query)
							rows = cursor.fetchall()
							newTrackId = rows[0][0] + 1

							query = """
							INSERT INTO Track (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice,Active,lastModBy)
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
							"""
							cursor.execute(query,[newTrackId,trackName,albumId,mediaTypeId,genreId,composer,millisec,bytes,unitPrice,True,username])
							connection.commit()

							# SAVE THE CUSTOMER WHO REGISTERED THE TRACK
							if not isEmployee:
								# get the customerid
								query = """
								SELECT c.CustomerId
								FROM Customer c
								WHERE c.username = %s
								LIMIT 1
								"""
								cursor.execute(query,[username])
								rows = cursor.fetchall()
								customerid = str(rows[0][0])

								query = """
								INSERT INTO track_register (TrackId, CustomerId)
								VALUES (%s,%s)
								"""
								cursor.execute(query,[newTrackId,customerid])
								connection.commit()

							mainApp(username,isEmployee)

						else:
							unitPriceErrorWarning['text'] = 'Unit price must be a number'
					else:
						bytesErrorWarning['text'] = 'Bytes must be an integer'
				else:
					millisecErrorWarning['text'] = 'Millisecongs must be an integer'


def inactivateTrackPage(username,isEmployee):
	root.title('Inactivate Track')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Track Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	trackNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	trackNameEntry.pack(side='top')

	global trackNotFoundWarning
	trackNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	trackNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	inactivateButton = tk.Button(frame,text='Inactivate',command=lambda: inactivateTrack(username,isEmployee,trackNameEntry.get(),artistNameEntry.get()),width=15,height=2,fg='#575757')
	inactivateButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def inactivateTrack(username,isEmployee,trackName,artistName):
	trackNotFoundWarning['text'] = ''
	artistNotFoundWarning['text'] = ''

	if len(trackName) > 0 and len(artistName) > 0:

		# CHECK IF TRACK NAME IS VALID
		query = """
		SELECT t.TrackId
		FROM Track t
		WHERE t.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[trackName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			trackNotFoundWarning['text'] = 'Track not found'
		else:

			# CHECK THE ARTIST MATCHES THE TRACK NAME
			query = """
			SELECT Track.TrackId
			FROM Track 
			JOIN Album ON Album.AlbumId = Track.AlbumId
			JOIN Artist ON Artist.ArtistId = Album.ArtistId
			WHERE Artist.Name = %s AND Track.Name = %s
			"""
			cursor.execute(query,[artistName,trackName])
			rows = cursor.fetchall()

			if len(rows) <= 0:
				artistNotFoundWarning['text'] = 'Artist for track not found'
			else:
				# GET THE UNIQUE TRACK ID AND SET active TO false
				trackId = rows[0][0]
				query = "UPDATE Track SET Active = false WHERE TrackId = %s"
				cursor.execute(query,[trackId])
				connection.commit()
				mainApp(username,isEmployee)
	else:
		trackNotFoundWarning['text'] = 'Some information is missing'
		artistNotFoundWarning['text'] = 'Some information is missing'


def modifyPage(username,isEmployee):
	root.title('Modify')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Modify',font='Arial 41 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')
	spacer1 = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacer1.pack(side='top')

	modArtistButton = tk.Button(frame,text='Artist',command=lambda: modArtistPage(username,isEmployee),width=20,height=2,fg='#575757')
	modArtistButton.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer2.pack(side='top')

	modAlbumButton = tk.Button(frame,text='Album',command=lambda: modAlbumPage(username,isEmployee),width=20,height=2,fg='#575757')
	modAlbumButton.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer3.pack(side='top')

	modTrackButton = tk.Button(frame,text='Track',command=lambda: selectTrackToModPage(username,isEmployee),width=20,height=2,fg='#575757')
	modTrackButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',borderwidth=0, highlightthickness=0,command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def modArtistPage(username,isEmployee):
	root.title('Modify Artist')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 140',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 20',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter New Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	newArtistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	newArtistNameEntry.pack(side='top')

	global newArtistNameWarning
	newArtistNameWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	newArtistNameWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	modArtistButton = tk.Button(frame,text='Change',command=lambda: modArtist(username,isEmployee,artistNameEntry.get(),newArtistNameEntry.get()),width=15,height=2,fg='#575757')
	modArtistButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')

def modArtist(username,isEmployee,artistName,newArtistName):
	artistNotFoundWarning['text'] = ''
	newArtistNameWarning['text'] = ''
	
	if len(artistName) > 0 and len(newArtistName):

		query = """
		SELECT a.ArtistId
		FROM Artist a
		WHERE a.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[newArtistName])
		rows = cursor.fetchall()

		if len(rows) <= 0: # check if new artist name is available
			query = """
			SELECT a.ArtistId
			FROM Artist a
			WHERE a.Name = %s
			LIMIT 1
			"""
			cursor.execute(query,[artistName])
			rows = cursor.fetchall()

			if len(rows) <= 0:
				artistNotFoundWarning['text'] = 'Artist not found'
			else:
				#get the ArtistId
				artistId = rows[0][0]

				query = "UPDATE Artist SET Name = %s, lastModBy = %s WHERE ArtistId = %s"
				cursor.execute(query,[newArtistName,username,artistId])
				connection.commit()
				mainApp(username,isEmployee)
		else:
			newArtistNameWarning['text'] = 'Artist name already exists'
	else:
		artistNotFoundWarning['text'] = 'Information is missing'
		newArtistNameWarning['text'] = 'Information is missing'


def modAlbumPage(username,isEmployee):
	root.title('Modify Album')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	col1Xpos = 0.3
	col2Xpos = 0.5

	instruction1 = tk.Label(frame,text = 'Enter Album Title',fg='#ffffff',bg='#121212')
	instruction1.place(relx=col1Xpos,rely=0.27)
	albumTitleEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	albumTitleEntry.place(relx=col1Xpos,rely=0.3)

	global albumNotFoundWarning
	albumNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	albumNotFoundWarning.place(relx=col1Xpos,rely=0.35)

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.place(relx=col1Xpos,rely=0.42)
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.place(relx=col1Xpos,rely=0.45)

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.place(relx=col1Xpos,rely=0.50)

	instruction3 = tk.Label(frame,text = 'Enter New Album Title',fg='#ffffff',bg='#121212')
	instruction3.place(relx=col2Xpos,rely=0.27)
	newAlbumTitleEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	newAlbumTitleEntry.place(relx=col2Xpos,rely=0.3)

	global newAlbumWarning
	newAlbumWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	newAlbumWarning.place(relx=col2Xpos,rely=0.35)

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')

	spacer = tk.Label(frame,text='',font='Arial 160',bg='#121212')
	spacer.pack(side='bottom')

	modAlbumButton = tk.Button(frame,text='Change',command=lambda: modAlbum(username,isEmployee,albumTitleEntry.get(),artistNameEntry.get(),newAlbumTitleEntry.get()),width=15,height=2,fg='#575757')
	modAlbumButton.pack(side='bottom')

def modAlbum(username,isEmployee,albumTitle,artistName,newAlbumTitle):
	artistNotFoundWarning['text'] = ''
	albumNotFoundWarning['text'] = ''
	newAlbumWarning['text'] = ''
	
	if len(albumTitle) > 0 and len(artistName) > 0 and len(newAlbumTitle) > 0:
		query = """
		SELECT a.ArtistId
		FROM Artist a
		WHERE a.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[artistName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			artistNotFoundWarning['text'] = 'Artist not found'
		else:
			#get the ArtistId
			artistId = rows[0][0]

			query = """
			SELECT a.AlbumId
			FROM Album a
			WHERE a.ArtistId = %s AND a.Title = %s
			"""
			cursor.execute(query,[artistId,albumTitle])
			rows = cursor.fetchall()
			
			if len(rows) <= 0:
				albumNotFoundWarning['text'] = 'Album not found for artist'
			else:
				albumId = rows[0][0]

				query = "UPDATE Album SET Title = %s, lastModBy = %s WHERE AlbumId = %s AND ArtistId = %s"
				cursor.execute(query,[newAlbumTitle,username,albumId,artistId])
				connection.commit()
				mainApp(username,isEmployee)
	else:
		artistNotFoundWarning['text'] = 'Information is missing'
		albumNotFoundWarning['text'] = 'Information is missing'
		newAlbumWarning['text'] = 'Information is missing'


def selectTrackToModPage(username,isEmployee):
	root.title('Modify Track')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Track Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	trackNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	trackNameEntry.pack(side='top')

	global trackNotFoundWarning
	trackNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	trackNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	modTrackPageButton = tk.Button(frame,text='Continue',command=lambda: modTrackPage(username,isEmployee,trackNameEntry.get(),artistNameEntry.get()),width=15,height=2,fg='#575757')
	modTrackPageButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def modTrackPage(username,isEmployee,trackName,artistName):
	trackNotFoundWarning['text'] = ''
	artistNotFoundWarning['text'] = ''

	if len(trackName) > 0 and len(artistName) > 0:

		# CHECK IF TRACK NAME IS VALID
		query = """
		SELECT t.TrackId
		FROM Track t
		WHERE t.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[trackName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			trackNotFoundWarning['text'] = 'Track not found'
		else:

			# CHECK THE ARTIST MATCHES THE TRACK NAME
			query = """
			SELECT t.TrackId, t.Name, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice
			FROM Track t
			JOIN Album ON Album.AlbumId = t.AlbumId
			JOIN Artist ON Artist.ArtistId = Album.ArtistId
			WHERE Artist.Name = %s AND t.Name = %s
			"""
			cursor.execute(query,[artistName,trackName])
			rows = cursor.fetchall()

			if len(rows) <= 0:
				artistNotFoundWarning['text'] = 'Artist for track not found'
			else:
				trackId,trackName,trackComposer,trackMilliseconds,trackBytes,trackUnitPrice = rows[0]

				# All info is corret, so we preload the existing info in a new page
				root.title('Modify Track')

				global canvas
				canvas.destroy()
				canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
				canvas.pack()
				frame = tk.Frame(root,bg='#121212')
				frame.place(relx=0,rely=0,relwidth=1,relheight=1)

				# Soundic Logo
				logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
				logoLabel.place(relx=0.82,rely=0.01)
				if isEmployee:
					adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
					adminLabel.place(relx=0.935,rely=0.07)

				boxWidth = 0.28
				col1Xpos = 0.23

				trackComposer = '' if trackComposer == None else trackComposer
				trackBytes = '' if trackBytes == None else trackBytes
				

				# Col 1

				instruction1 = tk.Label(frame,text = 'Track Name *',fg='#ffffff',bg='#121212')
				instruction1.place(relx=col1Xpos,rely=0.1)
				trackNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
				trackNameEntry.place(relx=col1Xpos,rely=0.13,relwidth=boxWidth)
				trackNameEntry.insert(0,trackName)

				instruction2 = tk.Label(frame,text = 'Composer',fg='#ffffff',bg='#121212')
				instruction2.place(relx=col1Xpos,rely=0.2)
				composerEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
				composerEntry.place(relx=col1Xpos,rely=0.23,relwidth=boxWidth)
				composerEntry.insert(0,trackComposer)

				# Col 2

				instruction3 = tk.Label(frame,text = 'Milliseconds *',fg='#ffffff',bg='#121212')
				instruction3.place(relx=0.55,rely=0.1)
				millisecEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
				millisecEntry.place(relx=0.55,rely=0.13)
				millisecEntry.insert(0,trackMilliseconds)

				global millisecErrorWarning
				millisecErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
				millisecErrorWarning.place(relx=0.55,rely=0.17)

				instruction4 = tk.Label(frame,text = 'Bytes',fg='#ffffff',bg='#121212')
				instruction4.place(relx=0.55,rely=0.2)
				bytesEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
				bytesEntry.place(relx=0.55,rely=0.23)
				bytesEntry.insert(0,trackBytes)

				global bytesErrorWarning
				bytesErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
				bytesErrorWarning.place(relx=0.55,rely=0.27)

				instruction5 = tk.Label(frame,text = 'Enter Unit Price *',fg='#ffffff',bg='#121212')
				instruction5.place(relx=0.55,rely=0.3)
				unitPriceEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
				unitPriceEntry.place(relx=0.55,rely=0.33)
				unitPriceEntry.insert(0,trackUnitPrice)

				global unitPriceErrorWarning
				unitPriceErrorWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
				unitPriceErrorWarning.place(relx=0.55,rely=0.37)

				saveTrackButton = tk.Button(frame,text='Save',command=lambda: modTrack(username,isEmployee,trackId,trackNameEntry.get(),composerEntry.get(),millisecEntry.get(),bytesEntry.get(),unitPriceEntry.get()),width=15,height=2,fg='#575757')
				saveTrackButton.place(relx=0.55,rely=0.45)

				returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
				returnToAppButton.pack(side='bottom')
	else:
		trackNotFoundWarning['text'] = 'Some information is missing'
		artistNotFoundWarning['text'] = 'Some information is missing'


def modTrack(username,isEmployee,trackId,trackName,composer,millisec,bytes,unitPrice):
	millisecErrorWarning['text'] = ''
	bytesErrorWarning['text'] = ''
	unitPriceErrorWarning['text'] = ''

	composer = None if composer == '' else composer
	bytes = None if bytes == '' else bytes

	if len(trackName) > 0 and len(millisec) > 0 and len(unitPrice) > 0:

		if isInt(millisec):
			if isInt(bytes) or bytes == None:
				if isFloat(unitPrice):

					# EVERY ENTRY IS CORRECT, so we update the track
					query = "UPDATE Track SET Name = %s, Composer = %s, Milliseconds = %s, Bytes = %s, UnitPrice = %s, lastModBy = %s WHERE TrackId = %s"
					cursor.execute(query,[trackName,composer,millisec,bytes,unitPrice,username,trackId])
					connection.commit()

					mainApp(username,isEmployee)

				else:
					unitPriceErrorWarning['text'] = 'Unit price must be a number'
			else:
				bytesErrorWarning['text'] = 'Bytes must be an integer'
		else:
			millisecErrorWarning['text'] = 'Millisecongs must be an integer'
	else:
		millisecErrorWarning['text'] = '*Required informacion is missing'
		bytesErrorWarning['text'] = '*Required informacion is missing'
		unitPriceErrorWarning['text'] = '*Required informacion is missing'


def deletePage(username,isEmployee):
	root.title('Delete')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Delete',font='Arial 41 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')
	spacer1 = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacer1.pack(side='top')

	delArtistButton = tk.Button(frame,text='Artist',command=lambda: delArtist(username,isEmployee),width=20,height=2,fg='#575757')
	delArtistButton.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer2.pack(side='top')

	delAlbumButton = tk.Button(frame,text='Album',command=lambda: delAlbum(username,isEmployee),width=20,height=2,fg='#575757')
	delAlbumButton.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer3.pack(side='top')

	delTrackButton = tk.Button(frame,text='Track',command=lambda: delTrack(username,isEmployee),width=20,height=2,fg='#575757')
	delTrackButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',borderwidth=0, highlightthickness=0,command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def delArtist(username,isEmployee):
	root.title('Delete Artist')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	delArtistButton = tk.Button(frame,text='Delete',command=lambda: deleteArtist(username,isEmployee,artistNameEntry.get()),width=15,height=2,fg='#575757')
	delArtistButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def deleteArtist(username,isEmployee,artistName):
	artistNotFoundWarning['text'] = ''
	
	if len(artistName) > 0:

		query = """
		SELECT a.ArtistId
		FROM Artist a
		WHERE a.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[artistName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			artistNotFoundWarning['text'] = 'Artist not found'
		else:
			#get the ArtistId
			artistId = rows[0][0]

			query = "SELECT * FROM registerDelete(%s,%s,%s);"
			cursor.execute(query,[artistId,username,'artist'])
			query = "DELETE FROM Artist WHERE ArtistId = %s"
			cursor.execute(query,[artistId])
			connection.commit()
			mainApp(username,isEmployee)
	else:
		artistNotFoundWarning['text'] = 'Information is missing'


def delAlbum(username,isEmployee):
	root.title('Delete Album')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Album Title',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	albumTitleEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	albumTitleEntry.pack(side='top')

	global albumNotFoundWarning
	albumNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	albumNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	delAlbumButton = tk.Button(frame,text='Delete',command=lambda: deleteAlbum(username,isEmployee,albumTitleEntry.get(),artistNameEntry.get()),width=15,height=2,fg='#575757')
	delAlbumButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def deleteAlbum(username,isEmployee,albumTitle,artistName):
	albumNotFoundWarning['text'] = ''
	artistNotFoundWarning['text'] = ''

	if len(albumTitle) > 0 and len(artistName) > 0:

		query = """
		SELECT a.ArtistId
		FROM Artist a
		WHERE a.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[artistName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			artistNotFoundWarning['text'] = 'Artist not found'
		else:
			#get the ArtistId
			artistId = rows[0][0]

			query = """
			SELECT a.AlbumId
			FROM Album a
			WHERE a.ArtistId = %s AND a.Title = %s
			LIMIT 1
			"""
			cursor.execute(query,[artistId,albumTitle])
			rows = cursor.fetchall()
			
			if len(rows) <= 0:
				albumNotFoundWarning['text'] = 'Album not found'
			else:
				albumId = rows[0][0]

				query = "SELECT * FROM registerDelete(%s,%s,%s);"
				cursor.execute(query,[albumId,username,'album'])
				query = "DELETE FROM Album WHERE AlbumId = %s"
				cursor.execute(query,[albumId])
				connection.commit()
				mainApp(username,isEmployee)
	else:
		albumNotFoundWarning['text'] = 'Some information is missing'
		artistNotFoundWarning['text'] = 'Some information is missing'


def delTrack(username,isEmployee):
	root.title('Delete Track')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Track Name',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	trackNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	trackNameEntry.pack(side='top')

	global trackNotFoundWarning
	trackNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	trackNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Artist Name',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	artistNameEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	artistNameEntry.pack(side='top')

	global artistNotFoundWarning
	artistNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	artistNotFoundWarning.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer3.pack(side='top')

	delTrackButton = tk.Button(frame,text='Delete',command=lambda: deleteTrack(username,isEmployee,trackNameEntry.get(),artistNameEntry.get()),width=15,height=2,fg='#575757')
	delTrackButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def deleteTrack(username,isEmployee,trackName,artistName):
	trackNotFoundWarning['text'] = ''
	artistNotFoundWarning['text'] = ''

	if len(trackName) > 0 and len(artistName) > 0:

		# CHECK IF TRACK NAME IS VALID
		query = """
		SELECT t.TrackId
		FROM Track t
		WHERE t.Name = %s
		LIMIT 1
		"""
		cursor.execute(query,[trackName])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			trackNotFoundWarning['text'] = 'Track not found'
		else:

			# CHECK THE ARTIST MATCHES THE TRACK NAME
			query = """
			SELECT Track.TrackId
			FROM Track 
			JOIN Album ON Album.AlbumId = Track.AlbumId
			JOIN Artist ON Artist.ArtistId = Album.ArtistId
			WHERE Artist.Name = %s AND Track.Name = %s
			"""
			cursor.execute(query,[artistName,trackName])
			rows = cursor.fetchall()

			if len(rows) <= 0:
				artistNotFoundWarning['text'] = 'Artist for track not found'
			else:
				trackId = rows[0][0]

				query = "SELECT * FROM registerDelete(%s,%s,%s);"
				cursor.execute(query,[trackId,username,'track'])
				query = "DELETE FROM Track WHERE TrackId = %s"
				cursor.execute(query,[trackId])
				connection.commit()
				mainApp(username,isEmployee)
	else:
		trackNotFoundWarning['text'] = 'Some information is missing'
		artistNotFoundWarning['text'] = 'Some information is missing'


def statsPage(username,isEmployee):
	root.title('Soundic Stats')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Statistics',font='Arial 40 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')

	# Extended Stats
	extendedStatsButton = tk.Button(frame,image=nextPageIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: displayExtendedStatsPage(username,isEmployee))
	extendedStatsButton.place(relx=0.9,rely=0.9,relwidth=0.024,relheight=0.042)
	eSLabel = tk.Label(frame,text='Extended Stats',font='Arial 15 bold',bg='#121212',fg='#ffffff')
	eSLabel.place(relx=0.8,rely=0.9)

	# Col 1
	title1 = 'Artists with the most albums'
	stats1Button = tk.Button(frame,text=title1,command=lambda: displayStats(username,isEmployee,1,title1),width=40,height=2,fg='#575757')
	stats1Button.place(relx=0.1,rely=0.2)

	title2 = 'Genres with the most tracks'
	stats2Button = tk.Button(frame,text=title2,command=lambda: displayStats(username,isEmployee,2,title2),width=40,height=2,fg='#575757')
	stats2Button.place(relx=0.1,rely=0.35)

	title3 = 'Playlist duration'
	stats3Button = tk.Button(frame,text=title3,command=lambda: displayStats(username,isEmployee,3,title3),width=40,height=2,fg='#575757')
	stats3Button.place(relx=0.1,rely=0.5)

	title4 = 'Longest tracks'
	stats4Button = tk.Button(frame,text=title4,command=lambda: displayStats(username,isEmployee,4,title4),width=40,height=2,fg='#575757')
	stats4Button.place(relx=0.1,rely=0.65)

	title9 = 'Most used Media Type'
	stats9Button = tk.Button(frame,text=title9,command=lambda: displayStats(username,isEmployee,9,title9),width=40,height=2,fg='#575757')
	stats9Button.place(relx=0.1,rely=0.8)

	# Col 2
	title5 = 'Users with the most registered tracks'
	stats5Button = tk.Button(frame,text=title5,command=lambda: displayStats(username,isEmployee,5,title5),width=40,height=2,fg='#575757')
	stats5Button.place(relx=0.6,rely=0.2)

	title6 = 'Average track duration per genre'
	stats6Button = tk.Button(frame,text=title6,command=lambda: displayStats(username,isEmployee,6,title6),width=40,height=2,fg='#575757')
	stats6Button.place(relx=0.6,rely=0.35)

	title7 = 'Different Artists per Playlist'
	stats7Button = tk.Button(frame,text=title7,command=lambda: displayStats(username,isEmployee,7,title7),width=40,height=2,fg='#575757')
	stats7Button.place(relx=0.6,rely=0.5)

	title8 = 'Most diverse artists'
	stats8Button = tk.Button(frame,text=title8,command=lambda: displayStats(username,isEmployee,8,title8),width=40,height=2,fg='#575757')
	stats8Button.place(relx=0.6,rely=0.65)

	title10 = 'Countries that buy the most'
	stats10Button = tk.Button(frame,text=title10,command=lambda: displayStats(username,isEmployee,10,title10),width=40,height=2,fg='#575757')
	stats10Button.place(relx=0.6,rely=0.8)

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def displayStats(username,isEmployee,num,title):
	root.title('Soundic Statistics')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer1.pack(side='top')

	titleLabel = tk.Label(frame,text=title,font='Arial 25 bold',bg='#121212',fg='white')
	titleLabel.pack(side='top')

	global statsTable

	if num == 1:
		statsTable = MultiColumnListbox(frame,['Artist','Album Count'])
		query = 'SELECT * FROM stats1'
	if num == 2:
		statsTable = MultiColumnListbox(frame,['Genre','Track Count'])
		query = 'SELECT * FROM stats2'
	if num == 3:
		statsTable = MultiColumnListbox(frame,['Playlist','Duration (min)'])
		query = 'SELECT * FROM stats3'
	if num == 4:
		statsTable = MultiColumnListbox(frame,['Track','Artist','Duration (min)'])
		query = 'SELECT * FROM stats4'
	if num == 5:
		statsTable = MultiColumnListbox(frame,['First Name','Last Name','Tracks Registered'])
		query = 'SELECT * FROM stats5'
	if num == 6:
		statsTable = MultiColumnListbox(frame,['Genre','Average (min)'])
		query = 'SELECT * FROM stats6'
	if num == 7:
		statsTable = MultiColumnListbox(frame,['Playlist','Artist Count'])
		query = 'SELECT * FROM stats7'
	if num == 8:
		statsTable = MultiColumnListbox(frame,['Artist','Genre Count'])
		query = 'SELECT * FROM stats8'
	if num == 9:
		statsTable = MultiColumnListbox(frame,['Media Type','Count'])
		query = 'SELECT * FROM stats9'
	if num == 10:
		statsTable = MultiColumnListbox(frame,['Billing Country','Purchases'])
		query = 'SELECT * FROM stats10'
	cursor.execute(query)
	rows = cursor.fetchall()
	statsTable.updateData(rows)
		
	returnToStatsButton = tk.Button(frame,text='Return to Statistics',fg='#575757',command=lambda: statsPage(username,isEmployee))
	returnToStatsButton.pack(side='bottom')


def displayExtendedStatsPage(username,isEmployee):
	root.title('Soundic Extended Statistics')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Extended Statistics',font='Arial 40 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')

	stats1Button = tk.Button(frame,text='Weekly Sales',command=lambda: extendedStatsInputPage(username,isEmployee,1),width=40,height=2,fg='#575757')
	stats1Button.place(relx=0.1,rely=0.2)

	stats2Button = tk.Button(frame,text='Artists With the Most Sales',command=lambda: extendedStatsInputPage(username,isEmployee,2),width=40,height=2,fg='#575757')
	stats2Button.place(relx=0.1,rely=0.4)

	stats3Button = tk.Button(frame,text='Genre Sales',command=lambda: extendedStatsInputPage(username,isEmployee,3),width=40,height=2,fg='#575757')
	stats3Button.place(relx=0.6,rely=0.2)

	stats4Button = tk.Button(frame,text='Most Played Tracks by an Artist',command=lambda: extendedStatsInputPage(username,isEmployee,4),width=40,height=2,fg='#575757')
	stats4Button.place(relx=0.6,rely=0.4)

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def extendedStatsInputPage(username,isEmployee,statid):
	root.title('Soundic Extended Statistics')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	instruction1 = tk.Label(frame,text = 'Start Date (YYYY/MM/dd)',fg='#ffffff',bg='#121212')
	entry1 = tk.Entry(frame,fg='#ffffff',bg='#171717')

	spacer2 = tk.Label(frame,text='',font='Arial 25',bg='#121212')
	instruction2 = tk.Label(frame,text = 'End Date (YYYY/MM/dd)',fg='#ffffff',bg='#121212')
	entry2 = tk.Entry(frame,fg='#ffffff',bg='#171717')

	spacer3 = tk.Label(frame,text='',font='Arial 25',bg='#121212')
	instruction3 = tk.Label(frame,text = 'Artist amount',fg='#ffffff',bg='#121212')
	entry3 = tk.Entry(frame,fg='#ffffff',bg='#171717')

	spacer4 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	instruction4 = tk.Label(frame,text = 'Artist name',fg='#ffffff',bg='#121212')
	entry4 = tk.Entry(frame,fg='#ffffff',bg='#171717')

	if statid in [1,2,3]:
		spacer1.pack(side='top')
		instruction1.pack(side='top')
		entry1.pack(side='top')

		spacer2.pack(side='top')
		instruction2.pack(side='top')
		entry2.pack(side='top')

	if statid == 2:
		spacer3.pack(side='top')
		instruction3.pack(side='top')
		entry3.pack(side='top')

	if statid == 4:
		spacer4.pack(side='top')
		instruction4.pack(side='top')
		entry4.pack(side='top')

		spacer3 = tk.Label(frame,text='',font='Arial 25',bg='#121212')
		instruction3 = tk.Label(frame,text = 'Song amount',fg='#ffffff',bg='#121212')
		entry3 = tk.Entry(frame,fg='#ffffff',bg='#171717')
		spacer3.pack(side='top')
		instruction3.pack(side='top')
		entry3.pack(side='top')

	spacerF = tk.Label(frame,text='',font='Arial 25',bg='#121212')
	spacerF.pack(side='top')

	goButton = tk.Button(frame,text='Go',command=lambda: displayExtendedStats(username,isEmployee,statid,entry1.get(),entry2.get(),entry3.get(),entry4.get()),width=15,height=2,fg='#575757')
	goButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to Extended Stats',fg='#575757',command=lambda: displayExtendedStatsPage(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def displayExtendedStats(username,isEmployee,statid,dateStart=None,dateEnd=None,n=None,artistName=None):
	root.title('Soundic Extended Statistics')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer1.pack(side='top')

	global statsTable

	if statid == 1:
		title = 'Weekly Sales'
		cols = ['Year-Week','Sales','Total ($)']
		statsTable = MultiColumnListbox(frame,cols)
		query = 'SELECT * FROM SalesWeek(%s,%s)'
		cursor.execute(query,[dateStart,dateEnd])
	if statid == 2:
		title = 'Top ' + n + ' Artists With the Most Sales'
		cols = ['Artist ID','Name','Sales']
		statsTable = MultiColumnListbox(frame,cols)
		query = 'SELECT * FROM ArtistRange(%s,%s,%s)'
		cursor.execute(query,[dateStart,dateEnd,n])
	if statid == 3:
		title = 'Genre Sales'
		cols = ['Genre ID','Genre','Sales']
		statsTable = MultiColumnListbox(frame,cols)
		query = 'SELECT * FROM GenreRange(%s,%s)'
		cursor.execute(query,[dateStart,dateEnd])
	if statid == 4:
		title = 'Most Played Tracks by an Artist'
		cols = ['Artist','Track','Plays']
		statsTable = MultiColumnListbox(frame,cols)
		query = 'SELECT * FROM ArtistPlays(%s,%s)'
		cursor.execute(query,[artistName,n])

	rows = cursor.fetchall()
	statsTable.updateData(rows)

	titleLabel = tk.Label(frame,text=title,font='Arial 25 bold',bg='#121212',fg='white')
	titleLabel.pack(side='top')

	exportButton = tk.Button(frame,image=exportIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: export(rows,cols))
	exportButton.place(relx=0.05,rely=0.02,relwidth=0.025,relheight=0.042)
		
	returnToStatsButton = tk.Button(frame,text='Return to Statistics',fg='#575757',command=lambda: statsPage(username,isEmployee))
	returnToStatsButton.pack(side='bottom')


def export(rows,colTitles):
	with open('stats-export.csv', mode='w') as file:
		file = csv.writer(file, delimiter=',')
		file.writerow(colTitles)
		for row in rows:
			file.writerow(row)


def displayBitacora(username,isEmployee):
	root.title('Soundic Binnacle')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer1.pack(side='top')

	titleLabel = tk.Label(frame,text='Operations Binnacle',font='Arial 25 bold',bg='#121212',fg='white')
	titleLabel.pack(side='top')

	bitacoraTable = MultiColumnListbox(frame,['Date', 'Operation', 'Item Type', 'Item ID', 'Username', 'Name'])

	cursor.execute('SELECT * FROM BitacoraView')
	rows = cursor.fetchall()
	bitacoraTable.updateData(rows)
		
	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def simulationPage(username,isEmployee):
	root.title('Soundic Simulation')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	spacerTop = tk.Label(frame,text='',font='Arial 70',bg='#121212')
	spacerTop.pack(side='top')

	titleLabel = tk.Label(frame,text='Sales & Plays Simulation',font='Arial 25 bold',bg='#121212',fg='white')
	titleLabel.pack(side='top')

	spacer1 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Amount of Invoices',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	invoiceAmountEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	invoiceAmountEntry.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 10',bg='#121212')
	spacer2.pack(side='top')

	instruction2 = tk.Label(frame,text = 'Enter Year',fg='#ffffff',bg='#121212')
	instruction2.pack(side='top')
	yearEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	yearEntry.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 10',bg='#121212')
	spacer3.pack(side='top')

	instruction3 = tk.Label(frame,text = 'Enter Month',fg='#ffffff',bg='#121212')
	instruction3.pack(side='top')
	monthEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	monthEntry.pack(side='top')

	spacer4 = tk.Label(frame,text='',font='Arial 10',bg='#121212')
	spacer4.pack(side='top')

	instruction4 = tk.Label(frame,text = 'Enter Day',fg='#ffffff',bg='#121212')
	instruction4.pack(side='top')
	dayEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	dayEntry.pack(side='top')

	spacer5 = tk.Label(frame,text='',font='Arial 20',bg='#121212')
	spacer5.pack(side='top')

	simulateButton = tk.Button(frame,text='Simulate',command=lambda: simulateSales(username,isEmployee,invoiceAmountEntry.get(),yearEntry.get(),monthEntry.get(),dayEntry.get()),width=15,height=2,fg='#575757')
	simulateButton.pack(side='top')
		
	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def simulateSales(username,isEmployee,invociesToSimulate,year,month,day):

	if isInt(invociesToSimulate) and isInt(year) and isInt(month) and isInt(day):

		try:

			invociesToSimulate = int(invociesToSimulate)

			# General
			countries = ['Suriname', 'Uruguay', 'Gambia', 'Malawi', 'Central African Republic', 'Burundi', 'Mongolia', 'Afghanistan', 'Anguilla', 'Mexico', 'United Arab Emirates', 'Bangladesh', 'Sierra Leone', 'British Virgin Islands', 'Nigeria', 'Yemen', 'Algeria', 'Samoa', 'United States Minor Outlying Islands', 'French Polynesia', 'Saint Lucia', 'Zambia', 'Sudan', 'Belize', 'French Southern Territories', 'Fiji', 'Korea', 'Uzbekistan', 'Saint Helena', 'Anguilla', 'Timor-Leste', 'Sweden', 'Wallis and Futuna', 'Bulgaria', 'Guatemala', 'Papua New Guinea', 'Belgium', 'Isle of Man', 'Switzerland', 'Nigeria', 'Saint Pierre and Miquelon', 'French Guiana', 'Seychelles', 'Mali', 'Qatar', 'Saudi Arabia', "Lao People's Democratic Republic", 'Suriname', 'Timor-Leste', 'Guernsey', 'Tokelau', 'Mexico', 'Mayotte', 'Oman', 'British Virgin Islands', 'Canada', 'India', 'Grenada', 'Haiti', 'Macao', "Lao People's Democratic Republic", 'Zambia', 'Turkey', 'Saint Pierre and Miquelon', 'Tonga', 'Lebanon', 'American Samoa', 'El Salvador', 'Netherlands Antilles', 'Guinea', 'Dominica', 'Nauru', 'Philippines', 'Namibia', 'Vietnam', 'Sao Tome and Principe', 'Timor-Leste', 'United States Minor Outlying Islands', 'Nigeria', 'Isle of Man', 'Colombia', 'Antigua and Barbuda', 'Greenland', 'Albania', 'Svalbard & Jan Mayen Islands', 'American Samoa', 'Guinea-Bissau', 'French Guiana', 'French Southern Territories', 'Papua New Guinea', 'Kuwait', 'Mexico', 'Angola', 'Marshall Islands', 'Syrian Arab Republic', 'Cambodia', 'Indonesia', 'Tonga', 'Monaco', 'Bouvet Island (Bouvetoya)', 'Finland', 'Central African Republic', 'United States of America', 'Liberia', 'Saint Lucia', 'Ghana', 'Nicaragua', 'Micronesia', 'Reunion', 'Egypt', 'French Southern Territories', 'Pakistan', 'Saudi Arabia', 'Palestinian Territory', 'Portugal', 'Nicaragua', 'Nepal', 'Paraguay', 'Israel', 'Isle of Man', 'Cameroon', 'Grenada', 'Holy See (Vatican City State)', 'Holy See (Vatican City State)', 'Botswana', 'Singapore', "Lao People's Democratic Republic", 'Kazakhstan', 'Luxembourg', 'Austria', 'Micronesia', 'Mauritania', 'Maldives', 'Niger', 'Malta', 'Kiribati', 'Thailand', 'Lebanon', 'Venezuela', 'Finland', "Lao People's Democratic Republic", 'Colombia', 'Suriname', 'Belize', 'Djibouti', 'Equatorial Guinea', 'Lithuania', 'Heard Island and McDonald Islands', 'Bolivia', 'Nepal', 'Guyana', 'Cook Islands', 'Portugal', 'Kuwait', 'Falkland Islands (Malvinas)', 'Peru', 'Mali', 'Mozambique', 'Venezuela', 'French Guiana', 'Uzbekistan', 'Saint Lucia', 'New Caledonia', 'Reunion', 'Korea', 'Brazil', 'Bangladesh', 'United States Minor Outlying Islands', 'Solomon Islands', 'New Caledonia', 'Singapore', 'Qatar', 'Greenland', 'Tokelau', 'Cameroon', 'Belarus', 'Zambia', 'Norway', 'Chile', 'Monaco', 'Somalia', 'Niue', 'Luxembourg', 'Sao Tome and Principe', 'Saint Pierre and Miquelon', 'Guinea', 'Eritrea', 'Serbia', 'El Salvador', 'Morocco', 'Kenya', 'Iran', 'Gibraltar', 'Sierra Leone', 'Central African Republic', 'Gibraltar', 'Spain', 'Bulgaria', 'Afghanistan']

			trackIds = []
			cursor.execute('SELECT TrackId FROM Track')
			rows = cursor.fetchall()
			for id in rows:
				trackIds.append(id)

			# Maxes
			cursor.execute('SELECT MAX(CustomerId) FROM Customer')
			rows = cursor.fetchall()
			maxCustomerId = rows[0][0]

			cursor.execute('SELECT MAX(InvoiceLineId) FROM InvoiceLine')
			rows = cursor.fetchall()
			invoiceLineId = rows[0][0]

			cursor.execute('SELECT MAX(InvoiceId) FROM Invoice')
			rows = cursor.fetchall()
			invoiceId = rows[0][0]

			for i in range(invociesToSimulate):

				invoiceLinesToSimulate = random.randint(1,3)

				simInvoiceLineIds = []
				simTrackIds = []
				simUnitPrices = []
				simQuantities = []

				for i in range(invoiceLinesToSimulate):
					invoiceLineId += 1
					simInvoiceLineIds.append(invoiceLineId)

					# Random TrackId
					simTrackIds.append(random.choice(trackIds))

					# Unit Price
					query = 'SELECT unitPrice FROM track WHERE TrackId = %s'
					cursor.execute(query,[simTrackIds[i]])
					rows = cursor.fetchall()
					simUnitPrices.append(rows[0][0])

					# Random Quantity
					simQuantities.append(random.randint(1,3))

				invoiceId += 1

				# Random CustomerId
				randomCustomerId = random.randint(1,maxCustomerId)

				# Random Date
				date = str(year) + '/' + str(month) + '/' + str(day)

				# Random Country
				randomCountry = random.choice(countries)

				# Random Postal Code
				randomPostalCode = random.randint(10000,99999)

				# Total
				total = 0.0
				for i in range(len(simUnitPrices)):
					total += float(simUnitPrices[i]) * float(simQuantities[i])

				# Insert changes & commit
				query = 'INSERT INTO Invoice (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingCountry, BillingPostalCode, Total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
				cursor.execute(query,[invoiceId,randomCustomerId,date,None,None,randomCountry,randomPostalCode,total])
				connection.commit()

				for i in range(invoiceLinesToSimulate):
					query = 'INSERT INTO InvoiceLine (InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity) VALUES (%s,%s,%s,%s,%s)'
					cursor.execute(query,[simInvoiceLineIds[i],invoiceId,simTrackIds[i],simUnitPrices[i],simQuantities[i]])
					
					# Simulate Plays for the songs bought
					randomPlays = random.randint(1,10)
					for x in range(randomPlays):
						cursor.execute('SELECT * from playTrack(%s,%s)',[randomCustomerId,simTrackIds[i]])
						
					connection.commit()

			messagebox.showinfo('Simulation', "Simulation ended successfuly")

			mainApp(username,isEmployee)
		except:
			messagebox.showerror("Error", "A problem occured while simulating")


def search(entry,export):

	entry = str(entry)

	if len(entry) > 0:

		# We search in each all tables and unify de result
		# searches are combined and displayed in the table for the user

		query = """
		SELECT r.trackName, r.artistName, r.Kind, r.albumTitle, r.genreName
		FROM (
			SELECT Track.Active AS Active,Track.Name AS trackName,Artist.Name AS artistName,MediaType.Name AS Kind,Album.Title AS albumTitle,Genre.Name AS genreName FROM Track JOIN Album ON Album.AlbumId = Track.AlbumId JOIN Artist ON Artist.ArtistId = Album.ArtistId JOIN Genre ON Genre.GenreId = Track.GenreId JOIN MediaType ON MediaType.MediaTypeId = Track.MediaTypeId WHERE Track.Name = %s
			UNION
			SELECT Track.Active AS Active,Track.Name AS trackName,Artist.Name AS artistName,MediaType.Name AS Kind,Album.Title AS albumTitle,Genre.Name AS genreName FROM Track JOIN Album ON Album.AlbumId = Track.AlbumId JOIN Artist ON Artist.ArtistId = Album.ArtistId JOIN Genre ON Genre.GenreId = Track.GenreId JOIN MediaType ON MediaType.MediaTypeId = Track.MediaTypeId WHERE Artist.Name = %s
			UNION
			SELECT Track.Active AS Active,Track.Name AS trackName,Artist.Name AS artistName,MediaType.Name AS Kind,Album.Title AS albumTitle,Genre.Name AS genreName FROM Track JOIN Album ON Album.AlbumId = Track.AlbumId JOIN Artist ON Artist.ArtistId = Album.ArtistId JOIN Genre ON Genre.GenreId = Track.GenreId JOIN MediaType ON MediaType.MediaTypeId = Track.MediaTypeId WHERE Album.Title = %s
			UNION
			SELECT Track.Active AS Active,Track.Name AS trackName,Artist.Name AS artistName,MediaType.Name AS Kind,Album.Title AS albumTitle,Genre.Name AS genreName FROM Track JOIN Album ON Album.AlbumId = Track.AlbumId JOIN Artist ON Artist.ArtistId = Album.ArtistId JOIN Genre ON Genre.GenreId = Track.GenreId JOIN MediaType ON MediaType.MediaTypeId = Track.MediaTypeId WHERE Genre.Name = %s
		) r
		WHERE r.Active = true
		"""
		cursor.execute(query,[entry,entry,entry,entry])
		rowsSearch = cursor.fetchall()

		if export:
			with open('search-export.csv', mode='w') as file:
				file = csv.writer(file, delimiter=',')

				file.writerow(('Track','Artist','Kind','Album','Genre'))

				for row in rowsSearch:
					file.writerow(row)

		outputTable.updateData(rowsSearch)




def requestCustomerId(username):
	root.title('Manage Users')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
	adminLabel.place(relx=0.935,rely=0.07)

	spacer1 = tk.Label(frame,text='',font='Arial 175',bg='#121212')
	spacer1.pack(side='top')

	instruction1 = tk.Label(frame,text = 'Enter Customer ID',fg='#ffffff',bg='#121212')
	instruction1.pack(side='top')
	customerIdEntry = tk.Entry(frame,fg='#ffffff',bg='#171717')
	customerIdEntry.pack(side='top')

	global customerNotFoundWarning
	customerNotFoundWarning = tk.Label(frame,text='',font='Arial 10',bg='#121212',fg='#e74c3c')
	customerNotFoundWarning.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacer2.pack(side='top')

	continueButton = tk.Button(frame,text='Continue',command=lambda: validateCustomerId(username,customerIdEntry.get()),width=15,height=2,fg='#575757')
	continueButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',borderwidth=0, highlightthickness=0,command=lambda: mainApp(username,isEmployee=True))
	returnToAppButton.pack(side='bottom')


def validateCustomerId(username,customerid):
	customerNotFoundWarning['text'] = ''

	if len(customerid) > 0:
		# CHECK IF TRACK NAME IS VALID
		query = """
		SELECT c.firstName,c.LastName
		FROM Customer c
		WHERE c.CustomerId = %s
		LIMIT 1
		"""
		cursor.execute(query,[customerid])
		rows = cursor.fetchall()

		if len(rows) <= 0:
			customerNotFoundWarning['text'] = 'Customer not found'
		else:
			# customer found, show allow options window
			firstname = rows[0][0]
			lastname = rows[0][1]
			showManageUsersOptions(username,customerid,firstname,lastname)
	else:
		customerNotFoundWarning['text'] = 'Some information is missing'


def showManageUsersOptions(username,customerid,firstname,lastname):
	root.title('Manage Users')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
	adminLabel.place(relx=0.935,rely=0.07)
	
	spacerTop = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacerTop.pack(side='top')
	pageTitleLabel = tk.Label(frame,text='Allow '+firstname+' '+lastname+' to:',font='Arial 30 bold',bg='#121212',fg='white')
	pageTitleLabel.pack(side='top')
	spacer1 = tk.Label(frame,text='',font='Arial 67',bg='#121212')
	spacer1.pack(side='top')

	allowInactivateButton = tk.Button(frame,text='Inactivate',command=lambda: allowInactivate(username,customerid),width=20,height=2,fg='#575757')
	allowInactivateButton.pack(side='top')

	spacer2 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer2.pack(side='top')

	allowModifyButton = tk.Button(frame,text='Modify',command=lambda: allowModify(username,customerid),width=20,height=2,fg='#575757')
	allowModifyButton.pack(side='top')

	spacer3 = tk.Label(frame,text='',font='Arial 50',bg='#121212')
	spacer3.pack(side='top')

	allowDeleteButton = tk.Button(frame,text='Delete',command=lambda: allowDelete(username,customerid),width=20,height=2,fg='#575757')
	allowDeleteButton.pack(side='top')

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',borderwidth=0, highlightthickness=0,command=lambda: mainApp(username,isEmployee=True))
	returnToAppButton.pack(side='bottom')


def playPage(username,isEmployee):
	root.title('Soundic Play')

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	tracksTable = MultiColumnListbox(frame,['Track','Artist','Kind','Album','Genre'])

	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)

	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

		cursor.execute('SELECT track.name,artist.name,mediaType.name,album.title,genre.name FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON artist.artistid = album.artistid JOIN genre ON genre.genreid = track.genreid JOIN mediatype ON mediatype.mediatypeid = track.mediatypeid')
	else:
		cursor.execute("SELECT track.name,artist.name,mediaType.name,album.title,genre.name FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON artist.artistid = album.artistid JOIN genre ON genre.genreid = track.genreid JOIN mediatype ON mediatype.mediatypeid = track.mediatypeid JOIN (SELECT x.trackid FROM (SELECT itemid as trackid,username FROM bitacora WHERE itemtype = 'track' UNION SELECT track.trackid,customer.username FROM invoice JOIN invoiceline ON invoiceline.invoiceid = invoice.invoiceid JOIN customer ON invoice.customerid = customer.customerid JOIN track ON track.trackid = invoiceline.trackid) x WHERE x.username = %s) r ON r.trackid = track.trackid",[username])
	
	rows = cursor.fetchall()
	tracksTable.updateData(rows)

	# Play Button
	playButton = tk.Button(frame,image=playIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: playTrack(username,isEmployee,tracksTable.getSelection()))
	playButton.place(relx=0.48,rely=0.02,relwidth=0.025,relheight=0.042)

	# Decorative Buttons
	prevButton = tk.Button(frame,image=playPrevIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	prevButton.place(relx=0.38,rely=0.02,relwidth=0.025,relheight=0.042)
	nextButton = tk.Button(frame,image=playNextIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	nextButton.place(relx=0.58,rely=0.02,relwidth=0.024,relheight=0.042)
		
	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def playSong(artist, song):
	try:
	    query = str(artist) +" "+ str(song)
	    query_string = urllib.parse.urlencode({"search_query" : query})
	    html_content = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
	    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	    wb.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))
	except:
		messagebox.showerror('Error', "An error occured during song loading, try again later.")


def playTrack(username,isEmployee,selection):

	if selection != None:
		trackName = selection[0]
		artistName = selection[1]
		albumName = selection[3]

		if not isEmployee:
			query = 'SELECT track.trackid, (SELECT customerid FROM customer WHERE customer.username = %s) FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON artist.artistid = album.artistid WHERE track.name = %s AND artist.name = %s AND album.title = %s'
			cursor.execute(query,[username,trackName,artistName,albumName])
			rows = cursor.fetchall()
			
			playTrackId = rows[0][0]
			playCustomerId = rows[0][1]

			cursor.execute('SELECT * from playTrack(%s,%s)',[playCustomerId,playTrackId])
			connection.commit()

		playSong(artistName,trackName)


def shopPage(username,isEmployee):
	root.title('Soundic Shop')

	# Canvas setup
	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	spacerTop = tk.Label(frame,text='',font='Arial 15',bg='#121212')
	spacerTop.pack(side='top')

	titleLabel = tk.Label(frame,text='Soundic Shop',font='Arial 25 bold',bg='#121212',fg='white')
	titleLabel.pack(side='top')

	global cart
	cart = []

	# Search text field
	searchEntry = tk.Entry(frame,text='Search',fg='#ffffff',bg='#171717')
	searchEntry.place(relx=0.005,rely=0.01,relwidth=0.2,relheight=0.05)

	# Search Button
	searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get(),export=False))
	searchButton.place(relx=0.215,rely=0.015,relwidth=0.025,relheight=0.042)

	global outputTable
	outputTable = MultiColumnListbox(frame,['Track','Artist','Kind','Album','Genre'])

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	global countLabel
	countLabel = tk.Label(frame,text='0',font='Arial 50 bold',bg='#121212',fg='white')
	countLabel.place(relx=0.925,rely=0.125)

	songsLabel = tk.Label(frame,text='Cart',font='Arial 25 bold',bg='#121212',fg='white')
	songsLabel.place(relx=0.908,rely=0.22)

	addButton = tk.Button(frame,text='Add to Cart',command=lambda: addToCart(outputTable.getSelection()),width=10,height=2,fg='#575757')
	addButton.place(relx=0.9,rely=0.3)

	clearButton = tk.Button(frame,text='Clear Cart',command=lambda: clearCart(),width=10,height=2,fg='#575757')
	clearButton.place(relx=0.9,rely=0.4)

	checkOutButton = tk.Button(frame,text='Check Out',command=lambda: checkOut(username,isEmployee,cart),width=10,height=2,fg='#575757')
	checkOutButton.place(relx=0.9,rely=0.5)

	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')

def addToCart(selection):
	if selection != None:
		query = 'SELECT track.trackid  FROM Track JOIN Album ON Album.AlbumId = Track.AlbumId JOIN Artist ON Artist.ArtistId = Album.ArtistId WHERE Track.Name = %s AND Artist.name = %s AND Album.title = %s'
		cursor.execute(query,[selection[0],selection[1],selection[3]])
		rows = cursor.fetchall()
		cart.append(rows[0][0])
		countLabel['text'] = str(len(cart))

def clearCart():
	global cart
	cart = []
	countLabel['text'] = '0'
	messagebox.showinfo('Soundic Shop', "Shopping cart cleared!")

def checkOut(username,isEmployee,cart):

	if not isEmployee:
		try:
			prices = []

			for i in cart:
				query='SELECT t.UnitPrice::float FROM Track t WHERE t.TrackId=%s'
				cursor.execute(query,[i])
				rows = cursor.fetchall()
				prices.append(rows[0][0])

			total = sum(prices)

			query = ''' 
				INSERT INTO Invoice VALUES (
		            (SELECT i.InvoiceId FROM Invoice i ORDER BY i.InvoiceId DESC LIMIT 1)+1,
		            (SELECT c.CustomerId FROM Customer c WHERE c.username=%s), 
					CURRENT_TIMESTAMP, 
		            (SELECT c.Address FROM Customer c WHERE c.username=%s), 
		            (SELECT c.City FROM Customer c WHERE c.username=%s), 
					(SELECT c.State FROM Customer c WHERE c.username=%s),	
		            (SELECT c.Country FROM Customer c WHERE c.username=%s),
		            (SELECT c.PostalCode FROM Customer c WHERE c.username=%s), 
		            %s);
				'''
			cursor.execute(query,[username,username,username,username,username,username,total])

			query='SELECT i.InvoiceId FROM Invoice i ORDER	BY i.InvoiceId DESC LIMIT 1'
			cursor.execute(query)
			rows = cursor.fetchall()
			invoiceid=int(rows[0][0])

			for k in cart:
				query='SELECT * FROM checkout(%s,%s)'
				cursor.execute(query,[k,invoiceid])
			connection.commit()
			messagebox.showinfo('Soundic Shop', "Checkout successful!")
			printpdf(invoiceid)
			mainApp(username,isEmployee)
			
		except:
			messagebox.showerror('Error', "An error occured during checkout, try again later.")
	else:
		messagebox.showinfo('Soundic Shop (Admin)', "Checkout successful!")
		mainApp(username,isEmployee)

#Print an Invoice pdf after a checkout
def printpdf(invoiceid):
	from reportlab.lib.pagesizes import letter
	from reportlab.pdfgen import canvas
	from reportlab.lib.colors import HexColor

	query='SELECT i.Total FROM Invoice i WHERE i.InvoiceId=%s' 
	cursor.execute(query,[invoiceid])
	rows = cursor.fetchall()
	total= float(rows[0][0])

	query='SELECT i.InvoiceDate FROM Invoice i WHERE i.InvoiceId=%s' 
	cursor.execute(query,[invoiceid])
	rows = cursor.fetchall()
	date= rows[0][0]

	query='SELECT c.FirstName, c.LastName FROM Invoice i JOIN Customer c ON i.CustomerId = c.CustomerId  WHERE i.InvoiceId=%s' 
	cursor.execute(query,[invoiceid])
	rows = cursor.fetchall()
	name= rows[0][0]
	lastname= rows[0][1]

	query= 'SELECT i.BillingAddress FROM Invoice i  WHERE i.InvoiceId=%s'
	cursor.execute(query,[invoiceid])
	rows= cursor.fetchall()
	address=rows[0][0]

	query= 'SELECT i.BillingCity FROM Invoice i  WHERE i.InvoiceId=%s'
	cursor.execute(query,[invoiceid])
	rows= cursor.fetchall()
	city=rows[0][0]

	query= 'SELECT i.BillingCountry FROM Invoice i  WHERE i.InvoiceId=%s'
	cursor.execute(query,[invoiceid])
	rows= cursor.fetchall()
	country=rows[0][0]

	canvas = canvas.Canvas(("Invoice_"+str(invoiceid)+".pdf"), pagesize=letter)
	canvas.setLineWidth(.3)
	canvas.setFont('Helvetica', 12)
	canvas.drawString(30,750,'Invoice details')
	
	canvas.drawString(400,750, ("Date: "+str(date)))
	canvas.line(420,747,580,747)
	 
	canvas.drawString(275,725,'Client:')
	canvas.drawString(500,725,(str(name)+" "+ str(lastname)))
	canvas.line(378,723,580,723)
	 
	canvas.drawString(30,703,'Full Address: ')
	canvas.line(120,700,580,700)
	canvas.drawString(120,703,(str(address)+", "+str(city)+", "+ str(country)))

	canvas.drawImage("logo-soundic.png", 200, 620)

	query='SELECT il.InvoiceLineId, il.invoiceid, t.name, il.UnitPrice, il.Quantity, (il.UnitPrice*il.Quantity) FROM InvoiceLine il JOIN Track t ON t.TrackId=il.TrackId WHERE InvoiceId=%s'
	cursor.execute(query,[invoiceid])
	rows= cursor.fetchall()
	line=0
	canvas.drawString(30,590,"InvoiceLineId ")
	canvas.drawString(130,590,"InvoiceId")
	canvas.drawString(230,590, "Track")
	canvas.drawString(330,590,"Unit Price")
	canvas.drawString(430,590, "Quantity")
	canvas.drawString(530,590, "Total")
	for row in rows:
		canvas.drawString(30,(570-line), str(row[0]))
		canvas.drawString(130,(570-line), str(row[1]))
		canvas.drawString(230,(570-line), str(row[2]))
		canvas.drawString(330,(570-line), str(row[3]))
		canvas.drawString(430,(570-line), str(row[4]))
		canvas.drawString(530,(570-line), str(row[5]))
		line=line+20
	canvas.setFillColor(HexColor('#ff3104'))
	canvas.drawString(490,(570-(line+20)), "Total: ")
	canvas.drawString(530,(570-(line+20)), str(total))

	canvas.save()

def allowInactivate(username,customerid):
	query = 'UPDATE Customer SET inactive_permission=true WHERE CustomerId = %s'
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

def allowModify(username,customerid):
	query = 'UPDATE Customer SET modify_permission=true WHERE CustomerId = %s'
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

def allowDelete(username,customerid):
	query = 'UPDATE Customer SET delete_permission=true WHERE CustomerId = %s'
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

def isInt(v):
    try:
        x = int(v)
        return True
    except ValueError:
        return False

def isFloat(v):
    try:
        x = float(v)
        return True
    except ValueError:
        return False


'''
------------------------------------------
				Clases
------------------------------------------
'''
class MultiColumnListbox(object):

	def __init__(self,frame,headings):
		self.frame = frame
		self.tree = None
		self.columnsToShow = headings
		self.setupWidgets(frame)
		self.buildTree([])

	def setupWidgets(self,frame):
		container = ttk.Frame(frame)
		container.place(relx=0.025,rely=0.1,relwidth=0.85,relheight=0.8)

		style = ttk.Style()
		style.configure("darkStyle.Treeview",font=('Arial', 14),fieldbackground="#121212",background="#121212", foreground="white", relief="flat",rowheight=30)
		style.configure("darkStyle.Treeview.Heading", font=('Arial', 15,'bold'),fieldbackground="#121212",background="white", foreground="#575757", relief="flat")

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

		self.selected = None
		self.tree.bind('<<TreeviewSelect>>', self.on_select)

	def on_select(self, event):
		self.selected = event.widget.selection()

	def getSelection(self):
		textData = []
		if self.selected != None:
			for idx in self.selected:
				textData.append(self.tree.item(idx)['values'])
			return textData[0]
		else:
			return None

	def buildTree(self,rows):
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
				self.tree.column(self.columnsToShow[ix], width=int(1012/len(self.columnsToShow)))

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
				self.tree.column(self.columnsToShow[ix], width=int(1012/len(self.columnsToShow)))



'''
------------------------------------------
				GUI Setup
------------------------------------------
'''

global loginLogo,logo,searchIcon,userIcon,searchIcon,exportIcon,playIcon

# Login Screen
def login(reload):
	root.title('Soundic Login')

	global canvas, frame

	if reload:
		canvas.destroy()
		frame.destroy()

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
	confirmationLabel = tk.Label(text = ' ',font='Arial 12',bg='#121212',fg='#e74c3c')
	confirmationLabel.place(relx=0.34,rely=0.78)

	loginButton = tk.Button(text='Login',bg='white',borderwidth=0, highlightthickness=0,command=lambda: authenticate(username.get(),password.get()))
	loginButton.place(relx=0.35,rely=0.68,relwidth=0.15)

	signInButton = tk.Button(text='Sign Up',bg='white',borderwidth=0, highlightthickness=0,command=lambda: signUp())
	signInButton.place(relx=0.55,rely=0.68,relwidth=0.15)


# Sign up Screen
def signUp():
	root.title('Soundic Sign Up')

	boxWidth = 0.25
	boxHeight = 0.05

	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=900,bg='#101010')
	canvas.pack()
	global frame
	frame.destroy()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	loginLogoLabel = tk.Label(frame,image=loginLogo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	loginLogoLabel.place(relx=0.47,rely=0.04)

	usernameLabel = tk.Label(text = 'Username*',fg='#ffffff',bg='#121212')
	usernameLabel.place(relx=0.45,rely=0.15,relwidth=0.25,relheight=0.05)
	username = tk.Entry(fg='#ffffff',bg='#171717')
	username.place(relx=0.65,rely=0.15,relwidth=boxWidth,relheight=boxHeight)

	passwordLabel = tk.Label(text = 'Password*',fg='#ffffff',bg='#121212')
	passwordLabel.place(relx=0.45,rely=0.22,relwidth=0.25,relheight=0.05)
	password = tk.Entry(fg='#ffffff',bg='#171717')
	password.place(relx=0.65,rely=0.22,relwidth=boxWidth,relheight=boxHeight)

	firstNameLabel = tk.Label(text = 'First Name*',fg='#ffffff',bg='#121212')
	firstNameLabel.place(relx=0.05,rely=0.15,relwidth=0.25,relheight=0.05)
	firstName = tk.Entry(fg='#ffffff',bg='#171717')
	firstName.place(relx=0.25,rely=0.15,relwidth=boxWidth,relheight=boxHeight)

	lastNameLabel = tk.Label(text = 'Last Name*',fg='#ffffff',bg='#121212')
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

	emailLabel = tk.Label(text = 'Email*',fg='#ffffff',bg='#121212')
	emailLabel.place(relx=0.05,rely=0.85,relwidth=0.25,relheight=0.05)
	email = tk.Entry(fg='#ffffff',bg='#171717')
	email.place(relx=0.25,rely=0.85,relwidth=boxWidth,relheight=boxHeight)

	global regConfLabel
	regConfLabel = tk.Label(text = '',font='Arial 12',bg='#121212',fg='#e74c3c')
	regConfLabel.place(relx=0.7,rely=0.3)

	loginButton = tk.Button(text='Create',borderwidth=0, highlightthickness=0,command=lambda: createUser(username.get(),password.get(),firstName.get(),lastName.get(),company.get(),address.get(),city.get(),state.get(),country.get(),postalCode.get(),phone.get(),fax.get(),email.get()))
	loginButton.place(relx=0.35,rely=0.95,relwidth=0.15)

	goBackButton = tk.Button(text='Go Back',borderwidth=0, highlightthickness=0,command=lambda: login(reload=True))
	goBackButton.place(relx=0.55,rely=0.95,relwidth=0.15)


def createUser(username,password,firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email):

	company = None if company == '' else company
	address = None if address == '' else address
	city = None if city == '' else city
	state = None if state == '' else state
	country = None if country == '' else country
	postalCode = None if postalCode == '' else postalCode
	phone = None if phone == '' else phone
	fax = None if fax == '' else fax

	if (len(firstName) not in range(1,41)) or (len(lastName) not in range(1,21)) or (len(email) not in range(1,61)) or (len(username) not in range(1,11)) or (len(password) not in range(1,21)):
		# not a valid register, show a red warning
		regConfLabel['text'] = 'Invalid data lenght'
	else:
		# valid register but username may already exist

		query = """
		SELECT c.username
		FROM Customer c
		WHERE c.username = %s
		UNION
		SELECT e.username
		FROM Employee e
		WHERE e.username = %s
		"""
		cursor.execute(query,[username,username])
		rows = cursor.fetchall()
		
		if len(rows) > 0:
			# then username already exists, show red warning
			regConfLabel['text'] = 'Username already exists'
		else:
			# its a valid register with a unique username

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

			# get a random employee id
			query = """
			SELECT e.EmployeeId
			FROM Employee e
			"""
			cursor.execute(query)
			rows = cursor.fetchall()
			newSupportRepId = rows[random.randint(1,len(rows)-1)][0]

			query = """
			INSERT INTO Customer (username,passwrd,CustomerId,FirstName,LastName,Company,Address,City,State,Country,PostalCode,Phone,Fax,Email,SupportRepId,inactive_permission,modify_permission,delete_permission) 
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
			"""
			cursor.execute(query,[username,password,newCustomerId,firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email,newSupportRepId,False,False,False])
			connection.commit()
			login(reload=True)


def returnPermissions(username):
	query = "SELECT c.inactive_permission,c.modify_permission,c.delete_permission FROM Customer c WHERE c.username = %s LIMIT 1"
	cursor.execute(query,[username])
	rows = cursor.fetchall()
	return rows[0]


# Home Screen
def mainApp(currentUsername,isEmployee):
	root.title('Soundic')

	# Canvas setup
	global canvas
	canvas.destroy()
	canvas = tk.Canvas(root,height=700,width=1200,bg='#101010')
	canvas.pack()

	# Main frame
	global frame
	frame.destroy()
	frame = tk.Frame(root,bg='#121212')
	frame.place(relx=0,rely=0,relwidth=1,relheight=1)

	# Log out button
	logoutButton = tk.Button(frame,text='Logout',command=logout,width=10,height=1,fg='#575757')
	logoutButton.pack(side='bottom')

	#manageLabel = tk.Label(frame,text='Manage',font='Arial 12 bold',fg='#ffffff',bg='#101010')
	#manageLabel.place(relx=0.9,rely=0.23)
	registerButton = tk.Button(frame,text='Register',command=lambda: registerPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
	registerButton.place(relx=0.9,rely=0.2)

	# Show admin options and commands
	if isEmployee:
		manageUsersButton = tk.Button(frame,text='Manage Users',command=lambda: requestCustomerId(currentUsername),width=20,height=1,fg='#575757')
		manageUsersButton.pack(side='top')

		inactivateButton = tk.Button(frame,text='Inactivate',command=lambda: inactivateTrackPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		inactivateButton.place(relx=0.9,rely=0.3)

		modifyButton = tk.Button(frame,text='Modify',command=lambda: modifyPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		modifyButton.place(relx=0.9,rely=0.4)

		deleteButton = tk.Button(frame,text='Delete',command=lambda: deletePage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		deleteButton.place(relx=0.9,rely=0.5)

		statsButton = tk.Button(frame,text='Statistics',command=lambda: statsPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		statsButton.place(relx=0.9,rely=0.6)

		bitacoraButton = tk.Button(frame,text='Binnacle',command=lambda: displayBitacora(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		bitacoraButton.place(relx=0.9,rely=0.7)

		simulateButton = tk.Button(frame,text='Simulate',command=lambda: simulationPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		simulateButton.place(relx=0.9,rely=0.8)
	else:
		# Customer permission
		canInactivate,canModify,canDelete = returnPermissions(currentUsername)

		posY = 0.3

		if canInactivate:
			inactivateButton = tk.Button(frame,text='Inactivate',command=lambda: inactivateTrackPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
			inactivateButton.place(relx=0.9,rely=posY)
			posY += 0.1
		if canModify:
			modifyButton = tk.Button(frame,text='Modify',command=lambda: modifyPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
			modifyButton.place(relx=0.9,rely=posY)
			posY += 0.1
		if canDelete:
			deleteButton = tk.Button(frame,text='Delete',command=lambda: deletePage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
			deleteButton.place(relx=0.9,rely=posY)
			posY += 0.1

		statsButton = tk.Button(frame,text='Statistics',command=lambda: statsPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		statsButton.place(relx=0.9,rely=posY)

	# Soundic Logo
	logoLabel = tk.Label(frame,image=logo,pady=0, padx=0, borderwidth=0, highlightthickness=0)
	logoLabel.place(relx=0.82,rely=0.01)
	if isEmployee:
		adminLabel = tk.Label(frame,text='Admin',font='Arial 14 bold',fg='#ffffff',bg='#101010')
		adminLabel.place(relx=0.935,rely=0.07)

	# Search text field
	searchEntry = tk.Entry(frame,text='Search',fg='#ffffff',bg='#171717')
	searchEntry.place(relx=0.005,rely=0.01,relwidth=0.2,relheight=0.05)

	# Search Button
	searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get(),export=False))
	searchButton.place(relx=0.215,rely=0.015,relwidth=0.025,relheight=0.042)

	# Export Button
	exportButton = tk.Button(frame,image=exportIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get(),export=True))
	exportButton.place(relx=0.265,rely=0.015,relwidth=0.025,relheight=0.042)

	# Play Button
	playButton = tk.Button(frame,image=playIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: playPage(currentUsername,isEmployee))
	playButton.place(relx=0.315,rely=0.015,relwidth=0.025,relheight=0.042)

	# Shop Button
	shopButton = tk.Button(frame,image=shopIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: shopPage(currentUsername,isEmployee))
	shopButton.place(relx=0.365,rely=0.015,relwidth=0.025,relheight=0.042)

	# Profile Button
	profileButton = tk.Button(frame,image=userIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: showProfile(currentUsername,isEmployee))
	profileButton.place(relx=0.6,rely=0.02,relwidth=0.025,relheight=0.042)

	# Logged in Label
	loggedLabel = tk.Label(frame,text=' Logged in as  '+ currentUsername,font='Arial 12',fg='#2ecc71',bg='#101010')
	loggedLabel.place(relx=0.65,rely=0.03)

	global outputTable
	outputTable = MultiColumnListbox(frame,['Track','Artist','Kind','Album','Genre'])


'''
------------------------------------------
				Run App
------------------------------------------
'''

root = tk.Tk()
root.configure(background='black')

# preload assets
loginLogo = tk.PhotoImage(file='assets/logo-login.png')
logo = tk.PhotoImage(file='assets/logo-soundic.png')
searchIcon = tk.PhotoImage(file='assets/icon-search.png')
userIcon = tk.PhotoImage(file='assets/icon-user.png')
exportIcon = tk.PhotoImage(file='assets/icon-export.png')
playIcon = tk.PhotoImage(file='assets/icon-play.png')
playPrevIcon = tk.PhotoImage(file='assets/icon-playprev.png')
playNextIcon = tk.PhotoImage(file='assets/icon-playnext.png')
nextPageIcon = tk.PhotoImage(file='assets/icon-nextpage.png')
shopIcon = tk.PhotoImage(file='assets/icon-shop.png')

login(reload=False)
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()

