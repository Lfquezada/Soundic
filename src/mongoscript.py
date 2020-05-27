#This python script interact with a postgresql db and allows to save a report of an specific date in a mongo db

import psycopg2 as pg
import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db=client.recommendations
purchases_collection = db["purchases"]
tracks_collection= db["tracks"]

connection = pg.connect(user='postgres',host='localhost',port='5432',database='Soundic',password='dbpass20')
cursor = connection.cursor()

#Writing json file with purchases made on the date indicated
def purchases (date):
	query = """
		WITH purchases (date, genre, firstname, lastname, customerid) 
		AS ( SELECT i.InvoiceDate AS date, g.name AS genre, c.FirstName, c.LastName, c.CustomerId
			FROM InvoiceLine il
			JOIN Invoice i ON il.InvoiceId= i.InvoiceId
			JOIN Customer c ON i.CustomerId=c.CustomerId
			JOIN Track t ON t.TrackId=il.TrackId
			JOIN Genre g ON g.GenreId=t.GenreId
			WHERE i.InvoiceDate= %s)
		SELECT row_to_json(purchases) from purchases
		"""
	data_json={}
	#Writing json file with purchases made on the date indicated
	cursor.execute(query,[date])
	rows = cursor.fetchall()
	for row in rows:
		for key in cursor.description:
			purchases_collection.insert_one({key[0]: value for value in row})


#Writing json file with recent tracks 
def RecentTracks():
	query="""
	WITH newTracks (Trackid, name, album, MediaType, composer, Milliseconds, Bytes, UnitPrice, genre) 
	AS (SELECT t.TrackId, t.Name, a.Title AS album, m.MediaTypeId AS MediaType, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice, g.name AS genre
		FROM track_register r
		JOIN Track t ON  t.TrackId=r.TrackId
		JOIN Genre g ON t.GenreId=g.GenreId
		JOIN Album a ON a.AlbumId=t.AlbumId
		JOIN MediaType m ON m.MediaTypeId= t.MediaTypeId
		WHERE r.Date > '2012-10-01')
	SELECT row_to_json(newTracks) from newTracks
	"""
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
		for key in cursor.description:
			tracks_collection.insert_many({key[0]: value for value in row})


def recommendation(date):
	genres=[]
	clients=[]
	result=''

	query = purchases_collection.find({"row_to_json.date" : date }, {'row_to_json.genre':1, '_id':0})
	for i in query:
		result=str(i)
		f=result.split(':')
		k=f[2]
		h=((k.replace(" '","")).replace("}","")).replace("'","")
		genres.append(h)
	print (genres)

	query1 = purchases_collection.find({"row_to_json.date" : date}, {'row_to_json.firstname':1, '_id':0})
	for i in query1:
		result=str(i)
		f=result.split(':')
		k=f[2]
		h=((k.replace(" '","")).replace("}","")).replace("'","")
		clients.append(h)
	print (clients)
	for i in genres:
		query2=recent_tracks_collection.find({"row_to_json.genre": i})
		
			
#purchases('2010/2/8')
RecentTracks()
#recommendation('2010-02-08T00:00:00')


