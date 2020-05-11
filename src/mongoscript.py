
import psycopg2 as pg
import json
import pymongo
#client = pymongo.MongoClient('mongodb://localhost:27017/')

connection = pg.connect(user='postgres',host='localhost',port='5432',database='Soundic',password='dbpass20')
cursor = connection.cursor()

#Writing json file with purchases made on the date indicated
def purchases (date):
	query = """
	     SELECT row_to_json(data) FROM (
	      SELECT *
			FROM InvoiceLine il
			JOIN Invoice i ON il.InvoiceId= i.InvoiceId
			JOIN Customer c ON i.CustomerId=c.CustomerId
			WHERE i.InvoiceDate= %s
	     ) data;
		"""
	cursor.execute(query,[date])
	rows = cursor.fetchall()
	with open('purchases.json', 'w') as file:
		json.dump(rows, file, indent=4)

#Writing json file with recent tracks 
def RecentTracks():
	query="""
	SELECT row_to_json(data) FROM(
		SELECT 
		FROM track_register tr
		JOIN Track t ON  t.TrackId=tr.TrackId
		WHERE tr.Date > '2020-04-30'
	)data;
	"""
	cursor.execute(query)
	rows = cursor.fetchall()
	with open('RecentTracks.json', 'w') as file:
		json.dump(rows, file, indent=4)


purchases('2010/2/8')
RecentTracks()


