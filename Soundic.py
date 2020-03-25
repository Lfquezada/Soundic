
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

	if username == '' and password == '':
		mainApp('testUser',isEmployee=True)

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
			INSERT INTO Artist (ArtistId,Name) 
			VALUES (%s,%s);
			"""
			cursor.execute(query,[newArtistId,artistName])
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
			INSERT INTO Album (AlbumId,Title,ArtistId) 
			VALUES (%s,%s,%s);
			"""
			cursor.execute(query,[newAlbumId,albumTitle,artistId])
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
							INSERT INTO Track (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice,Active)
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
							"""
							cursor.execute(query,[newTrackId,trackName,albumId,mediaTypeId,genreId,composer,millisec,bytes,unitPrice,True])
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

				query = "UPDATE Artist SET Name = %s WHERE ArtistId = %s"
				cursor.execute(query,[newArtistName,artistId])
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

				query = "UPDATE Album SET Title = %s WHERE AlbumId = %s AND ArtistId = %s"
				cursor.execute(query,[newAlbumTitle,albumId,artistId])
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
					query = "UPDATE Track SET Name = %s, Composer = %s, Milliseconds = %s, Bytes = %s, UnitPrice = %s WHERE TrackId = %s"
					cursor.execute(query,[trackName,composer,millisec,bytes,unitPrice,trackId])
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
		query = """
		SELECT artist.name,COUNT(artist.artistid)
		FROM album
		JOIN artist ON album.artistid = artist.artistid
		GROUP BY artist.artistid
		ORDER BY COUNT(artist.artistid) DESC
		LIMIT 5
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 2:
		statsTable = MultiColumnListbox(frame,['Genre','Track Count'])
		query = """
		SELECT genre.name, COUNT(genre.name) 
		FROM track
		JOIN genre on track.genreid = genre.genreid
		GROUP BY genre.name, genre.genreid 
		ORDER BY COUNT(genre.name) DESC
		LIMIT 5
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 3:
		statsTable = MultiColumnListbox(frame,['Playlist','Duration (min)'])
		query = """
		SELECT playlist.name, ROUND((SUM(milliseconds)/60000.0),2)
		FROM playlist
		JOIN playlisttrack ON playlist.playlistid = playlisttrack.playlistid
		JOIN track ON playlisttrack.trackid = track.trackid
		GROUP BY playlist.name
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 4:
		statsTable = MultiColumnListbox(frame,['Track','Artist','Duration (min)'])
		query = """
		SELECT track.name, artist.name, ROUND(track.milliseconds/60000.0,2)
		FROM track
		JOIN album ON track.albumid = album.albumid
		JOIN artist ON album.artistid = artist.artistid
		ORDER BY track.milliseconds DESC
		LIMIT 5
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 5:
		statsTable = MultiColumnListbox(frame,['First Name','Last Name','Tracks Registered'])
		query = """
		SELECT firstname, lastname, COUNT(trackid)
		FROM track_register
		JOIN customer ON track_register.customerid = customer.customerid
		GROUP BY track_register.customerid,firstname,lastname
		ORDER BY COUNT(trackid) DESC
		LIMIT 5
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 6:
		statsTable = MultiColumnListbox(frame,['Genre','Average (min)'])
		query = """
		SELECT genre.name,ROUND(AVG(track.milliseconds)/60000.0,2)
		FROM track
		JOIN genre ON track.genreid = genre.genreid
		GROUP BY genre.name
		ORDER BY ((AVG(track.milliseconds)/1000)/60) DESC
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 7:
		statsTable = MultiColumnListbox(frame,['Playlist','Artist Count'])
		query = """
		SELECT playlist.name, COUNT(DISTINCT artist.name)
		FROM playlisttrack
		JOIN playlist on playlisttrack.playlistid = playlist.playlistid
		JOIN track on playlisttrack.trackid = track.trackid
		JOIN album on track.albumid = album.albumid
		JOIN artist on album.artistid = artist.artistid
		GROUP BY playlist.name
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 8:
		statsTable = MultiColumnListbox(frame,['Artist','Genre Count'])
		query = """
		SELECT artist.name, COUNT(DISTINCT genreid)
		FROM track
		JOIN album on track.albumid = album.albumid
		JOIN artist on album.artistid = artist.artistid
		GROUP BY artist.name
		ORDER BY COUNT(DISTINCT genreid) DESC
		LIMIT 5
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 9:
		statsTable = MultiColumnListbox(frame,['Media Type','Count'])
		query = """
		SELECT mt.Name, COUNT(mt.MediaTypeId)
		FROM Track t
		JOIN MediaType mt ON mt.MediaTypeId = t.MediaTypeId
		GROUP BY mt.MediaTypeId
		ORDER BY COUNT(mt.MediaTypeId) DESC
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
	if num == 10:
		statsTable = MultiColumnListbox(frame,['Billing Country','Purchases'])
		query = """
		SELECT   BillingCountry, COUNT(BillingCountry)
		FROM Invoice 
		GROUP BY BillingCountry
		ORDER BY (COUNT(BillingCountry)) DESC
		"""
		cursor.execute(query)
		rows = cursor.fetchall()
		statsTable.updateData(rows)
		


	returnToAppButton = tk.Button(frame,text='Return to App',fg='#575757',command=lambda: mainApp(username,isEmployee))
	returnToAppButton.pack(side='bottom')


def search(entry):

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
		displaySearchResult(rowsSearch)


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

def allowInactivate(username,customerid):
	query = "UPDATE Customer SET inactive_permission=true WHERE CustomerId = %s"
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

def allowModify(username,customerid):
	query = "UPDATE Customer SET modify_permission=true WHERE CustomerId = %s"
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

def allowDelete(username,customerid):
	query = "UPDATE Customer SET delete_permission=true WHERE CustomerId = %s"
	cursor.execute(query,[customerid])
	connection.commit()
	mainApp(username,isEmployee=True)

# Fill output Table with the query result
def displaySearchResult(rows):
	outputTable.updateData(rows)

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
				self.tree.column(self.columnsToShow[ix], width=int(1008/len(self.columnsToShow)))

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
				self.tree.column(self.columnsToShow[ix], width=int(1004/len(self.columnsToShow)))




'''
------------------------------------------
				GUI Setup
------------------------------------------
'''

global loginLogo,logo,searchIcon,userIcon

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
		LIMIT 1
		"""
		cursor.execute(query,[username])
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
			INSERT INTO Customer (username,passwrd,CustomerId,FirstName,LastName,Company,Address,City,State,Country,PostalCode,Phone,Fax,Email,SupportRepId) 
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
			"""
			cursor.execute(query,[username,password,newCustomerId,firstName,lastName,company,address,city,state,country,postalCode,phone,fax,email,newSupportRepId])
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

	manageLabel = tk.Label(frame,text='Manage Tracks',font='Arial 11 bold',fg='#ffffff',bg='#101010')
	manageLabel.place(relx=0.9,rely=0.23)
	registerButton = tk.Button(frame,text='Register',command=lambda: registerPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
	registerButton.place(relx=0.9,rely=0.3)

	# Show admin options and commands
	if isEmployee:
		manageUsersButton = tk.Button(frame,text='Manage Users',command=lambda: requestCustomerId(currentUsername),width=20,height=1,fg='#575757')
		manageUsersButton.pack(side='top')

		inactivateButton = tk.Button(frame,text='Inactivate',command=lambda: inactivateTrackPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		inactivateButton.place(relx=0.9,rely=0.4)

		modifyButton = tk.Button(frame,text='Modify',command=lambda: modifyPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		modifyButton.place(relx=0.9,rely=0.5)

		deleteButton = tk.Button(frame,text='Delete',command=lambda: deletePage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		deleteButton.place(relx=0.9,rely=0.6)

		statsButton = tk.Button(frame,text='Statistics',command=lambda: statsPage(currentUsername,isEmployee),width=10,height=2,fg='#575757')
		statsButton.place(relx=0.9,rely=0.7)
	else:
		# Customer permission
		canInactivate,canModify,canDelete = returnPermissions(currentUsername)

		posY = 0.4

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
	searchEntry.place(relx=0.005,rely=0.01,relwidth=0.25,relheight=0.05)

	# Search Button
	searchButton = tk.Button(frame,image=searchIcon,pady=0, padx=0, borderwidth=0, highlightthickness=0,command=lambda: search(searchEntry.get()))
	searchButton.place(relx=0.265,rely=0.015,relwidth=0.025,relheight=0.042)

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

login(reload=False)
root.mainloop()


'''
------------------------------------------
			Close Connections
------------------------------------------
'''
cursor.close()
connection.close()









