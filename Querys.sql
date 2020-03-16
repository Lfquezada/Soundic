--1.Artistas por área
--No se a que se refiere con area

--2.Generos con mas canciones
SELECT genre.genreid, genre.name, COUNT(genre.name) 
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name, genre.genreid 
ORDER BY COUNT(genre.name) DESC


--3.Artistas con más albums individuales
SELECT COUNT(artist.artistid)AS "Cantidad de albumes individuales", artist.name AS "Artista"  
FROM album
JOIN artist ON album.artistid = artist.artistid
WHERE artist.name NOT LIKE '%Feat.%'
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC


--4.Canciones de mayor duración con la información de sus artistas
SELECT track.name AS "Cancion", track.milliseconds/1000.0/60.0 AS "Duracion minutos", artist.name AS "Nombre de artista"
FROM track
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
ORDER BY track.milliseconds DESC


--5.Usuarios que han registrado más canciones
SELECT COUNT(invoice.customerid) AS "Canciones Registradas", customer.firstname AS "Nombre", customer.lastname AS "Apellido"
FROM invoice
JOIN customer ON invoice.customerid = customer.customerid
GROUP BY customer.firstname, customer.lastname
ORDER BY COUNT(invoice.customerid)DESC


--6.Promedio de duración de canciones por género
SELECT genre.name AS "Genero", (AVG(track.milliseconds)/1000)/60 AS "Minutos Promedio"
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name


--7.Álbumes más recientes
--No hay info de fecha en los albumes


--8.Artistas más colaborativos
SELECT COUNT(artist.artistid)AS "Cantidad de albumes colaborativos", artist.name AS "Artista"  
FROM album
JOIN artist ON album.artistid = artist.artistid
WHERE artist.name LIKE '%Feat.%'
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC


