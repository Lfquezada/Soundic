--1.Artistas por área
--No se a que se refiere con area

--2.Generos con mas canciones
SELECT genre.name, COUNT(genre.name) 
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name, genre.genreid 
ORDER BY COUNT(genre.name) DESC


--3.Artistas con más albums individuales
SELECT artist.name,COUNT(artist.artistid)
FROM album
JOIN artist ON album.artistid = artist.artistid
WHERE artist.name NOT LIKE '%Feat.%'
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC


--4.Canciones de mayor duración con la información de sus artistas
SELECT track.name, track.milliseconds/1000.0/60.0,artist.name
FROM track
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
ORDER BY track.milliseconds DESC


--5.Usuarios que han registrado más canciones
SELECT COUNT(invoice.customerid),customer.firstname,customer.lastname
FROM invoice
JOIN customer ON invoice.customerid = customer.customerid
GROUP BY customer.firstname, customer.lastname
ORDER BY COUNT(invoice.customerid) DESC


--6.Promedio de duración de canciones por género
SELECT genre.name,(AVG(track.milliseconds)/1000)/60
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name


--7.Álbumes más recientes
--No hay info de fecha en los albumes


--8.Artistas más colaborativos
SELECT artist.name,COUNT(artist.artistid)
FROM album
JOIN artist ON album.artistid = artist.artistid
WHERE artist.name LIKE '%Feat.%'
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC


