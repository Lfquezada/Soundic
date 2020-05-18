#This python script interact with a postgresql db and allows to save a report of an specific date in a mongo db

import psycopg2 as pg
import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db=client.recommendations
purchases_collection = db["purchases"]
recent_tracks_collection= db["new_tracks"]

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
		SELECT json_agg(purchases) from purchases
		"""
	#Writing json file with purchases made on the date indicated
	cursor.execute(query,[date])
	rows = cursor.fetchall()
	purchases=[]
	for row in rows:
		for key in cursor.description:
			purchases.append({key[0]: value for value in row})
	with open('purchases.json', 'w') as file:
		json.dump({'purchases':purchases}, file, indent=4 )

	#Reading json file and adding a document to a mongo db collection
	data_json={}
	with open('purchases.json', 'r') as data_file:
	    data_json = json.load(data_file)
	purchases_collection.insert(data_json)



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
		WHERE r.Date >= '2020-04-30')
	SELECT json_agg(newTracks) from newTracks
	"""
	cursor.execute(query)
	rows = cursor.fetchall()
	tracks=[]
	for row in rows:
		for key in cursor.description:
			tracks.append({key[0]: value for value in row})
	with open('RecentTracks.json', 'w') as file:
		json.dump({'tracks':tracks}, file, indent=4 )

	data_json={}
	with open('RecentTracks.json', 'r') as data_file:
	    data_json = json.load(data_file)
	recent_tracks_collection.insert(data_json)

def recommendation(date):
	genres=[]
	result={}
	query = purchases_collection.find({'purchases.json_agg.date':'2010-02-08T00:00:00'}, {'purchases.json_agg.genre':1})
	for i in query:
		result['genre']:id
	print(result)

#purchases('2010/2/8')
#RecentTracks()
recommendation('2010-02-08')


