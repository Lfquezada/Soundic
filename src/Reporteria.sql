--------------------------
--AMPLIACION DE REPORTERIA
--------------------------

----------------------------------------------------
-- FUNCION 1 PARA VENTAS POR SEMANA EN UN RANGO DADO
-- Recibe 2 fechas
----------------------------------------------------
DROP function IF EXISTS SalesWeek;

CREATE OR REPLACE FUNCTION SalesWeek(inicial DATE, finale DATE)
RETURNS TABLE (ventas bigint, anio_semana text, ingresototal numeric)
AS $$
BEGIN

	RETURN QUERY
	SELECT COUNT(*) AS VENTAS, to_char(DATE(invoicedate), 'IYYY-IW') AS Anio_Semana, SUM(total) AS IngresoTotal
	FROM invoice
	WHERE invoicedate > $1 AND invoicedate < $2
	GROUP BY  Anio_Semana
	ORDER BY Anio_Semana;

END;
$$
LANGUAGE 'plpgsql';
----------------------------------------------------

----------------------------------------------------
-- FUNCION 2 PARA LOS N ARTISTAS CON MAS VENTAS EN UN RANGO DE FECHAS
-- Recibe dos fechas y un int
----------------------------------------------------
DROP FUNCTION IF EXISTS ArtistRange;

CREATE OR REPLACE FUNCTION ArtistRangeE(inicial DATE, finale DATE, num int)
RETURNS TABLE (artistid int, nombre VARCHAR(120), ventas bigint)
AS $$
BEGIN
	
	RETURN QUERY
	SELECT artist.artistid, artist.name, COUNT(*) AS VENTAS
	FROM invoiceline
	JOIN invoice on invoiceline.invoiceid = invoice.invoiceid
	JOIN track on invoiceline.trackid = track.trackid
	JOIN album on track.albumid = album.albumid
	JOIN artist on album.artistid = artist.artistid
	WHERE invoicedate > $1 AND invoicedate < $2
	GROUP BY artist.artistid
	ORDER BY COUNT(*) DESC
	LIMIT $3;

END;
$$
LANGUAGE 'plpgsql';

----------------------------------------------------

----------------------------------------------------
-- FUNCION 3 PARA VENTAS POR GENERO EN UN RANGO DE FECHAS
-- Recibe dos fechas
----------------------------------------------------
DROP FUNCTION IF EXISTS GenreRange;

CREATE OR REPLACE FUNCTION GenreRange(inicial DATE, finale DATE)
RETURNS TABLE (genid int, genre VARCHAR(120), ventas bigint)
AS $$
BEGIN

	RETURN QUERY
	SELECT genre.genreid, genre.name, COUNT(*) AS VENTAS
	FROM invoiceline
	JOIN invoice on invoiceline.invoiceid = invoice.invoiceid
	JOIN track on invoiceline.trackid = track.trackid
	JOIN genre on track.genreid = genre.genreid
	WHERE invoicedate > $1 AND invoicedate < $2
	GROUP BY genre.genreid
	ORDER BY VENTAS DESC;
	
END;
$$
LANGUAGE 'plpgsql';

----------------------------------------------------

----------------------------------------------------
-- FUNCION 4 PARA CANCIONES MAS REPRODUCIDAS DE UN ARTISTA
-- Recibe un artista y un int para la cantidad de canciones
----------------------------------------------------

DROP FUNCTION IF EXISTS ArtistPlays;

CREATE OR REPLACE FUNCTION ArtistPlays(artista VARCHAR(120), num int)
RETURNS TABLE (artist VARCHAR(120), trackid int, song VARCHAR (200), reproducciones bigint)
AS $$
BEGIN

	RETURN QUERY
	SELECT artist.name AS artista, track.trackid, track.name AS cancion, SUM(plays) AS plays
	FROM plays
	JOIN track on track.trackid = plays.trackid
	JOIN album on track.albumid = album.albumid
	JOIN artist on album.artistid = artist.artistid
	WHERE artist.name = $1
	GROUP BY track.trackid, artist.name
	LIMIT $2;

END;
$$
LANGUAGE 'plpgsql';

----------------------------------------------------