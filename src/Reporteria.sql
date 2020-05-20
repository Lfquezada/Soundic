--------------------------
--AMPLIACION DE REPORTERIA
--------------------------

----------------------------------------------------
-- FUNCION 1 PARA VENTAS POR SEMANA EN UN RANGO DADO
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
--FUNCION 2 PARA LOS N ARTISTAS CON MAS VENTAS EN UN RANGO DE FECHAS
----------------------------------------------------
DROP FUNCTION IF EXISTS ARTISTRANGE;