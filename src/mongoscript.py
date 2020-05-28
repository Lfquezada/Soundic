#Soundic
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
		AS ( SELECT i.InvoiceDate AS date, g.name AS genre, c.FirstName, c.LastName, c.CustomerId, t.Name AS track
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
	print('The purchases made in '+date+' have been added to purchases collection')



#Writing json file with recent tracks 
def RecentTracks(date):
	query="""
	WITH newTracks (Trackid, name, album, MediaType, composer, Milliseconds, Bytes, UnitPrice, genre) 
	AS (SELECT t.TrackId, t.Name, a.Title AS album, m.MediaTypeId AS MediaType, t.Composer, t.Milliseconds, t.Bytes, t.UnitPrice, g.name AS genre
		FROM track_register r
		JOIN Track t ON  t.TrackId=r.TrackId
		JOIN Genre g ON t.GenreId=g.GenreId
		JOIN Album a ON a.AlbumId=t.AlbumId
		JOIN MediaType m ON m.MediaTypeId= t.MediaTypeId
		WHERE r.Date >= %s)
	SELECT row_to_json(newTracks) from newTracks
	"""
	cursor.execute(query,[date])
	rows = cursor.fetchall()
	tracks_collection.delete_many( { } )
	for row in rows:
		for key in cursor.description:
			tracks_collection.insert_one({key[0]: value for value in row})
	print('New tracks have been added to Tracks collection')


def recommendation():
	genres=[]
	clients=[]
	tracks=[]
	result=''
	recommendation=[]

	#Looking for clients in Mongo DB
	query = purchases_collection.find({"row_to_json.date" : {'$gt': '2008-12-31TT00:00:00'} }, {'row_to_json.genre':1, '_id':0}).limit(20)
	for i in query:
		result=str(i)
		f=result.split(':')
		k=f[2]
		h=((k.replace(" '","")).replace("}","")).replace("'","")
		genres.append(h)
	#print (genres)


	#Looking for the purchased tracks genres by the clients in Mongo DB
	query1 = purchases_collection.find({"row_to_json.date" : {'$gt': '2008-12-31TT00:00:00'}}, {'row_to_json.firstname':1, '_id':0}).limit(20)
	for i in query1:
		result=str(i)
		f=result.split(':')
		k=f[2]
		h=((k.replace(" '","")).replace("}","")).replace("'","")
		clients.append(h)
	#print (clients)

	query3 = purchases_collection.find({"row_to_json.date" : {'$gt': '2008-12-31TT00:00:00'}}, {'row_to_json.track':1, '_id':0}).limit(20)
	for i in query3:
		result=str(i)
		f=result.split(':')
		k=f[2]
		h=((k.replace(" '","")).replace("}","")).replace("'","")
		tracks.append(h)

	#Recommendations for the users found in Mongo DB based on the tracks genres
	contador=0
	for i in genres:
		query2=tracks_collection.find({"row_to_json.genre": i}, {'_id':0})
		print ('\n Because you bought '+ str (tracks[contador])+ ' our recommendation for '+ str (clients[contador])+ '\n')
		for j in query2:
			print (j)
		contador=contador+1
		

#Add purchases to mongo DB purchases collection 			
#purchases('2013/9/2')
#purchases('2013/12/4')
#purchases('2010/02/08')
#purchases ('2012/12/28')
#2013/5/2

#Add recent tracks to mongo DB tracks collection
#RecentTracks()

#Make a recommendation
#recommendation()
#'2020-03-01'

print ('\nBienvenido, a continuación se muestran las acciones que puede realizar \n 1. Ingresar las compras de una fecha especifica a la BD de Mongo \n 2. Actualizar las canciones recientes en la BD de mongo \n 3. Obtener recomendaciones para 10 clientes \n 4. Salir' )
opcion=input('Ingrese la accion que desea realizar: ')
while (opcion!='4'):
	if (opcion=='1'):
		fecha=input('Ingrese la fecha de las compras que desea almacenar en la BD de Mongo en formato (YYYY/M/D) ')
		purchases(fecha)
	elif (opcion=='2'):
		date=input('Ingrese la fecha a partir de la cual desea que se ingresen las canciones recientes en formato (YYYY-MM-DD) ')
		RecentTracks(date)
	elif (opcion=='3'):
		print ('-------------------------------------------------Recomendaciones-----------------------------------------------------------------------------------')
		recommendation()
	else: 
		print('La opcion ingresada no es valida')
	print ('\nBienvenido, a continuación se muestran las acciones que puede realizar \n 1. Ingresar las compras de una fecha especifica a la BD de Mongo \n 2. Actualizar las canciones recientes en la BD de mongo \n 3. Obtener recomendaciones para 10 clientes \n 4. Salir' )
	opcion=input('Ingrese la accion que desea realizar> ')

