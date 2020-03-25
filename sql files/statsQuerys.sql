--1. Top 5 Artistas con más albumes
SELECT artist.name, COUNT(artist.artistid)
FROM album
JOIN artist ON album.artistid = artist.artistid
GROUP BY artist.artistid
ORDER BY COUNT(artist.artistid) DESC
LIMIT 5

--2.Top 5 Generos con mas canciones
SELECT genre.name, COUNT(genre.name) 
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name, genre.genreid 
ORDER BY COUNT(genre.name) DESC
LIMIT 5

--3.Total de duración de cada playlist (return 'Playlist','Minute Duration')
SELECT playlist.name, (SUM(milliseconds)/60000)
FROM playlist
JOIN playlisttrack on playlist.playlistid = playlisttrack.playlistid
JOIN track on playlisttrack.trackid = track.trackid
GROUP BY playlist.name

--4. Top 5 Canciones de mayor duración con la información de sus artistas
SELECT track.name, track.milliseconds/1000.0/60.0,artist.name
FROM track
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
ORDER BY track.milliseconds DESC
LIMIT 5

--5. Top 5 Usuarios que han registrado más canciones (return 'User','Songs Registered')
SELECT firstname, lastname, COUNT(trackid)
FROM track_register
JOIN customer on track_register.customerid = customer.customerid
GROUP BY track_register.customerid, firstname, lastname
ORDER BY COUNT(trackid) DESC
LIMIT 5

--6.Promedio de duración de canciones por género
SELECT genre.name,(AVG(track.milliseconds)/1000)/60
FROM track
JOIN genre on track.genreid = genre.genreid
GROUP BY genre.name

--7.Cantidad de artistas diferentes por playlist (return 'Playlist','Artist Count')
SELECT playlist.name, COUNT(DISTINCT artist.name)
FROM playlisttrack
JOIN playlist on playlisttrack.playlistid = playlist.playlistid
JOIN track on playlisttrack.trackid = track.trackid
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
GROUP BY playlist.name

--8. Top 5 Artistas con más diversidad de géneros musicales (return 'Artist','Genre Count')
SELECT artist.name, COUNT(DISTINCT genreid)
FROM track
JOIN album on track.albumid = album.albumid
JOIN artist on album.artistid = artist.artistid
GROUP BY artist.name
ORDER BY COUNT(DISTINCT genreid) DESC
LIMIT 5

-- 9. Most used MediaType
SELECT mt.Name, COUNT(mt.MediaTypeId)
FROM Track t
JOIN MediaType mt ON mt.MediaTypeId = t.MediaTypeId
GROUP BY mt.MediaTypeId
ORDER BY COUNT(mt.MediaTypeId) DESC

-- 10. 


