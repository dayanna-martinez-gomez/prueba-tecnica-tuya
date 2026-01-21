-- Ejercicio 3 (SQLite) - UNA sola consulta
-- Convención: corte_mes = último día del mes (EOM)
-- Parámetros:
--   fecha_base: fin de mes (ej: '2024-12-31')
--   n: mínimo de meses de racha (ej: 3)

WITH
params AS (
	SELECT
		date('2024-12-31') AS fecha_base,
		3 AS n
),
-- 1. Primer corte por cliente (EOM)
primer_mes AS (
	SELECT
		identificacion,
		MIN(date(corte_mes, 'start of month', '+1 month', '-1 day')) AS primer_corte
	FROM historia
	GROUP BY identificacion
),
-- 2. Calendario mensual en EOM (sin saltos) desde primer_corte hasta fecha_base
calendario AS (
	WITH RECURSIVE c AS (
		SELECT
			p.identificacion,
			p.primer_corte AS corte_mes
		FROM primer_mes p

		UNION ALL

		SELECT
			c.identificacion,
			date(c.corte_mes, 'start of month', '+2 months', '-1 day') AS corte_mes
		FROM c
		JOIN params pa
		WHERE date(c.corte_mes, 'start of month', '+2 months', '-1 day') <= pa.fecha_base
	)
SELECT * FROM c
),
-- 3. Quitar meses posteriores al retiro (comparando también a EOM)
calendario_validado AS (
	SELECT
		cal.identificacion,
		cal.corte_mes
	FROM calendario cal
	LEFT JOIN retiros r
		ON r.identificacion = cal.identificacion
	WHERE r.identificacion IS NULL
		OR cal.corte_mes <= date(r.fecha_retiro, 'start of month', '+1 month', '-1 day')
),
-- 4) Completar saldos faltantes (N0) + clasificar nivel
saldos_completos AS (
	SELECT
		cv.identificacion,
		cv.corte_mes,
		COALESCE(h.saldo, 0) AS saldo,
		CASE
			WHEN COALESCE(h.saldo, 0) >= 0       AND COALESCE(h.saldo, 0) <  300000   THEN 'N0'
			WHEN COALESCE(h.saldo, 0) >= 300000  AND COALESCE(h.saldo, 0) <  1000000  THEN 'N1'
			WHEN COALESCE(h.saldo, 0) >= 1000000 AND COALESCE(h.saldo, 0) <  3000000  THEN 'N2'
			WHEN COALESCE(h.saldo, 0) >= 3000000 AND COALESCE(h.saldo, 0) <  5000000  THEN 'N3'
			WHEN COALESCE(h.saldo, 0) >= 5000000                                   THEN 'N4'
		ELSE 'N0'
		END AS nivel
	FROM calendario_validado cv
	LEFT JOIN historia h
		ON h.identificacion = cv.identificacion
		AND date(h.corte_mes, 'start of month', '+1 month', '-1 day') = cv.corte_mes
),
-- 5) Marcar rachas consecutivas por nivel
rachas_marcadas AS (
	SELECT
		identificacion,
		corte_mes,
		nivel,
		ROW_NUMBER() OVER (PARTITION BY identificacion ORDER BY corte_mes)
		- ROW_NUMBER() OVER (PARTITION BY identificacion, nivel ORDER BY corte_mes)
		AS grupo_racha
	FROM saldos_completos
),
-- 6) Resumir rachas (una fila por racha)
resumen_rachas AS (
	SELECT
		identificacion,
		nivel,
		grupo_racha,
		COUNT(*) AS racha,
		MAX(corte_mes) AS fecha_fin
	FROM rachas_marcadas
	GROUP BY identificacion, nivel, grupo_racha
),
-- 7) Filtrar candidatas (racha >= n y termina <= fecha_base)
candidatas AS (
	SELECT rr.*
	FROM resumen_rachas rr
	JOIN params pa
	WHERE rr.racha >= pa.n
		AND rr.fecha_fin <= pa.fecha_base
),
-- 8) Elegir por cliente: racha más larga; si empate, la más reciente
ranked AS (
	SELECT *,
		ROW_NUMBER() OVER (
		PARTITION BY identificacion
		ORDER BY racha DESC, fecha_fin DESC
		) AS rn
	FROM candidatas
)
SELECT
	identificacion,
	racha,
	fecha_fin,
	nivel
FROM ranked
WHERE rn = 1
ORDER BY identificacion