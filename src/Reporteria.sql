--------------------------
--AMPLIACION DE REPORTERIA
--------------------------

----------------------------------------------------
-- FUNCION 1 PARA VENTAS POR SEMANA EN UN RANGO DADO
-- Recibe 2 fechas
----------------------------------------------------
DROP function IF EXISTS SALESWEEK;

CREATE OR REPLACE FUNCTION SALESWEEK(inicial DATE, finale DATE)
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
DROP FUNCTION IF EXISTS ARTISTRANGE;

CREATE OR REPLACE FUNCTION ARTISTRANGE(inicial DATE, finale DATE, num int)
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