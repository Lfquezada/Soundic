--1.Artistas con más albums
SELECT artist.name,COUNT(artist.artistid)
FROM album
JOIN artist ON album.artistid = artist.artistid
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC
LIMIT 5

--2.Generos con mas canciones
SELECT genre.name, COUNT(genre.name) 
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name, genre.genreid 
ORDER BY COUNT(genre.name) DESC
LIMIT 5


--3.Total de duración de cada playlist (return 'Playlist','Duration')


--4.Canciones de mayor duración con la información de sus artistas
SELECT track.name, track.milliseconds/1000.0/60.0,artist.name
FROM track
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
ORDER BY track.milliseconds DESC
LIMIT 5


--5.Usuarios que han registrado más canciones (return 'User','Songs Registered')
LIMIT 5


--6.Promedio de duración de canciones por género
SELECT genre.name,(AVG(track.milliseconds)/1000)/60
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name


--7.Cantidad de artistas diferentes por playlist (return 'Playlist','Artist Count')



--8.Artistas con más diversidad de géneros musicales (return 'Artist','Collab Count')
LIMIT 5


